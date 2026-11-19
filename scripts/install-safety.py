#!/usr/bin/env python3
"""V4 install-safety snapshots: hash every file in Typora's themes dir and the
Obsidian ITS theme dir. Usage: install-safety.py pre|post|verify
- pre:  write test/install-snapshots/pre.json
- post: write test/install-snapshots/post.json
- verify: diff pre vs post — PASS only if the ONLY changes are additions inside our
  owned paths (its.css, its-dark.css, its-assets/) and the Obsidian dir is unchanged.
"""
import hashlib
import json
import sys
from pathlib import Path

TYPORA_THEMES = Path("/home/lithvik/.var/app/io.typora.Typora/config/Typora/themes")
OBSIDIAN_ITS = Path("/home/lithvik/Obsidian/Projects/.obsidian/themes/ITS Theme")
SNAP = Path(__file__).resolve().parent.parent / "test" / "install-snapshots"
OWNED = ("cryptomize.css", "cryptomize-dark.css", "cryptomize.meta.json", "cryptomize-dark.meta.json", "cryptomize-assets/")


def snap_dir(d: Path) -> dict:
    out = {}
    if not d.exists():
        return {"__missing__": True}
    for f in sorted(d.rglob("*")):
        if f.is_file():
            rel = str(f.relative_to(d))
            out[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    SNAP.mkdir(parents=True, exist_ok=True)
    data = {"typora_themes": snap_dir(TYPORA_THEMES), "obsidian_its": snap_dir(OBSIDIAN_ITS)}
    if mode in ("pre", "post"):
        (SNAP / f"{mode}.json").write_text(json.dumps(data, indent=2, sort_keys=True))
        print(f"{mode}: {len(data['typora_themes'])} typora files, {len(data['obsidian_its'])} obsidian files hashed")
        return
    pre = json.loads((SNAP / "pre.json").read_text())
    post = json.loads((SNAP / "post.json").read_text())
    ok = True
    if pre["obsidian_its"] != post["obsidian_its"]:
        print("V4 FAIL: Obsidian ITS dir changed!")
        ok = False
    pre_t, post_t = pre["typora_themes"], post["typora_themes"]
    for f, h in pre_t.items():
        if f not in post_t:
            print(f"V4 FAIL: file removed: {f}")
            ok = False
        elif post_t[f] != h:
            print(f"V4 FAIL: existing file modified: {f}")
            ok = False
    added = [f for f in post_t if f not in pre_t]
    rogue = [f for f in added if not any(f == o or f.startswith(o) for o in OWNED)]
    if rogue:
        print(f"V4 FAIL: additions outside owned paths: {rogue}")
        ok = False
    print(f"V4: additions = {added if added else 'none'}")
    print("V4:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
