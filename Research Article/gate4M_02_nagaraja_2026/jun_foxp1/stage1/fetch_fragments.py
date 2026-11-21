"""Cache complete public fragment objects with resumable ranges and deposited MD5s."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import time

import requests

S0 = Path("raw_data/nagaraja_s0")
DEST = Path("raw_data/nagaraja_jf1")
PART = 16 * 1024 * 1024


def fetch_file(series):
    record = json.loads((S0 / (series + ".json")).read_bytes())
    item, = [f for f in record["files"] if f["content_type"] == "fragments"]
    url = item["s3_uri"].replace("s3://igvf-public/", "https://igvf-public.s3.amazonaws.com/")
    size = item["file_size"]
    target = DEST / url.split("/")[-1]
    def correct(p):
        with p.open("rb") as stream:
            return p.stat().st_size == size and hashlib.file_digest(stream, "md5").hexdigest() == item["md5sum"]
    if target.exists():
        assert correct(target)
        return
    progress = DEST / (item["accession"] + "_ranges")
    progress.mkdir(parents=True, exist_ok=True)
    cache = target.with_suffix(".partial")
    if not cache.exists():
        assert not list(progress.glob("*.ok"))
        with cache.open("wb") as stream:
            stream.truncate(size)
    assert cache.stat().st_size == size
    def piece(start):
        end = min(size-1, start+PART-1)
        marker = progress / f"{start}.ok"
        if marker.exists():
            return
        for trial in range(6):
            try:
                with requests.get(url, params={"partStart":start}, headers={"Range":f"bytes={start}-{end}"},
                                  timeout=(18,90)) as response:
                    response.raise_for_status()
                    if response.status_code != 206 or response.headers.get("Content-Range") != f"bytes {start}-{end}/{size}":
                        raise ValueError(f"Unexpected range for {item['accession']}: {start}")
                    data = response.content
                    assert len(data) == end-start+1
                with cache.open("r+b") as stream:
                    stream.seek(start)
                    stream.write(data)
                marker.write_text(str(len(data)))
                return
            except (requests.RequestException, ValueError, AssertionError):
                if trial == 5:
                    raise
                time.sleep(2**trial)
    with ThreadPoolExecutor(8) as workers:
        list(workers.map(piece,range(0,size,PART)))
    if not correct(cache):
        raise ValueError(f"Source MD5 mismatch: {item['accession']}")
    os.replace(cache,target)
    print(f"{item['accession']} complete, {size} bytes, verified MD5",flush=True)


if __name__ == "__main__":
    for dataset in ["IGVFDS0502QEQJ","IGVFDS0237MRDL"]:
        fetch_file(dataset)
