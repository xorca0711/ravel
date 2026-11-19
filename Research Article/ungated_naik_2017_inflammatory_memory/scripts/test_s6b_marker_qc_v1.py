"""Constructed counts only; no actual D6 marker profile is read before freeze."""
import copy
import csv
import gzip
import json
from pathlib import Path
import tempfile
import unittest

from s6b_marker_qc_v1 import MARKERS, SAMPLES, reconstruct, write_outputs, table, read_rows
from s6b_verify_v1 import verify


def fixture(folder):
    cp, meta, qc = {}, [], []
    for j, gsm in enumerate(SAMPLES):
        p = folder/(gsm+'_artificial.tab.gz'); cp[gsm] = p
        values = [j*10+i for i in range(5)]+[100]
        genes = [m[1] for m in MARKERS]+['ENSMUSG00000000001.1']
        with gzip.open(p, 'wt', encoding='utf-8') as f:
            for g, v in zip(genes, values): f.write(f'{g}\t{v}\n')
        role, condition = ('control', 'control') if j < 2 else ('exposed', 'acute_inflamed')
        meta.append(dict(gsm=gsm, assay='RNA-seq', day_label='6', wound_hour_label='', label_conflicts='',
            history_label='control' if j < 2 else 'prior_inflammation', runs='SRR'+str(5133553+j), biosamples='sample'+str(j),
            instrument_models='Illumina HiSeq 4000', library_layouts='PAIRED', count_files=p.name,
            characteristics='Sex: female | artificial fixture'))
        qc.append(dict(gsm=gsm, time='D6', role=role, condition=condition, short_label=['D6_C1','D6_C2','D6_A1','D6_A2'][j],
            run=meta[-1]['runs'], biosample=meta[-1]['biosamples'], instrument=meta[-1]['instrument_models'], layout='PAIRED',
            source_file=p.name, gene_count_total=sum(values), mor_size_factor=2+j, total_count_size_factor=4+j))
    crosswalk, qpath, annotation = folder/'crosswalk.tsv', folder/'s2.tsv', folder/'m9.gtf.gz'
    table(crosswalk, meta); table(qpath, qc)
    with gzip.open(annotation, 'wt', encoding='utf-8') as f:
        for name, gene, chrom, typ in MARKERS:
            f.write(f'{chrom}\tfixture\tgene\t1\t2\t.\t+\t.\tgene_id "{gene}"; gene_name "{name}"; gene_type "{typ}";\n')
    return cp, crosswalk, qpath, annotation


class FixedMarkerTests(unittest.TestCase):
    def test_full_library_denominator_fixed_factors_zero_and_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); args=fixture(p); data=reconstruct(*args, expected_gene_count=6)
            first, second=data['marker_qc'][:2]
            self.assertEqual(first['raw'],0); self.assertEqual(first['log2_cpm_plus1'],0)
            self.assertTrue(first['raw_zero']); self.assertEqual(first['recorded_sex'],'female')
            self.assertEqual(second['mor'],.5); self.assertEqual(second['total'],.25)
            self.assertAlmostEqual(second['cpm'],1e6/110)
            self.assertEqual(data['sample_qc'][0]['gene_count_total'],110)
            self.assertEqual(len(data['marker_qc']),20)
            write_outputs(p,data); result=verify(*args,p,expected_gene_count=6)
            self.assertEqual(result['status'],'passed'); print('ARTIFICIAL_VERIFICATION',json.dumps(result))

    def test_changed_source_factor_and_metadata_join_fail(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); args=fixture(p); data=reconstruct(*args,expected_gene_count=6);write_outputs(p,data)
            q=read_rows(args[2]); original=args[2].read_bytes()
            for field,value in [('gene_count_total','999'),('mor_size_factor','0'),('total_count_size_factor','NaN'),
                    ('run','SRR_wrong'),('short_label','D6_A1'),('time','D30')]:
                changed=copy.deepcopy(q);changed[0][field]=value;table(args[2],changed)
                with self.assertRaises(ValueError):reconstruct(*args,expected_gene_count=6)
                with self.assertRaises(AssertionError):verify(*args,p,expected_gene_count=6)
                args[2].write_bytes(original)
            m=read_rows(args[1]);m[0]['characteristics']='Sex: male';table(args[1],m)
            with self.assertRaises(ValueError):reconstruct(*args,expected_gene_count=6)
            with self.assertRaises(AssertionError):verify(*args,p,expected_gene_count=6)

    def test_bad_count_structure_and_gene_order_fail(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);args=fixture(p);data=reconstruct(*args,expected_gene_count=6);write_outputs(p,data)
            source=args[0][SAMPLES[0]]; original=gzip.decompress(source.read_bytes()).decode().splitlines()
            cases=[]
            for bad in ['-1','1.5','NaN','1\textra']:
                lines=original.copy();lines[0]=lines[0].split('\t')[0]+'\t'+bad;cases.append(lines)
            cases.extend([original[:-1],original+[original[0]],list(reversed(original))])
            for lines in cases:
                with gzip.open(source,'wt',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
                with self.assertRaises(ValueError):reconstruct(*args,expected_gene_count=6)
                with self.assertRaises(AssertionError):verify(*args,p,expected_gene_count=6)

    def test_ambiguous_or_changed_annotation_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);args=fixture(p);data=reconstruct(*args,expected_gene_count=6);write_outputs(p,data)
            text=gzip.decompress(args[3].read_bytes()).decode()
            for changed in [text+text.splitlines()[0]+'\n',text.replace('ENSMUSG00000086503.3','ENSMUSG00000086503.4')]:
                with gzip.open(args[3],'wt',encoding='utf-8') as f:f.write(changed)
                with self.assertRaises(ValueError):reconstruct(*args,expected_gene_count=6)
                with self.assertRaises(AssertionError):verify(*args,p,expected_gene_count=6)

    def test_semantic_and_numeric_output_tamper_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);args=fixture(p);data=reconstruct(*args,expected_gene_count=6);write_outputs(p,data)
            for name,field,value in [('marker_qc','recorded_sex','male'),('marker_qc','mor','99'),
                    ('marker_qc','cpm','99'),('marker_qc','log2_cpm_plus1','99'),('marker_qc','raw_zero','False'),
                    ('sample_qc','normalization_origin','refitted'),('annotation','gene_id','wrong')]:
                path=p/(name+'.tsv');original=path.read_bytes();rs=read_rows(path);rs[0][field]=value;table(path,rs)
                with self.assertRaises(AssertionError):verify(*args,p,expected_gene_count=6)
                path.write_bytes(original)


if __name__=='__main__':unittest.main()
