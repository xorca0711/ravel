#!/usr/bin/env python3
"""Install Ravel hook declarations at Codex's root-checkout discovery location.

Never changes hook trust, permissions, other configuration, or research files.
The handler still resolves and uses the session's own checkout at execution.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tomllib


def main_checkout(source: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(source), "worktree", "list", "--porcelain"],
        capture_output=True, text=True, check=True, timeout=10,
    )
    first = result.stdout.split("\n\n", 1)[0].splitlines()
    if not first or not first[0].startswith("worktree ") or "bare" in first:
        raise ValueError("A non-bare main checkout is required.")
    return Path(first[0].removeprefix("worktree ")).resolve()


def plan(source: Path, target: Path) -> dict:
    """Validate an installation without writes; fail rather than replace user hooks."""
    source, target = source.resolve(), target.resolve()
    config = tomllib.loads((source / ".codex/config.toml").read_text(encoding="utf-8"))
    if "hooks" in config:
        raise ValueError("Source config has inline hooks; keep declarations only in hooks.json.")
    payload = json.loads((source / ".codex/hooks.json").read_text(encoding="utf-8"))
    hooks = payload["hooks"]
    if set(hooks) != {"SessionStart", "Stop"}:
        raise ValueError("Unexpected source hook events; review before installing.")
    folder = (target / ".codex").resolve()
    if not folder.is_relative_to(target):
        raise ValueError("The target .codex directory escapes its checkout.")
    destination = folder / "hooks.json"
    root_config = folder / "config.toml"
    if root_config.exists():
        existing = tomllib.loads(root_config.read_text(encoding="utf-8"))
        if "hooks" in existing:
            raise ValueError("Main checkout already has inline hooks; reconcile them explicitly.")
        if existing.get("features", {}).get("hooks") is False:
            raise ValueError("Main checkout explicitly disables hooks; preserve that setting.")
    if destination.exists():
        if json.loads(destination.read_text(encoding="utf-8")) != payload:
            raise ValueError("Main checkout has a different hooks.json; refusing to overwrite it.")
        return {"status": "already-installed", "path": str(destination)}
    return {"status": "ready", "path": str(destination), "payload": payload,
            "create_config": not root_config.exists()}


def install(source: Path, target: Path) -> dict:
    result = plan(source, target)
    if result["status"] != "ready":
        return result
    destination = Path(result["path"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    config = destination.parent / "config.toml"
    if result["create_config"]:
        with config.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write("# Root-checkout hook discovery anchor. Trust is reviewed separately.\n[features]\nhooks = true\n")
    # Exclusive creation prevents replacing a file added since the preflight.
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(result["payload"], handle, indent=2)
        handle.write("\n")
    return {"status": "installed-pending-trust", "path": str(destination)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Create the main-checkout declarations; never trust them.")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[2]
    try:
        target = main_checkout(source)
        result = install(source, target) if args.install else plan(source, target)
        result.pop("payload", None)
        print(json.dumps({"source_checkout": str(source), "main_checkout": str(target), **result}))
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
