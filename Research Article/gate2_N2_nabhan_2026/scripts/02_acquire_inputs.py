"""Recover public Nb3 source inputs to ignored storage with exact hash checks."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
INPUTS = {
    "GSE307112_gene_counts.xlsx": "60736e5c153a4fb92908f19148ebb5ef2b59f7ade97fb1056deee7d0205acc33",
    "GSE307112_xenome_stats.csv.gz": "045b9da623db54a59948f1e8e6b68c1587fa4786a6838a51a890dfe59064edf5",
}


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def recover(item):
    name, expected = item
    target = ROOT / "raw_data/GSE307112" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE307nnn/GSE307112/suppl/" + name
    started = time.time()
    if not target.exists():
        partial = target.with_name(name + ".part")
        request = urllib.request.Request(url, headers={"User-Agent": "Nb3-public-reproduction/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as handle:
            total = 0
            while chunk := response.read(2**20):
                handle.write(chunk)
                total += len(chunk)
                if total % (64 * 2**20) == 0:
                    print(f"{name}: {total // 2**20} MiB", flush=True)
        if sha(partial) != expected:
            raise ValueError(f"Hash differs from historical acquisition: {name}")
        partial.replace(target)
    if sha(target) != expected:
        raise ValueError(f"Existing input differs: {name}")
    return {"path": target.relative_to(ROOT).as_posix(), "url": url,
            "bytes": target.stat().st_size, "sha256": expected,
            "seconds": round(time.time()-started, 2)}


if __name__ == "__main__":
    out = HERE / "reports/Nb3_acquisition.json"
    if out.exists():
        raise SystemExit("Acquisition record exists; inspect it rather than overwriting.")
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(recover, INPUTS.items()))
    out.write_text(json.dumps({"analysis_id": "Nb3", "files": records}, indent=2)+"\n", encoding="utf-8")
    print("Recovered and verified both inputs.", flush=True)
