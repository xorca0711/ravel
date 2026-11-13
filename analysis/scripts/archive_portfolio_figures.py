"""Copy a frozen, explicit figure manifest; never execute numerical analyses."""
import argparse, hashlib, json, shutil
from pathlib import Path

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    manifest = root / args.manifest
    data = json.loads(manifest.read_text(encoding="utf-8"))
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    for record in data["assets"]:
        source = (root / record["input"]).resolve()
        target = (output / record["output"]).resolve()
        if not source.is_relative_to(root) or not target.is_relative_to(output):
            raise ValueError("Path escapes archive workspace")
        if digest(source) != record["sha256"]:
            raise ValueError("Input hash mismatch: " + record["input"])
        if target.exists():
            raise FileExistsError(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if digest(target) != record["sha256"]:
            raise ValueError("Output hash mismatch: " + record["output"])
    public = {k: v for k, v in data.items() if k != "assets"}
    public["assets"] = [{k: v for k, v in a.items() if k != "input"} for a in data["assets"]]
    (output / "manifest.json").write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Archived {len(data['assets'])} assets; all hashes match; no analysis rerun.")

if __name__ == "__main__":
    main()
