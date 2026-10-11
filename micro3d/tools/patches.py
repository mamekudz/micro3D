# SPDX-License-Identifier: GPL-3.0-or-later
"""Fail-closed source pin and patch manager. Python 3.11+, standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root, name):
    p = (root / name).resolve()
    if not p.is_relative_to(root.resolve()) or p == root.resolve():
        raise ValueError("Path outside project: " + name)
    return p


def git(source, *args, env=None, data=None):
    return subprocess.run(["git", "-C", str(source), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          input=data, env=env).stdout


def verify(root=ROOT, compare=True):
    manifest = read(root / "upstream/manifest.json")
    lock = read(root / "upstream/lock.json")
    series = read(root / "patches/series.json")
    if any(x.get("schemaVersion") != 1 for x in (manifest, lock, series)):
        raise ValueError("Unsupported schema")
    src = lock["source"]
    if not re.fullmatch(r"[0-9a-f]{40}", src["commit"]):
        raise ValueError("Full source commit required")
    if any(src[k] != manifest["upstream"][k] for k in ("url", "ref")):
        raise ValueError("Manifest/source mismatch")
    if manifest["patchSeries"] != "patches/series.json":
        raise ValueError("Unsupported patch series path")
    if lock["status"] != "bootstrap":
        raise ValueError("Release readiness requires a future full dependency-lock validator")
    entries = []
    ids, paths = set(), set()
    for item in series["patches"]:
        for key in ("id", "file", "purpose", "category", "tests", "upstreamStrategy"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError("Missing patch metadata: " + key)
        p = inside(root, item["file"])
        if not p.is_relative_to((root / "patches").resolve()) or p.suffix != ".patch":
            raise ValueError("Patch must be a .patch file inside patches/")
        if item["id"] in ids or p in paths:
            raise ValueError("Duplicate patch")
        ids.add(item["id"]); paths.add(p)
        entries.append({"id": item["id"], "file": item["file"], "sha256": sha(p)})
    if {p.resolve() for p in (root / "patches").rglob("*.patch")} != paths:
        raise ValueError("Unlisted patch file")
    if compare and lock["patches"] != entries:
        raise ValueError("Patch order/content differs from lock")
    verify_platform_locks(root, lock)
    return lock, entries


def verify_platform_locks(root, lock):
    entries = lock.get("platformLocks", {})
    if not isinstance(entries, dict):
        raise ValueError("platformLocks must be an object")
    upstream = (root / "upstream").resolve()
    for name, item in entries.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid platform lock name")
        if not isinstance(item, dict):
            raise ValueError("Invalid platform lock: " + name)
        rel = item.get("file")
        digest = item.get("sha256")
        if not isinstance(rel, str) or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("Platform lock requires file and sha256: " + name)
        path = inside(root, rel)
        if not path.is_relative_to(upstream) or path.suffix != ".json":
            raise ValueError("Platform lock must be a JSON file inside upstream/")
        if sha(path) != digest:
            raise ValueError("Platform lock hash mismatch: " + name)


def lock_patches(root=ROOT):
    lock, entries = verify(root, compare=False)
    lock["patches"] = entries
    p = root / "upstream/lock.json"
    temp = p.with_suffix(".json.tmp")
    temp.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(p)


def apply(source, root=ROOT):
    lock, entries = verify(root)
    source = source.resolve()
    top = Path(git(source, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if top != source:
        raise ValueError("Source must be a repository root")
    if git(source, "rev-parse", "HEAD").decode().strip() != lock["source"]["commit"]:
        raise ValueError("Wrong upstream commit")
    if git(source, "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("Source tree is not clean")
    if not entries:
        return
    # Stage sequential patches in an isolated temporary index. Real tree stays
    # untouched on hash/conflict failure, including a conflict in a later patch.
    with tempfile.TemporaryDirectory(prefix="micro3d-index-") as tmp:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(Path(tmp) / "index")
        git(source, "read-tree", "HEAD", env=env)
        for entry in entries:
            p = inside(root, entry["file"])
            git(source, "apply", "--cached", "--check", str(p), env=env)
            git(source, "apply", "--cached", str(p), env=env)
        delta = git(source, "diff", "--cached", "--binary", "HEAD", env=env)
        if delta:
            git(source, "apply", "--index", "--check", "-", data=delta)
            git(source, "apply", "--index", "-", data=delta)


def clone(root=ROOT):
    lock, _ = verify(root)
    dest = root / "vendor/blender"
    if dest.exists():
        raise ValueError("Clone destination exists; preserving it")
    dest.parent.mkdir(exist_ok=True)
    subprocess.run(["git", "clone", "--filter=blob:none", "--no-checkout",
                    lock["source"]["url"], str(dest)], check=True)
    git(dest, "fetch", "origin", lock["source"]["commit"])
    git(dest, "checkout", "--detach", lock["source"]["commit"])
    print("Pinned source cloned. Dependencies have NOT been resolved.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("verify", "lock-patches", "clone", "apply"))
    parser.add_argument("--source", type=Path, default=ROOT / "vendor/blender")
    args = parser.parse_args()
    try:
        if args.command == "verify":
            verify()
        elif args.command == "lock-patches":
            lock_patches()
        elif args.command == "clone":
            clone()
        else:
            apply(args.source)
        print("OK (source/patch scope only; dependency lock remains bootstrap)")
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, "ERROR: " + str(exc) + "\n" +
                    (getattr(exc, "stderr", b"") or b"").decode(errors="replace"))


if __name__ == "__main__":
    main()
