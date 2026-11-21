"""List the public inputs and optionally restore missing cached files."""
from pathlib import Path
from urllib.parse import urlencode
import hashlib

import pandas as pd


CACHE = Path("raw_data/nagaraja_jf_external")
BARCODES = {"TCAGTG40NGAT": ("JUN", "HT-SELEX"), "TTTGCC40NTGA": ("JUN", "mHT-SELEX"),
            "TACCCT40NTTA": ("FOXP1", "HT-SELEX"), "TTATGA40NCAG": ("FOXP1", "mHT-SELEX")}
FIELDS = "run_accession,experiment_accession,experiment_alias,sample_alias,experiment_title,library_name,fastq_ftp,fastq_md5,fastq_bytes,read_count"


def report(project):
    return "https://www.ebi.ac.uk/ena/portal/api/filereport?" + urlencode(dict(
        accession=project, result="read_run", fields=FIELDS, format="tsv", limit=0))


def xml(acc):
    return "https://www.ebi.ac.uk/ena/browser/api/xml/" + acc


def fixed_sources():
    anno = "https://raw.githubusercontent.com/zhou-lab/InfiniumAnnotation/v8.6/MM285/MM285."
    geo = "https://ftp.ncbi.nlm.nih.gov/geo/"
    return {"ena.tsv": report("PRJEB9797"), "cycle0.tsv": report("PRJEB20112"),
            "yin-study.xml": xml("PRJEB9797"), "cycle0-study.xml": xml("PRJEB20112"),
            "yin-pmc-bioc.xml": "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC8009048/unicode",
            "colon-pmc-bioc.xml": "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC12873232/unicode",
            "matrix.gz": geo+"series/GSE283nnn/GSE283386/suppl/GSE283386_Betas_all.csv.gz",
            "geo.soft.gz": geo+"series/GSE283nnn/GSE283386/soft/GSE283386_family.soft.gz",
            "manifest.gz": geo+"platforms/GPL30nnn/GPL30650/suppl/GPL30650_MM285.mm10.manifest.tsv.gz",
            "ordering.gz": anno+"ordering.tsv.gz", "mm10.coord.gz": anno+"mm10.coord.tsv.gz"}


def libraries():
    selected = pd.read_csv(CACHE / "ena.tsv", sep="\t")
    selected = selected[selected.sample_alias.str.match(r"^(?:FOXP1_eDBD|JUN_FL)_[1-4]_")]
    starts = pd.read_csv(CACHE / "cycle0.tsv", sep="\t")
    starts = starts[starts.sample_alias.isin(["ZeroCycle_" + bc for bc in BARCODES])]
    assert len(selected) == 16 and len(starts) == 4
    return pd.concat([selected.assign(project="PRJEB9797"), starts.assign(project="PRJEB20112")])


def all_sources():
    result = fixed_sources()
    for r in libraries().itertuples():
        result[r.experiment_accession + ".xml"] = xml(r.experiment_accession)
        result[r.run_accession + ".fastq.gz"] = "https://" + r.fastq_ftp
    return result


def digest(path, alg="sha256"):
    with path.open("rb") as f:
        return hashlib.file_digest(f, alg).hexdigest()


if __name__ == "__main__":
    import requests
    CACHE.mkdir(parents=True, exist_ok=True)
    for listing in [fixed_sources, all_sources]:
        for name, url in listing().items():
            path = CACHE / name
            if not path.exists():
                response = requests.get(url, timeout=(15,180))
                response.raise_for_status()
                path.write_bytes(response.content)
    for r in libraries().itertuples():
        assert digest(CACHE / (r.run_accession + ".fastq.gz"), "md5") == r.fastq_md5
