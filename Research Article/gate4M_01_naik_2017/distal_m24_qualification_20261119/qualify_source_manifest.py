"""Record cross-checked public accessions, acquisition receipts and metadata source identities."""
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREVIOUS = ROOT / "raw_data/naik_distal_step1_20261119"
TRACKS = ROOT / "raw_data/naik_distal_m24_sources_20261119"
SOFT = PREVIOUS / "GSE299177.soft.gz"
RUNS = TRACKS / "GSE299177_run_metadata.tsv"
S1 = PREVIOUS / "Cowley_S1.xlsx"
METHODS_COMMIT = "f2511024b0dcf7be5d47454ee170594d7b79d35b"


def identity(path, source):
    with path.open("rb") as handle:
        sha = hashlib.file_digest(handle, "sha256").hexdigest()
    return dict(path=path.relative_to(ROOT).as_posix(),source=source,sha256=sha,bytes=path.stat().st_size)


def main():
    frozen = json.loads((HERE/"selection_v1.json").read_text())
    gsm_ids = frozen["control"]+frozen["post_IMQ"]
    sections = gzip.open(SOFT,"rt").read().split("^SAMPLE = ")[1:]
    samples = {s.splitlines()[0]:s.split("\n^",1)[0] for s in sections}
    with RUNS.open() as stream:
        runs = list(csv.DictReader(stream,delimiter="\t"))
    wb = openpyxl.load_workbook(S1, read_only=True, data_only=True)
    qc = {row[0]:row[1] for row in list(wb.active.values)[1:]}
    wb.close()
    samples_out, receipts = [], []
    for gsm in gsm_ids:
        block=samples[gsm]
        naive = gsm in frozen["control"]
        rep=(frozen["control"] if naive else frozen["post_IMQ"]).index(gsm)+1
        expected_title = f"Y2_{'Naive' if naive else 'PIMQ'}_ATAC-seq_Rep{rep}"
        s1_name = f"M24_{'Ctrl' if naive else 'IMQ'}_rep{rep}"
        assert f"!Sample_title = {expected_title}\n" in block
        assert all("!Sample_characteristics_ch1 = "+value in block for value in
                   ["tissue: Skin","cell type: Epidermal Stem Cell","genotype: wildtype"])
        treatment = re.search(r"!Sample_characteristics_ch1 = treatment: ([^\n]+)",block)[1]
        assert ("non-treated" in treatment) if naive else ("Imiquimod for 6 consecutive days" in treatment)
        file_url = re.search(r"!Sample_supplementary_file_1 = (\S+)",block)[1].replace("ftp://","https://")
        matches = [r for r in runs if r["experiment_alias"] == gsm+"_r1"]
        assert len(matches)==1
        ena=matches[0]
        assert ena["sample_accession"] in block and ena["experiment_accession"] in block
        assert ena["library_strategy"]=="ATAC-seq" and ena["library_layout"]=="PAIRED"
        assert qc[s1_name] == 2*int(ena["read_count"])
        receipt = json.loads((TRACKS/(gsm+"_receipt.json")).read_text())
        assert receipt["url"] == file_url and receipt["bytes"]==int(receipt["headers"]["Content-Length"])
        assert "GRCm38 (mm10)" in block and "CPM normalized values" in block
        receipts.append(receipt)
        samples_out.append(dict(gsm=gsm,title=expected_title,history="naive" if naive else "post_IMQ",
            time="M24/Y2",replicate=rep,cowley_S1_label=s1_name,biological_unit="pooled EpdSC library",
            published_mice_per_pool="2-3",mouse_IDs="unknown",pairing="unknown",bioSample=ena["sample_accession"],
            experiment=ena["experiment_accession"],run=ena["run_accession"],platform="GPL19057",
            instrument=ena["instrument_model"],layout=ena["library_layout"],ena_read_count=ena["read_count"],
            ena_base_count=ena["base_count"],s1_total_reads=qc[s1_name],assembly="GRCm38/mm10",
            signal="CPM-normalized paired-fragment coverage",file_url=file_url,bytes=receipt["bytes"],sha256=receipt["sha256"]))
    for col in ("gsm","bioSample","experiment","run","sha256"):
        assert len({r[col] for r in samples_out})==4
    with (HERE/"samples.tsv").open("w",encoding="utf8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(samples_out[0]),delimiter="\t",lineterminator="\n")
        writer.writeheader()
        writer.writerows(samples_out)
    pmc="https://pmc-oa-opendata.s3.amazonaws.com/PMC13295011.1/"
    sources=[identity(PREVIOUS/f"Cowley_S{i}.xlsx",pmc+f"NIHMS2170334-supplement-Data_s{i}.xlsx") for i in (1,2,3)]
    gene=ROOT/"raw_data/naik2017_s2_sources"
    gtf_receipt=json.loads((gene/"acquisition_gencode_m9.json").read_text())
    pinned="https://github.com/dpeerlab/persistent-epigenetic-memory/blob/"+METHODS_COMMIT+"/ATAC_preprocessing/"
    sources += [identity(SOFT,"https://ftp.ncbi.nlm.nih.gov/geo/series/GSE299nnn/GSE299177/soft/GSE299177_family.soft.gz"),
        identity(RUNS,"https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1273025&result=read_run&fields="+",".join(runs[0])+"&format=tsv"),
        identity(gene/gtf_receipt["file"],gtf_receipt["url"]),
        identity(ROOT/"raw_data/naik2017_s3_sources/mm10.chrom.sizes","https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.chrom.sizes"),
        identity(PREVIOUS/"PMC13295011.xml",pmc+"PMC13295011.1.xml"),
        identity(PREVIOUS/"s5_bigwig.sh",pinned+"base_scripts/s5_bigwig.sh"),
        identity(PREVIOUS/"Bulk_ATAC_BWA_MACS3peaks_DESeq2.ipynb",pinned+"notebooks/Bulk_ATAC_BWA_MACS3peaks_DESeq2.ipynb"),
        identity(TRACKS/"rtracklayer_RELEASE_3_21_bigWig.R","https://raw.githubusercontent.com/bioc/rtracklayer/RELEASE_3_21/R/bigWig.R"),
        identity(TRACKS/"acquire_m24.py","Local acquisition script, based on prior D180 receipt practice")]
    result=dict(freeze="3027143",file_identity="Hashes computed locally and re-read from disk. The GEO HTTP responses provided length and Last-Modified and no checksum or ETag.",sample_receipts=receipts,metadata_sources=sources)
    (HERE/"source_receipts.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")

if __name__ == "__main__":
    main()
