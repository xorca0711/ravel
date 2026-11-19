"""Constructed signal tests. The only binary accepted here is the pinned upstream toy BigWig."""
import argparse
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from m24_reader import GSMS, ROOT, audit_all, audit_interval, read_rows, write_json, write_rows

BINARY = ROOT / "raw_data/naik2017_s3_runtime_v1/test.bw"
PREVIEW = None


class ToyTrack:
    chromsizes={"toy":1000}

    def __init__(self, records, override=None):
        self.records=records
        self.override=override

    def fetch_intervals(self, chrom,start,end,iterator):
        assert iterator is True
        return [(chrom,a,b,v) for a,b,v in self.records if a<end and start<b]

    def fetch(self, chrom,start,end,*,bins,missing,oob):
        assert bins==-1 and np.isnan(missing) and np.isposinf(oob)
        if self.override is not None:
            return np.asarray(self.override)
        arr=np.full(end-start,missing)
        for a,b,v in self.records:
            if a<end and start<b:
                arr[max(a,start)-start:min(b,end)-start]=v
        return arr


def fixture():
    regions=[dict(s2_excel_row=str(i),source_class="Memory" if i<4 else "Resolved",chromosome="toy",
                  start0=str(i*10),end0=str(i*10+4),width_bp="4",s3_D6_log2FoldChange=x)
             for i,x in enumerate([0,0,0,1,0,1,1,1])]
    series=[[0,0,0,8,4,4,4,4], [2,2,2,10,2,2,2,2], [1,1,1,5,5,5,5,5], [5,5,5,13,1,1,1,1]]
    samples=[dict(gsm=g,history=h,replicate=r) for g,h,r in
             [("C1","naive",1),("C2","naive",2),("P1","post_IMQ",1),("P2","post_IMQ",2)]]
    handles={sample["gsm"]:ToyTrack([(i*10,i*10+4,v) for i,v in enumerate(values)]) for sample,values in zip(samples,series)}
    return regions,samples,handles


class ConstructedTests(unittest.TestCase):
    def test_exact_clipped_base_coverage(self):
        result=audit_interval(ToyTrack([(0,3,0),(3,5,4),(5,10,8)]),"toy",1,6)
        self.assertEqual((result["status"],result["explicit_zero_bp"],result["stored_bp"]),("valid",2,5))
        self.assertAlmostEqual(result["mean_cpm"],3.2)
        zero=audit_interval(ToyTrack([(1,6,0)]),"toy",1,6)
        self.assertEqual((zero["mean_cpm"],zero["explicit_zero_bp"]),(0.0,5))

    def test_distinct_coverage_failures(self):
        cases=[
            ([(1,3,0)],None,"absent_bp"),
            ([(1,5,1),(4,6,1)],None,"overlap_bp"),
            ([(1,5,1),(4,6,2)],None,"conflict_bp"),
            ([(1,6,np.nan)],None,"nonfinite_record_bp"),
            ([(1,6,np.inf)],None,"nonfinite_record_bp"),
            ([(1,6,-1)],None,"negative_record_bp"),
            ([(1,6,1)],[1,1,1,1,np.nan],"nonfinite_fetch_stored_bp"),
            ([(1,6,1)],[1,1,1,1,2],"disagreement_bp"),
            ([(1,6,1)],[1,1],"wrong_fetch_length"),
            ([(1,3,1)],[1,1,0,0,0],"disagreement_bp"),
            ([(1,1001,0)],None,"invalid_record"),
        ]
        for records,override,flag in cases:
            with self.subTest(flag=flag):
                result=audit_interval(ToyTrack(records,override),"toy",1,6)
                self.assertEqual((result["status"],result["mean_cpm"]),("held",""))
                self.assertGreater(result[flag],0)
        self.assertEqual(audit_interval(ToyTrack([]),"toy",998,1002)["out_of_bounds"],1)

    def test_coverage_hold_precedes_all_aggregates(self):
        from m24_analysis import finish
        regions,samples,handles=fixture()
        handles["C1"].records=handles["C1"].records[1:]
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            with self.assertRaisesRegex(ValueError,"1 interval-library"):
                audit_all(handles,regions,out)
            audited=read_rows(out/"intervals.tsv")
            self.assertEqual(len(audited),32)
            failed=[r for r in audited if r["status"]=="held"]
            self.assertEqual((failed[0]["gsm"],failed[0]["absent_bp"],failed[0]["mean_cpm"]),("C1","4",""))
            with self.assertRaisesRegex(ValueError,"Coverage hold"):
                finish(regions,samples,out)
            self.assertEqual({p.name for p in out.iterdir()},{"coverage.json","intervals.tsv"})

    def test_equal_region_weight_despite_different_widths(self):
        from m24_analysis import support,summarize
        regions,samples,handles=fixture()
        regions[3].update(width_bp="9",end0="39")
        for track in handles.values():
            a,_,v=track.records[3]
            track.records[3]=(a,a+9,v)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            audit_all(handles,regions,out)
            pools,_,_=summarize(regions,samples,read_rows(out/"intervals.tsv"),support(regions)[0])
            self.assertEqual(next(r for r in pools if r["gsm"]=="C1" and r["method"]=="full_mean")["Memory"],2.0)

    def test_support_weights_ties_and_empty_cells(self):
        from m24_analysis import support
        regions,_,_=fixture()
        weights,design=support(regions)
        self.assertEqual(design["cutpoints"],{"s3_D6_log2FoldChange":[0,.5,1],"width_bp":[4,4,4]})
        self.assertEqual({r["D6_bin"] for r in weights},{2,4})
        self.assertEqual({r["width_bin"] for r in weights},{4})
        self.assertEqual(design["total_overlap_units"],2)
        self.assertEqual(len(design["strata"]),16)
        for cl in ("Memory","Resolved"):
            self.assertAlmostEqual(design["classes"][cl]["regional_Kish_ESS"],3.)
            self.assertAlmostEqual(sum(r["overlap_weight"] for r in weights if r["source_class"]==cl),1.)
        self.assertAlmostEqual(weights[3]["overlap_weight"],.5)
        self.assertAlmostEqual(weights[0]["overlap_weight"],1/6)
        for row in design["balance"]:
            if row["method"]=="overlap_weighted_mean":
                self.assertAlmostEqual(row["difference"],0.)
        for r in regions: r["s3_D6_log2FoldChange"]=float(r["source_class"]=="Memory")
        ws,ds=support(regions)
        self.assertEqual(ds["weighted_status"],"no_common_support")
        self.assertFalse(any(r["overlap_weight"] for r in ws))

    def test_shared_strata_keep_all_members_and_measure_residual_balance(self):
        from m24_analysis import support
        regions,_,_=fixture()
        for r,v in zip(regions,[0,0.1,0.2,8,0.3,5,6,7]):
            r["s3_D6_log2FoldChange"]=v
        weights,design=support(regions)
        self.assertTrue(any(r["overlap_weight"]==0 for r in weights))
        row=next(r for r in design["balance"] if r["method"]=="overlap_weighted_mean" and r["covariate"]=="s3_D6_log2FoldChange")
        self.assertNotAlmostEqual(row["difference"],0.)
        self.assertIsNotNone(row["standardized_difference"])

    def test_reference_disagreement_stops_at_design(self):
        from m24_analysis import support,verify_support_reference
        design=support(fixture()[0])[1]
        table=dict(axes=["s3_D6_log2FoldChange","s3_baseMean","width_bp"],cell_counts=[])
        ref={"acute_covariate_support":dict(pooled_quartile_cuts=design["cutpoints"].copy(),diagnostics=[table])}
        with self.assertRaisesRegex(ValueError,"stratum counts"):
            verify_support_reference(design,ref)
        ref["acute_covariate_support"]["pooled_quartile_cuts"]["width_bp"]=[0,0,0]
        with self.assertRaisesRegex(ValueError,"cutpoints"):
            verify_support_reference(design,ref)

    def test_complete_four_pool_estimands_and_figure(self):
        from m24_analysis import finish
        from PIL import Image
        from pypdf import PdfReader
        regions,samples,handles=fixture()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            audit_all(handles,regions,out)
            finish(regions,samples,out)
            pool=read_rows(out/"pool_summaries.tsv")
            self.assertEqual(len(pool),12)
            self.assertEqual([float(r["gap"]) for r in pool if r["method"]=="full_mean"],[-2,2,-3,6])
            changes={r["method"]:r for r in read_rows(out/"history_changes.tsv")}
            self.assertEqual([float(changes["full_mean"][k]) for k in ("Memory","Resolved","gap")],[1.5,0,1.5])
            self.assertAlmostEqual(float(changes["overlap_weighted_mean"]["gap"]),1.)
            self.assertEqual(float(changes["full_median"]["gap"]),2.)
            cp=[r for r in read_rows(out/"cross_pool.tsv") if r["method"]=="full_mean"]
            self.assertEqual([float(r["gap"]) for r in cp],[-1,-5,8,4])
            self.assertEqual(len(set((r["post_pool"],r["naive_pool"]) for r in cp)),4)
            with Image.open(out/"m24_distal.png") as im:
                self.assertGreater(im.width,1800)
                im.verify()
            self.assertEqual(len(PdfReader(out/"m24_distal.pdf").pages),1)
            if PREVIEW:
                import matplotlib.pyplot as plt
                # Mark the optional review copy as constructed to avoid mistaking it for a measured figure.
                image=plt.imread(out/"m24_distal.png")
                fig,ax=plt.subplots(figsize=(9,7))
                ax.imshow(image)
                ax.axis("off")
                fig.suptitle("Synthetic layout check",fontsize=16)
                fig.savefig(PREVIEW,dpi=105,bbox_inches="tight")
                plt.close(fig)


def binary_fixture():
    import bbi
    with BINARY.open("rb") as stream:
        assert hashlib.file_digest(stream,"sha256").hexdigest()=="cfbf15ba7e9559db9841b246a12a79b51c44b2215137b652dc8f35b100b7ae86"
    with bbi.open(str(BINARY)) as handle:
        complete=audit_interval(handle,"1",0,3)
        sparse=audit_interval(handle,"1",0,4)
        assert complete["status"]=="valid" and complete["stored_bp"]==3
        assert np.isclose(complete["mean_cpm"],.2,rtol=1e-7,atol=0)
        assert (sparse["status"],sparse["stored_bp"],sparse["absent_bp"])==("held",3,1)
        assert sparse["mean_cpm"]==""
    print("Pinned synthetic BigWig: three stored bases reconcile; one absent base triggers hold.")


def synthetic_pipeline():
    """Exercise the actual host-to-reader entrypoint using four copies of one public artificial file."""
    from m24_analysis import run,support
    toy_hash="cfbf15ba7e9559db9841b246a12a79b51c44b2215137b652dc8f35b100b7ae86"
    assert hashlib.sha256(BINARY.read_bytes()).hexdigest()==toy_hash
    with tempfile.TemporaryDirectory(prefix="nk17_constructed_",dir=ROOT/"raw_data") as temp:
        folder=Path(temp)
        paths=[]
        samples=[]
        for i,gsm in enumerate(GSMS):
            dest=folder/f"constructed_{i}.bw"
            shutil.copyfile(BINARY,dest)
            paths.append(dest)
            samples.append(dict(gsm=gsm,history="naive" if i<2 else "post_IMQ",replicate=i%2+1,
                         file_url="https://fixture.invalid/"+dest.name,bytes=dest.stat().st_size,sha256=toy_hash))
        # Nested toy windows allow the real cohort-size guard to run on this 154-covered-base fixture.
        coords=[("1",a,b) for a in range(100,151) for b in range(a+1,152)]
        coords += [("10",a,b) for a in range(200,300) for b in range(a+1,301)]
        rows=[dict(s2_excel_row=i+2,primary=1,distal=1,source_class="Memory" if i<791 else "Resolved",
                   chromosome=c,start0=a,end0=b,width_bp=b-a,s3_D6_log2FoldChange=i%11)
              for i,(c,a,b) in enumerate(coords[:1575])]
        write_rows(folder/"regions.tsv",rows)
        write_rows(folder/"samples.tsv",samples)
        _,design=support(rows)
        ref_cells=[dict(bin=[s["D6_bin"],1,s["width_bin"]],Memory=s["Memory"],Resolved=s["Resolved"]) for s in design["strata"]]
        write_json(folder/"region_qualification.json",{"acute_covariate_support":{
            "pooled_quartile_cuts":design["cutpoints"],"diagnostics":[dict(
                axes=["s3_D6_log2FoldChange","s3_baseMean","width_bp"],cell_counts=ref_cells)]}})
        write_json(folder/"track_structure.json",dict(reader=dict(pybbi="0.4.2",numpy="2.5.5"),
                   tracks={g:{"chromosome_sizes":{"1":195471971,"10":130694993}} for g in GSMS}))
        paths.extend(folder/name for name in ("regions.tsv","samples.tsv","track_structure.json","region_qualification.json"))
        config=folder/"constructed.json"
        write_json(config,{"inputs":[{"path":p.relative_to(ROOT).as_posix()} for p in paths]})
        out=folder/"output"
        out.mkdir()
        run(config,out)
        audit=json.loads((out/"coverage.json").read_text())
        assert audit["complete"]==6300 and audit["held"]==0
        changes=read_rows(out/"history_changes.tsv")
        assert len(changes)==3 and all(float(r[k])==0 for r in changes for k in ("Memory","Resolved","gap"))
        assert all((out/name).stat().st_size>0 for name in ("m24_distal.png","m24_distal.pdf"))
    print("Synthetic normal entrypoint: 6300 exact interval/library audits; all identical-track changes zero; PNG/PDF produced.")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--binary-fixture",action="store_true")
    parser.add_argument("--synthetic-pipeline",action="store_true")
    parser.add_argument("--preview",type=Path)
    args=parser.parse_args()
    if args.binary_fixture:
        binary_fixture()
    elif args.synthetic_pipeline:
        synthetic_pipeline()
    else:
        PREVIEW=args.preview
        unittest.main(argv=[sys.argv[0]])
