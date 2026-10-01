"""Preserve F09 v1 and widen its left margin to retain every target label."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parents[1]
original = HERE / "scripts/20_e5_external_figure.py"
prior = json.loads((HERE / "figures/E5_external_v1/render_record.json").read_text())
assert hashlib.sha256(original.read_bytes()).hexdigest() == prior["script_sha256"]
source = original.read_text()
assert source.count('"figures/E5_external_v1"') == 1
assert source.count('left=.075') == 1
source = source.replace('"figures/E5_external_v1"', '"figures/E5_external_v2"').replace('left=.075', 'left=.115')
namespace = {"__file__": str(original), "__name__": "e5_layout_revision"}
exec(compile(source, str(original), "exec"), namespace)
namespace["main"]()
path = HERE / "figures/E5_external_v2/render_record.json"
record = json.loads(path.read_text())
record["layout_revision"] = {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "change": "subplot left margin .075 to .115; values unchanged; v1 exports preserved"}
path.write_text(json.dumps(record, indent=2)+"\n")
