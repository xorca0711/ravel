"""Requantify the three experiment 1 FASTQs with explicit release-84 inputs."""
import argparse
import gzip
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

RAW = Path("raw_data/roberts_2017/requant")
SAMPLES = (
    ("GSM2462968", "SRR5186277"),
    ("GSM2462969", "SRR5186278"),
    ("GSM2462970", "SRR5186279"),
)


def run_checked(argv):
    return subprocess.run(argv, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", choices=("ena", "sra"), required=True)
    parser.add_argument("--gsm", choices=tuple(gsm for gsm, _ in SAMPLES), required=True)
    args = parser.parse_args()
    cutadapt = shutil.which("cutadapt")
    kallisto = RAW / "kallisto-0.43.1"
    if not cutadapt or subprocess.check_output([cutadapt, "--version"], text=True).strip() != "4.9":
        raise RuntimeError("cutadapt 4.9 is required")
    if "version 0.43.1" not in subprocess.check_output([kallisto, "version"], text=True):
        raise RuntimeError("Kallisto 0.43.1 is required")
    with TemporaryDirectory(prefix="scratch-", dir=RAW) as scratch:
        workspace = Path(scratch)
        index = RAW / "ensembl84.k31.idx"
        if not index.is_file():
            raise ValueError("Missing frozen release-84 index")
        threads = str(min(4, len(os.sched_getaffinity(0))))
        for gsm, run in SAMPLES:
            if gsm != args.gsm:
                continue
            reads = RAW / f"{run}.verified.fastq.gz"
            if args.source == "sra":
                archive = RAW / f"{run}.sra"
                with (args.output / f"{gsm}.sra_validation.txt").open("w") as validation:
                    subprocess.run([RAW / "vdb-validate-3.2.1", archive], stdout=validation, stderr=subprocess.STDOUT, check=True)
                run_checked([RAW / "fasterq-dump-3.2.1", archive, "--split-spot", "--threads", threads, "--temp", workspace, "--outdir", workspace])
                reads = workspace / f"{run}.fastq"
                if not reads.is_file():
                    raise FileNotFoundError(reads)
            processed = workspace / f"{run}.trim.fastq.gz"
            quant = workspace / gsm
            with (args.output / f"{gsm}.cutadapt.txt").open("w") as logfile:
                subprocess.run([cutadapt, "-j", threads, "-m", "35", "-q", "30,30", "-o", processed, reads], stdout=logfile, check=True)
            if args.source == "sra":
                reads.unlink()
            run_checked([kallisto, "quant", "-i", index, "-o", quant, "--single", "-l", "200", "-s", "30", "-t", threads, "--plaintext", processed])
            shutil.copyfile(quant / "run_info.json", args.output / f"{gsm}.run_info.json")
            with (quant / "abundance.tsv").open("rb") as source, (args.output / f"{gsm}.abundance.tsv.gz").open("wb") as handle:
                with gzip.GzipFile(filename="", fileobj=handle, mode="wb", mtime=0) as dest:
                    shutil.copyfileobj(source, dest)
            processed.unlink()


if __name__ == "__main__":
    main()
