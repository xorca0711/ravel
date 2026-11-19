"""Constructed-source tests; no actual D180 research-window values are read."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

import s6c_proxy_v1 as main
import s6c_reader_v1 as reader
import s6c_verify_v1 as verify
from s3_rank_v1 import analyze as old_analyze


def fixture():
    entries=[(name,gene,anchor) for name,gene,anchor in main.ANCHORS]
    entries += [('Toy'+str(i),'TOY'+str(i),f'chr1:{5000+i*10000}') for i in range(35)]
    windows=[];mappings=[]
    for flank in [1000,2000]:
        for name,gene,anchor in entries:
            chrom,pos=anchor.split(':');pos=int(pos);key=f'{flank}:{chrom}:{pos-flank}-{pos+flank}'
            windows.append(dict(window_id=key,anchor_id=anchor,flank=flank,chrom=chrom,start=pos-flank,end=pos+flank,clipped=False))
            mappings.append(dict(gene_id=gene,gene_name=name,gene_type='protein_coding',strand='+',tss=pos,window_id=key,anchor_id=anchor,flank=flank))
        alias=dict(mappings[-1]);alias.update(gene_id='TOY_ALIAS',gene_name='Alias');mappings.append(alias)
    windows=pd.DataFrame(windows).sort_values(['flank','chrom','start']).reset_index(drop=True)
    mappings=pd.DataFrame(mappings);old_signal=[];signal=[]
    for i,gsm in enumerate(main.OLD+main.NEW):
        for pos,w in enumerate(windows.itertuples(index=False)):
            value=float((pos*(i+3)+i*5)%13)
            if pos%40 < 2 or (i>=8 and pos%(i-5)==0):value=0.
            row=dict(window_id=w.window_id,gsm=gsm,mean_signal=value,encoded_zero_bases=2*w.flank if value==0 else 0)
            (old_signal if i<8 else signal).append(row)
    old,_,_=old_analyze(windows,pd.DataFrame(old_signal))
    return windows,mappings,old,pd.DataFrame(signal),{c:200000000 for c in ['chr1','chr2','chr9']}


def write_fixture(output):
    windows,mappings,old,signal,sizes=fixture()
    anchors,chosen=main.qualify_universe(windows,mappings,old,sizes,40,41)
    frame,diag,summary=main.analyze(windows,signal,old)
    for name,data in [('windows.tsv',windows),('gene_window_map.tsv.gz',mappings),('old.tsv.gz',old),('window_signal.tsv.gz',signal),
        ('window_effects.tsv.gz',frame),('library_diagnostics.tsv',diag),('verification_windows.tsv',chosen)]:main.tsv(output/name,data)
    main.save(output/'summary.json',summary);main.save(output/'anchor_manifest.json',anchors)
    indexed=frame.set_index('window_id',drop=False)
    cases=pd.DataFrame([dict(indexed.loc[a['window_id']].to_dict(),**{k:v for k,v in a.items() if k not in indexed.columns}) for a in anchors])
    main.tsv(output/'fixed_anchors.tsv',cases)
    return windows,mappings,old,signal,frame,cases


class Tests(unittest.TestCase):
    def test_full_fixture_and_tampered_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);w,m,o,s,frame,cases=write_fixture(p)
            check=verify.verify_data(p,verify.rows(p/'windows.tsv'),verify.rows(p/'gene_window_map.tsv.gz'),verify.rows(p/'old.tsv.gz'),40,41)
            self.assertGreater(check.count,10000)
            print(json.dumps(dict(artificial_checks=check.count,maximum_scaled_error=check.maximum)),flush=True)
            summary=json.loads((p/'summary.json').read_text());summary['by_flank']['1000']['comparisons']['D30']['fraction_absolute_smaller']+=.1
            main.save(p/'summary.json',summary)
            with self.assertRaises(AssertionError):verify.verify_data(p,verify.rows(p/'windows.tsv'),verify.rows(p/'gene_window_map.tsv.gz'),verify.rows(p/'old.tsv.gz'),40,41)

    def test_exact_universe_mapping_and_fixed_anchor_failures(self):
        w,m,o,s,sizes=fixture()
        for bad in ['coordinate','missing_window','missing_mapping','wrong_gene','wrong_anchor','clipped']:
            ww,mm,oo=w.copy(),m.copy(),o.copy()
            if bad=='coordinate':ww.loc[0,'end']+=1
            if bad=='missing_window':ww=ww.iloc[:-1]
            if bad=='missing_mapping':mm=mm.iloc[:-1]
            if bad=='wrong_gene':mm.loc[mm.gene_name=='Aim2','gene_id']='VERSION_CHANGED'
            if bad=='wrong_anchor':mm.loc[mm.gene_name=='Aim2','anchor_id']='chr1:999999'
            if bad=='clipped':ww.loc[0,'clipped']=True
            with self.subTest(bad=bad),self.assertRaises((AssertionError,KeyError)):
                main.qualify_universe(ww,mm,oo,sizes,40,41)

    def test_missing_duplicated_or_nonfinite_signal(self):
        w,m,o,s,sizes=fixture()
        for bad in ['missing','duplicate','wrong_gsm','nan','fractional_zero','too_many_zeros']:
            ss=s.copy()
            if bad=='missing':ss=ss.iloc[:-1]
            if bad=='duplicate':ss=pd.concat([ss.iloc[:-1],ss.iloc[[0]]],ignore_index=True)
            if bad=='wrong_gsm':ss.loc[0,'gsm']='OTHER'
            if bad=='nan':ss.loc[0,'mean_signal']=np.nan
            if bad=='fractional_zero':ss['encoded_zero_bases']=ss.encoded_zero_bases.astype(float);ss.loc[0,'encoded_zero_bases']=.5
            if bad=='too_many_zeros':ss.loc[0,'encoded_zero_bases']=5000
            with self.subTest(bad=bad),self.assertRaises((AssertionError,KeyError)):main.analyze(w,ss,o)

    def test_rank_ties_local_zero_and_range_semantics(self):
        np.testing.assert_allclose(main.percentile_points([0,0,2,4]),[100/6,100/6,200/3,100])
        np.testing.assert_allclose(main.percentile_points([0,0,0,0]),[50]*4)
        w,m,o,s,sizes=fixture();frame,diag,summary=main.analyze(w,s,o)
        all_zero=np.logical_and.reduce([frame[g+'__mean_zero'] for g in main.NEW])
        self.assertTrue(all_zero.any());self.assertTrue((~frame.loc[all_zero,'D180_computational_zero']).any())
        self.assertTrue((frame.D180_range_touches_zero & ~frame.D180_computational_zero).any())
        for flank in [1000,2000]:
            f=frame.loc[frame.flank==flank]
            self.assertAlmostEqual(f.D180_delta.mean(),0)
            for gsm in main.NEW:self.assertAlmostEqual(f[gsm+'__percentile'].mean(),50)
        bad=frame.copy();bad.loc[0,main.NEW[0]+'__mean_zero']=not bool(bad.loc[0,main.NEW[0]+'__mean_zero'])
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);write_fixture(p);main.tsv(p/'window_effects.tsv.gz',bad)
            with self.assertRaises(AssertionError):verify.verify_data(p,verify.rows(p/'windows.tsv'),verify.rows(p/'gene_window_map.tsv.gz'),verify.rows(p/'old.tsv.gz'),40,41)

    def test_qualification_fails_before_any_fetch(self):
        class Backend:
            def __init__(self,bad):self.bad=bad;self.fetches=0
            def is_bigwig(self,path):return True
            def chromsizes(self,path):return {'chr1':99 if self.bad and path.endswith('3') else 100,'extra':7}
            def info(self,path):return {'version':4}
            def zooms(self,path):return []
            def open(self,path):
                parent=self
                class Handle:
                    def __enter__(self):return self
                    def __exit__(self,*args):pass
                    def fetch(self,chrom,start,end,**kwargs):parent.fetches+=1;return np.zeros(end-start)
                return Handle()
        sources=[dict(gsm=g,path=str(i)) for i,g in enumerate(main.NEW)]
        windows=[dict(window_id='one',chrom='chr1',start='10',end='14')]
        old=dict(tracks=[dict(chromosomes={'chr1':100,'extra':7})])
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);backend=Backend(True)
            with self.assertRaises(AssertionError):reader.qualify_then_extract(p,sources,windows,{'chr1':100},Path('.'),backend,old,lambda:{},False)
            self.assertEqual(backend.fetches,0);self.assertFalse((p/'window_signal.tsv.gz').exists())
            self.assertEqual(json.loads((p/'qualification.json').read_text())['status'],'failed_before_extraction')
            backend=Backend(False);reader.qualify_then_extract(p,sources,windows,{'chr1':100},Path('.'),backend,old,lambda:{},False)
            self.assertEqual(backend.fetches,4)
            self.assertEqual(len(reader.rows(p/'window_signal.tsv.gz')),4)

    def test_full_coverage_zero_array_rules(self):
        self.assertEqual(reader.array_summary(np.array([0.,2.,0.,2.]),4),(1.,2))
        for values,length in [(np.array([0.,np.nan]),2),(np.array([0.,np.inf]),2),(np.array([0.]),2)]:
            with self.assertRaises(ValueError):reader.array_summary(values,length)

    def test_source_membership_and_metadata_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);sources=[];metadata=[];inputs=[]
            for i,gsm in enumerate(main.NEW):
                group='PI' if i<2 else 'Ctrl';name=f'{gsm}_{group}_D180_mm10_ATAC_Rep_{i%2+1}_.bw'
                path='raw_data/naik2017_s6_d180_sources_v1/'+name;target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(b'artificial');digest=main.sha(target)
                sources.append(dict(gsm=gsm,path=path,url=f'https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/{gsm}/suppl/{name}',
                    sha256=digest,bytes=10,expected_bytes=10,exit_code=0,status='downloaded_size_and_hash_recorded'))
                inputs.append(dict(path=path,sha256=digest))
                metadata.append(dict(gsm=gsm,assay='ATAC-seq',day_label='180',history_label='prior_inflammation' if i<2 else 'control',
                    wound_hour_label='',label_conflicts='',wound_status_label='no wound stated in selected metadata',
                    runs='SRR'+str(5657347+i),biosamples=['SAMN07203513','SAMN07203512','SAMN07203511','SAMN07203514'][i],
                    instrument_models='Illumina HiSeq 2500',library_layouts='PAIRED',organism='Mus musculus',source_compartment='Skin',replicate_label=str(i%2+1)))
            manifest=dict(all_downloaded=True,files=sources);crosswalk=pd.DataFrame(metadata);contract=dict(inputs=inputs)
            self.assertEqual(len(main.qualify_sources(manifest,crosswalk,contract,root)['files']),4)
            for bad in ['duplicate','missing','run','history','platform','hash','length']:
                mm=copy.deepcopy(manifest);cc=crosswalk.copy()
                if bad=='duplicate':mm['files'][-1]=mm['files'][0]
                if bad=='missing':mm['files'].pop()
                if bad=='run':cc.loc[0,'runs']='SRR_OTHER'
                if bad=='history':cc.loc[0,'history_label']='control'
                if bad=='platform':cc.loc[0,'instrument_models']='Illumina HiSeq 4000'
                if bad=='hash':mm['files'][0]['sha256']='0'*64
                if bad=='length':mm['files'][0]['bytes']=11
                with self.subTest(bad=bad),self.assertRaises(AssertionError):main.qualify_sources(mm,cc,contract,root)


if __name__=='__main__':unittest.main()
