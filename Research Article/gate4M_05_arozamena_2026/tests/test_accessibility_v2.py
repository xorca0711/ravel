import gzip,sys,tempfile,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import accessibility_core_v2 as a

class AccessibilityTests(unittest.TestCase):
    def test_strand_conversion_and_adjacent_union(self):
        self.assertEqual(a.tss0(11,80,'+'),10);self.assertEqual(a.tss0(11,80,'-'),79)
        self.assertEqual(a.merge_intervals([(10,20),(0,10),(30,40),(15,21)]),[[0,21],[30,40]])
        self.assertFalse(a.overlap_once(20,30,[[10,20],[30,40]]));self.assertTrue(a.overlap_once(19,31,[[10,20],[30,40]]))
    def test_basic_selection_and_recorded_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'tiny.gtf.gz';gid=a.TARGETS['Cd74'];src={'Cd74':[dict(stable_id=gid,symbol='Cd74',chrom='chr1',start=49,end=50) for _ in range(3)]}
            def write(basic):
                lines=['##description GRCm39 M33',f'chr1\tx\tgene\t1\t10000\t.\t+\t.\tgene_id "{gid}.1"; gene_name "Cd74";',f'chr1\tx\ttranscript\t50\t1000\t.\t+\t.\tgene_id "{gid}.1"; gene_name "Cd74"; transcript_id "t1";'+(' tag "basic";' if basic else ''),f'chr1\tx\ttranscript\t5000\t6000\t.\t+\t.\tgene_id "{gid}.1"; gene_name "Cd74"; transcript_id "t2";']
                with gzip.open(path,'wt') as f:f.write('\n'.join(lines)+'\n')
            write(True);r=a.read_regions(path,src)[0]['Cd74'];self.assertEqual(r['regions']['tss_2kb_union'],[[0,2049]]);self.assertFalse(r['fallback_all_transcripts']);self.assertEqual(r['regions']['gene_body'],[[0,10000]])
            write(False);r=a.read_regions(path,src)[0]['Cd74'];self.assertTrue(r['fallback_all_transcripts']);self.assertEqual(r['selected_tss_0based'],[49,4999])
    def regions(self):
        return {t:dict(status='qualified',chrom='chr1',regions={'tss_2kb_union':[[10,20],[25,35]],'gene_body':[[0,40]]}) for t in a.TARGETS}
    def fragment_file(self,td,text):
        p=Path(td)/'tiny.tsv.gz'
        with gzip.open(p,'wt') as f:f.write('# id=fixture\n'+text)
        return p
    def test_readsupport_excluded_double_overlap_counts_once(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fragment_file(td,'chr1\t15\t30\tAAAA-1\t7\t+\nchr1\t40\t50\tAAAA-1\t2\t-\nchrM\t10\t20\tAAAA-1\t5\t+\n')
            depth,counts,d,_=a.count_fragments(p,['AAAA-1'],self.regions(),{'id':'fixture'})
            self.assertEqual(depth['strand_records'].tolist(),[2]);self.assertEqual(counts['strand_records'][0,0].tolist(),[1,1]);self.assertEqual(d['noncanonical_rows'],1)
    def test_exact_allowlist_and_zero_fragment_barcodes(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fragment_file(td,'chr1\t1\t12\tAAAA-2\t1\t+\nchr1\t15\t30\tCCCC-1\t1\t+\n')
            depth,_,d,_=a.count_fragments(p,['AAAA-1','CCCC-1'],self.regions(),{'id':'fixture'})
            self.assertEqual(depth['strand_records'].tolist(),[0,1]);self.assertEqual(d['canonical_nonallowlisted_rows'],1);self.assertEqual(d['n_zero_nuclear_fragment_barcodes'],1)
    def test_same_strand_duplicate_despite_changed_readsupport_stops(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fragment_file(td,'chr1\t15\t30\tAAAA-1\t1\t+\nchr1\t15\t30\tAAAA-1\t9\t+\n')
            with self.assertRaises(a.FragmentFailure) as caught:a.count_fragments(p,['AAAA-1'],self.regions(),{'id':'fixture'})
            self.assertIn('Duplicate',str(caught.exception));self.assertFalse(caught.exception.details['endpoints_released'])
    def test_malformed_unsorted_or_bad_header_stops(self):
        for text in ['chr1\t15\t15\tAAAA-1\t1\t+\n','chr1\t15\t30\tAAAA-1\t1\t?\n','chr1\t15\t30\tAAAA-1\t0\t+\n','chr1\t15\t30\tAAAA-1\t1\t+\nchr1\t10\t20\tAAAA-1\t1\t+\n']:
            with tempfile.TemporaryDirectory() as td:
                with self.assertRaises(a.FragmentFailure):a.count_fragments(self.fragment_file(td,text),['AAAA-1'],self.regions(),{'id':'fixture'})
    def test_truncated_gzip_is_not_released(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fragment_file(td,'chr1\t15\t30\tAAAA-1\t1\t+\n');p.write_bytes(p.read_bytes()[:-6])
            with self.assertRaises(a.FragmentFailure):a.count_fragments(p,['AAAA-1'],self.regions(),{'id':'fixture'})
    def test_weighting_and_zero_depth(self):
        r=a.aggregate(np.array([9,1,0]),np.array([10,100,0]),np.array([True]*3));self.assertEqual(r['n'],2);self.assertAlmostEqual(r['pooled_cpm'],1e6*10/110);self.assertAlmostEqual(r['equal_cpm'],455000)
        self.assertIsNone(a.aggregate(np.array([0]),np.array([0]),np.array([True]))['pooled_log'])
    def test_rna_reuse_identical_vs_reduced_population(self):
        counts=np.array([9,1]);depth=np.array([10,100]);original=a.aggregate(counts,depth,np.array([True,True]));same=a.aggregate(counts,depth,np.array([True,True]));reduced=a.aggregate(counts,depth,np.array([False,True]))
        self.assertEqual(original,same);self.assertEqual(reduced['n'],1);self.assertNotEqual(original['pooled_log'],reduced['pooled_log']);self.assertEqual(reduced['pooled_log'],reduced['equal_log'])

    def test_opposite_strand_pair_both_definitions_and_denominators(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fragment_file(td,'chr1\t15\t30\tAAAA-1\t1\t+\nchr1\t15\t30\tAAAA-1\t9\t-\n')
            depth,counts,d,collisions=a.count_fragments(p,['AAAA-1'],self.regions(),{'id':'fixture'})
            self.assertEqual(depth['strand_records'].tolist(),[2]);self.assertEqual(depth['coordinate_groups'].tolist(),[1])
            self.assertEqual(counts['strand_records'][0,0].tolist(),[2,2]);self.assertEqual(counts['coordinate_groups'][0,0].tolist(),[1,1])
            self.assertEqual(d['canonical_allowlisted_opposite_strand_groups'],1);self.assertTrue(d['positive_sets_agree_between_definitions'])
            self.assertEqual(d['collision_locus_regions'][0]['allowlisted_groups'],1);self.assertEqual(collisions['AAAA-1']['canonical_groups'],1)
    def test_nonadjacent_opposite_strands_and_exclusions(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fragment_file(td,'chr1\t15\t30\tAAAA-1\t1\t-\nchr1\t15\t31\tCCCC-1\t1\t+\nchr1\t15\t30\tAAAA-1\t2\t+\nchrM\t5\t8\tGGGG-1\t1\t+\nchrM\t5\t8\tGGGG-1\t1\t-\n')
            depth,counts,d,collisions=a.count_fragments(p,['CCCC-1'],self.regions(),{'id':'fixture'})
            self.assertEqual(depth['coordinate_groups'].tolist(),[1]);self.assertEqual(d['opposite_strand_coordinate_groups'],2)
            self.assertEqual(d['canonical_allowlisted_opposite_strand_groups'],0);self.assertEqual(d['noncanonical_opposite_strand_groups'],1)
            self.assertEqual(d['collision_locus_regions'][0]['all_barcode_groups'],1);self.assertEqual(d['collision_locus_regions'][0]['allowlisted_groups'],0)
    def test_header_contig_and_barcode_rejections(self):
        examples=[('chr1\t1\t2\tAAAA-1\t1\t+\n',{'id':'wrong'}),('chr1\t1\t2\tNNNN-1\t1\t+\n',{'id':'fixture'}),('chr1\t1\t2\tAAAA-1\t1\t+\nchr2\t1\t2\tAAAA-1\t1\t+\nchr1\t3\t4\tAAAA-1\t1\t+\n',{'id':'fixture'})]
        for text,header in examples:
            with tempfile.TemporaryDirectory() as td:
                with self.assertRaises(a.FragmentFailure):a.count_fragments(self.fragment_file(td,text),['AAAA-1'],self.regions(),header)

if __name__=='__main__':unittest.main()

