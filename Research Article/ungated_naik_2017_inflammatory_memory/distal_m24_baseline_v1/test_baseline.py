"""Constructed regional data and one hash-pinned public software fixture only."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from baseline import BRIDGE, CLASSES, CONTROLS, NEW, OLD, ROOT, effects, rank_design, sparse_mean, weighting


class Track:
    chromsizes = {"toy":20}

    def __init__(self, records, raw):
        self.records = records
        self.raw = raw

    def fetch_intervals(self, chrom, start, end, *, iterator):
        assert iterator
        return [("toy",a,b,x) for a,b,x in self.records]

    def fetch(self, chrom, start, end, *, bins, missing, oob):
        assert bins == -1 and np.isnan(missing) and np.isposinf(oob)
        return np.array(self.raw)


def cohort():
    values = [0,1,2,3,4,5,6,8,7,9,10,11,12,13,14,15]
    regions, old, intervals = [], [], []
    samples = [dict(gsm=name, history=history, replicate=i) for name,history,i in
               (("C1","naive",1),("C2","naive",2),("P1","post_IMQ",1),("P2","post_IMQ",2))]
    for j,x in enumerate(values):
        k = CLASSES[int(j>=8)]
        rec = dict(s2_excel_row=str(j),source_class=k,chromosome="toy",start0=j*5,end0=j*5+4,
                   s3_D6_log2FoldChange=1,width_bp=4)
        regions.append(rec)
        old.append(dict(s2_excel_row=str(j),source_class=k,D6_log2FC=1,width_bp=4,D6_bin=4,width_bin=4,
                        overlap_weight=1/8))
        for s,signal in zip(samples, (0,2,x+2,x+4),strict=True):
            intervals.append(rec | dict(gsm=s["gsm"],status="valid",stored_bp=4,fetch_bp=4,absent_bp=0,mean_cpm=signal))
    return np.array(values), regions, old, intervals, samples


class TestBaseline(unittest.TestCase):
    def test_sparse_depth_is_distinct_from_explicit_zero(self):
        tr = Track([(0,3,0.),(4,8,6.)],[0.,0.,np.nan,6.,6.])
        result = sparse_mean(tr,"toy",1,6)
        self.assertEqual(result,dict(stored_bp=4,explicit_zero_bp=2,sparse_zero_bp=1,mean_rpm=2.4))
        self.assertEqual(sparse_mean(Track([], [np.nan]*5),"toy",1,6)["mean_rpm"],0.)

    def test_corrupt_missing_and_io_are_never_zero(self):
        for records, raw in [([(0,4,2),(3,5,2)],[2]*4), ([(1,5,-1)],[-1]*4),
                             ([(1,5,np.nan)],[np.nan]*4), ([(1,4,2)],[2]*4),
                             ([(1,5,2)],[2,2,np.nan,2]), ([(1,5,2)],[2,2,2]),
                             ([(1,21,2)],[2]*4), ([],[np.inf]*4)]:
            with self.subTest(records=records,raw=raw), self.assertRaises(ValueError):
                sparse_mean(Track(records,raw),"toy",1,5)
        with self.assertRaises(ValueError):
            sparse_mean(Track([],[]),"unknown",0,3)
        class Broken(Track):
            def fetch_intervals(self,*args,**kwargs):
                raise OSError("Unreadable primary data")
        with self.assertRaises(OSError):
            sparse_mean(Broken([],[]),"toy",0,3)

    def test_real_reader_artificial_binary(self):
        import bbi
        toy = ROOT/"raw_data/naik2017_s3_runtime_v1/test.bw"
        self.assertEqual(hashlib.sha256(toy.read_bytes()).hexdigest(),
                         "cfbf15ba7e9559db9841b246a12a79b51c44b2215137b652dc8f35b100b7ae86")
        with bbi.open(str(toy)) as tr:
            row = sparse_mean(tr,"1",0,4)
            records = list(tr.fetch_intervals("1",0,4,iterator=True))
            self.assertEqual((row["stored_bp"],row["sparse_zero_bp"]),(3,1))
            self.assertAlmostEqual(row["mean_rpm"],sum((min(b,4)-max(a,0))*v for _,a,b,v in records)/4)
            self.assertEqual(sparse_mean(tr,"1",3,4)["sparse_zero_bp"],1)

    def test_tied_zeros_equal_ranks_and_library_scale(self):
        a = np.array([0.,0.,4.,8.])
        ranks, combined, qc = rank_design(np.stack([a,a*2,a*100,a]))
        np.testing.assert_equal(ranks,np.tile([.25,.25,.625,.875],(4,1)))
        np.testing.assert_equal(combined,ranks[0])
        self.assertEqual(qc["libraries"][CONTROLS[0]]["zero_regions"],2)
        self.assertEqual(len(qc["correlations"]),6)
        _, _, qc = rank_design(np.stack([a,a,a,np.zeros_like(a)]))
        self.assertEqual(qc["status"],"unresolved_constant_rank")
        b = np.arange(4)
        _, combined, qc = rank_design(np.stack([b,b[::-1],b,b[::-1]]))
        self.assertEqual(len(set(combined)),1)
        self.assertEqual(qc["status"],"unresolved_constant_rank")

    def test_changed_target_and_effect_decomposition(self):
        x, regions, old, late, samples = cohort()
        ranks, consensus, _ = rank_design(np.stack([x,2*x,3*x,4*x]))
        rows, info = weighting(regions,old,ranks,consensus)
        self.assertEqual((len(info["strata"]),info["shared_three_way_cells"],info["overlap_units"]),(64,2,2))
        self.assertEqual(info["shared_baseline_bins"],[2,3])
        for k in CLASSES:
            self.assertEqual(info["classes"][k]["old_mass_retained"],.5)
            self.assertAlmostEqual(info["classes"][k]["weight_diagnostics"][NEW]["regional_ESS"],3.)
        expected = [dict(method="overlap_weighted_mean",Memory=5.625,Resolved=13.375,gap=-7.75)]
        pools,changes,pairs,decomp = effects(regions,samples,late,rows,expected)
        self.assertEqual((len(pools),len(changes),len(pairs)),(12,3,12))
        for r, value in zip(changes,[-7.75,-3.5,-2.],strict=True):
            self.assertAlmostEqual(r["gap"],value)
        self.assertAlmostEqual(decomp["gap"]["support_restriction"],4.25)
        self.assertAlmostEqual(decomp["gap"]["redistribution"],1.5)
        self.assertAlmostEqual(decomp["gap"]["total"],5.75)
        self.assertEqual(len(info["balance"]),28)
        self.assertEqual({r["s2_excel_row"] for r in rows if r[BRIDGE] != 0},{str(i) for i in (4,5,6,7,8,9,10,11)})
        for bad in [late[:-1],late+[late[0]],late[:-1]+[late[-1] | {"source_class":"Memory"}]]:
            with self.assertRaises(ValueError):
                effects(regions,samples,bad,rows,expected)

    def test_synthetic_entrypoint_and_source_hold(self):
        import bbi
        from baseline import run
        from m24_analysis import support
        from m24_reader import GSMS, read_rows, write_json, write_rows
        toy = ROOT/"raw_data/naik2017_s3_runtime_v1/test.bw"
        with tempfile.TemporaryDirectory(dir=ROOT/"raw_data") as tmp:
            path = Path(tmp)
            with bbi.open(str(toy)) as track:
                header = dict(chromosomes=track.chromsizes,header_bases_covered=track.info["summary"]["basesCovered"])
            sources = []
            digest = hashlib.sha256(toy.read_bytes()).hexdigest()
            for i,s in enumerate(CONTROLS):
                copy = path/(s+".bw")
                shutil.copyfile(toy,copy)
                sources.append(dict(srx=s,gsm=f"toy{i}",bytes=copy.stat().st_size,sha256=digest,**header))
            write_json(path/"SOURCES_V1.json",{"libraries":sources})
            regions = [dict(s2_excel_row=str(i), source_class=CLASSES[int(i % 2 != 0 and i < 1568)],
                            primary="1",distal="1",chromosome="1",start0="0",end0=str(i+4),width_bp=str(i+4),
                            s3_D6_log2FoldChange="1") for i in range(1575)]
            samples = [dict(gsm=s,history="naive" if i<2 else "post_IMQ",replicate=i%2+1) for i,s in enumerate(GSMS)]
            write_rows(path/"regions.tsv",regions)
            write_rows(path/"samples.tsv",samples)
            weights,_ = support(regions)
            write_rows(path/"region_weights.tsv",weights)
            write_rows(path/"intervals.tsv",[r | dict(gsm=s,stored_bp=r["width_bp"],fetch_bp=r["width_bp"],absent_bp=0,
                       status="valid",mean_cpm=0.) for r in regions for s in GSMS])
            write_rows(path/"history_changes.tsv",[dict(method="overlap_weighted_mean",Memory=0,Resolved=0,gap=0)])
            contract = path/"synthetic_contract.json"
            write_json(contract, {"inputs":[dict(path=str(f)) for f in path.iterdir()]})
            out = path/"complete"
            out.mkdir()
            subprocess.run([sys.executable,"-B",str(Path(__file__).with_name("baseline.py")),
                            "--contract",str(contract),"--output",str(out)],check=True,timeout=90)
            self.assertEqual(len(read_rows(out/"baseline_intervals.tsv")),6300)
            self.assertEqual(len(read_rows(out/"cross_pool.tsv")),12)
            self.assertEqual([float(r["gap"]) for r in read_rows(out/"history_changes.tsv")],[0.,0.,0.])
            broken = path/(CONTROLS[0]+".bw")
            broken.write_bytes(b"invalid synthetic source")
            out = path/"held"
            out.mkdir()
            with self.assertRaisesRegex(ValueError,"Incomplete D6"):
                run(contract,out)
            self.assertEqual(json.loads((out/"coverage.json").read_bytes())["libraries"][CONTROLS[0]]["status"],"held")
            self.assertFalse((out/"rank_qc.json").exists())
            self.assertFalse((out/"history_changes.tsv").exists())

    def test_disjoint_or_single_shared_bin_holds(self):
        x, regions, old, _, _ = cohort()
        for vals, count in [(np.arange(16),0),(np.array([0]*7+[1]+[1]*7+[2]),1)]:
            ranks, consensus, _ = rank_design(np.tile(vals,(4,1)))
            rows, info = weighting(regions,old,ranks,consensus)
            self.assertEqual(len(info["shared_baseline_bins"]),count)
            self.assertEqual(info["status"],"insufficient_shared_baseline_support")
            self.assertTrue(all(r[OLD]>0 for r in rows))


if __name__ == "__main__":
    unittest.main()
