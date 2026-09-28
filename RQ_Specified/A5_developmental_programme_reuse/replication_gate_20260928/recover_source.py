"""Bounded A5 source recovery. Downloads metadata and author text only, never matrices."""
import argparse, hashlib, json, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'sources'
OUT.mkdir(exist_ok=True)
LEDGER = ROOT / 'source_ledger.json'

def fetch(key, url):
    records = json.loads(LEDGER.read_text(encoding='utf-8')) if LEDGER.exists() else []
    old = next((r for r in records if r['key'] == key), None)
    if old and old.get('status') == 'downloaded' and (ROOT / old['path']).exists():
        print(json.dumps({'key': key, 'status': 'reused', 'bytes': old['bytes']}))
        return
    row = {'key': key, 'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'A5-metadata-audit/1.0', 'Accept': 'application/json,text/plain,text/html,*/*'})
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read(10_000_001)
            if len(data) > 10_000_000:
                raise ValueError('Metadata safety cap 10 MB exceeded; matrix download refused')
            path = OUT / (key + '.txt')
            path.write_bytes(data)
            row.update(status='downloaded', http_status=response.status, final_url=response.url,
                       content_type=response.headers.get('Content-Type'), bytes=len(data),
                       sha256=hashlib.sha256(data).hexdigest(), path=str(path.relative_to(ROOT)).replace('\\', '/'))
    except Exception as exc:
        row.update(status='retrieval_failed', error=str(exc))
    records.append(row)
    LEDGER.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: row[k] for k in ['key','status','bytes','error'] if k in row}))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('key'); ap.add_argument('url')
    args = ap.parse_args()
    fetch(args.key, args.url)
