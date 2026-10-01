"""Check saved follow-up evidence and assemble an eleven-figure PDF; no refits."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import false_discovery_control
from pypdf import PdfReader, PdfWriter
from PIL import Image

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
RUN=HERE/"runs/followup_v1"


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    checks=[]
    specpath=HERE/"config/Nb3_followup_v1.json";spec=json.loads(specpath.read_text())
    record=json.loads((RUN/"run_record.json").read_text())
    assert record["config_sha256"]==sha(specpath)
    checks.append("follow-up contract hash")
    for path,digest in spec["inputs"].items():
        assert sha(ROOT/path)==digest,path
        checks.append("frozen input: "+path)
    for path,digest in record["script_sha256"].items():
        assert sha(HERE/"scripts"/path)==digest,path
        checks.append("analysis script: "+path)
    for path,digest in record["output_sha256"].items():
        assert sha(RUN/path)==digest,path
        checks.append("analysis output: "+path)
    # Independent BH recomputation against the recorded cross-species family.
    h=pd.read_csv(RUN/"hallmark_camera.tsv",sep="\t")
    for cor,frame in h.groupby("intergene_correlation"):
        assert len(frame)==1486
        assert np.allclose(false_discovery_control(frame.PValue.to_numpy()),frame.FDR_global,rtol=1e-10,atol=1e-14)
        checks.append(f"independent global BH: correlation {cor}")
    coverage=pd.read_csv(RUN/"hallmark_coverage.tsv",sep="\t")
    assert len(coverage)==1600 and int(coverage.eligible.sum())==1486
    assert (coverage.eligible==((coverage.mapped_genes>=15)&(coverage.coverage_fraction>=.5))).all()
    checks.append("all planned Hallmark coverage gates")
    # Single-plate arithmetic from saved CPM, independently of the OLS implementation.
    sens=pd.read_csv(RUN/"panel_sensitivities.tsv",sep="\t")
    for species,program,target in [("mouse","AT2_figure3","NKX21"),("human","chemokines_figure4","NKX21"),("human","wound_figure4","NKX21"),("mouse","transition_figure3","SLC34A2")]:
        norm=pd.read_csv(HERE/f"runs/R2_v1/{species}_normalization.tsv",sep="\t")
        cpm=pd.read_csv(ROOT/f"raw_data/GSE307112/Nb3_v1/{species}_selected_symbol_cpm.tsv",sep="\t").set_index("gene")
        nt=norm[norm.target==target];assert nt.plate.nunique()==1
        plate=nt.plate.iloc[0]
        selected=sens[(sens.species==species)&(sens.program==program)&(sens.target==target)&(sens.status=="technical_descriptive")]
        for r in selected.itertuples():
            genes=list(spec["programs"][species][program])
            controls=spec["B1"]["control_variants"].get(r.variant,["TIGIT","TDTOMATO"])
            target_libraries=list(nt.library)
            if r.variant=="omit_gene":genes.remove(r.omitted)
            if r.variant=="omit_target_well":target_libraries.remove(r.omitted)
            refs=norm[(norm.plate==plate)&norm.target.isin(controls)].library
            tv=np.log2(cpm.loc[genes,target_libraries].to_numpy()+.5).mean()
            cv=np.log2(cpm.loc[genes,refs].to_numpy()+.5).mean()
            assert np.isclose(tv-cv,r.effect,atol=1e-9),str(r)
            checks.append(f"independent mean contrast: {species}/{program}/{target}/{r.variant}/{r.omitted}")
    # Frisch-Waugh-Lovell recovery of NKX21 depth coefficients by residualizing
    # outcome and exposure separately against nuisance variables.
    paired=pd.read_csv(HERE/"runs/R4_v1/paired_library_QC.tsv",sep="\t")
    dep=pd.read_csv(RUN/"paired_depth_effects.tsv",sep="\t")
    for species,program in [("mouse","AT2_figure3"),("human","chemokines_figure4")]:
        scores=pd.read_csv(HERE/f"runs/R2_v1/{species}_panel_scores.tsv",sep="\t")
        d=paired.merge(scores[scores.program==program][["library","score"]],on="library",validate="one_to_one")
        plate=d.loc[d.target=="NKX21","plate"].unique();d=d[(d.target=="NKX21")|(d.target.isin(["TIGIT","TDTOMATO"])&d.plate.isin(plate))]
        nuisance=np.column_stack([np.ones(len(d)),pd.get_dummies(d.plate,drop_first=True).to_numpy(dtype=float),np.log2(d[["total_reads_mouse","total_reads_human"]].to_numpy())])
        y=d.score.to_numpy();z=(d.target=="NKX21").to_numpy(dtype=float)
        yr=y-nuisance@np.linalg.lstsq(nuisance,y,rcond=None)[0]
        zr=z-nuisance@np.linalg.lstsq(nuisance,z,rcond=None)[0]
        value=zr@yr/(zr@zr)
        expected=dep[(dep.species==species)&(dep.target=="NKX21")&(dep.variant=="paired_depth")].effect.iloc[0]
        assert np.isclose(value,expected,atol=1e-9)
        checks.append("FWL adjusted coefficient: "+species)
    figures=[]
    for directory,script in [(HERE/"figures/publication_v1","13_publication_figures.py"),(HERE/"figures/followup_v1","15_followup_figures.py")]:
        manifest=json.loads((directory/"render_record.json").read_text())
        assert manifest["script_sha256"]==sha(HERE/"scripts"/script)
        checks.append("figure script: "+script)
        for path,digest in manifest["inputs"].items():
            assert sha(ROOT/path)==digest,path
            checks.append("figure input: "+path)
        for path,digest in manifest["outputs"].items():
            assert sha(directory/path)==digest,path
            checks.append("figure output: "+path)
        for png in directory.glob("Nb3_[FS]*.png"):
            im=Image.open(png);assert im.width==2160 and im.height>=1500
            pdf=PdfReader(png.with_suffix(".pdf"));assert len(pdf.pages)==1
            assert abs(float(pdf.pages[0].mediabox.width)-518.4)<.01
            figures.append(png.with_suffix(".pdf"))
            checks.append("figure geometry: "+png.name)
    assert len(figures)==11
    figures.sort(key=lambda x:x.stem)
    writer=PdfWriter()
    for f in figures:writer.add_page(PdfReader(f).pages[0])
    writer.add_metadata({"/Title":"Nb3: reproduction, extensions and follow-up figures", "/Author":"Nb3 analysis"})
    atlas=HERE/"figures/Nb3_complete_figure_atlas.pdf"
    import io
    buffer=io.BytesIO();writer.write(buffer);content=buffer.getvalue()
    if atlas.exists():assert atlas.read_bytes()==content,"Existing atlas differs; preserve it and use a new version"
    else:atlas.write_bytes(content)
    assert len(PdfReader(atlas).pages)==11
    checks.append("eleven-page ordered figure atlas")
    result={"status":"PASS","checks":len(checks),"details":checks,"script_sha256":sha(Path(__file__)),
        "atlas":{"path":str(atlas.relative_to(HERE)).replace("\\","/"),"sha256":sha(atlas),"pages":11},
        "limits":"Verifies arithmetic, coverage, provenance and exports; does not establish source S5 agreement or independent biology. Visual review recorded separately."}
    report=HERE/"reports/Nb3_followup_verification.json"
    if report.exists():raise SystemExit("Refusing to overwrite verification record")
    report.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"checks":len(checks),"figure_pages":11}))


if __name__=="__main__":main()
