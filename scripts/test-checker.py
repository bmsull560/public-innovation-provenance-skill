#!/usr/bin/env python3
"""Run the provenance checker against pass and should-fail fixtures."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check-provenance.py"


def run(pack: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(pack)],
        capture_output=True,
        text=True,
    )


def main() -> None:
    failed = 0
    for pack in sorted((ROOT / "fixtures" / "pass").iterdir()):
        if not pack.is_dir():
            continue
        result = run(pack)
        if result.returncode != 0:
            failed += 1
            print(f"PASS FIXTURE FAILED {pack.name}: {result.stderr.strip()}")
        else:
            print(f"ok {pack.name}")
    for pack in sorted((ROOT / "fixtures" / "should-fail").iterdir()):
        if not pack.is_dir():
            continue
        expect = (pack / "expect.txt").read_text(encoding="utf-8").strip()
        result = run(pack)
        if result.returncode == 0 or expect not in result.stderr:
            failed += 1
            print(
                f"SHOULD-FAIL MISSED {pack.name}: code={result.returncode} "
                f"stderr={result.stderr.strip()!r} expected {expect!r}"
            )
        else:
            print(f"ok reject {pack.name}")
    if failed:
        print(f"{failed} fixture checks failed", file=sys.stderr)
        raise SystemExit(1)
    print("all fixture checks passed")


if __name__ == "__main__":
    main()
