#!/usr/bin/env python3
"""
Set the version number in all source UFOs.
"""

import ufoLib2
import argparse

from pathlib import Path

def version(v: str):
    parts = list(map(int, v.split(".")))
    if len(parts) != 2:
        raise ValueError

    return (parts[0], parts[1])

ap = argparse.ArgumentParser(description="Set the version number in all source UFOs.")

ap.add_argument("version", help="<major>.<minor>", type=version)

v = ap.parse_args().version

src_dir = Path(Path(__file__).resolve().parent, "../src/").resolve()
for ufo in src_dir.glob("*.ufo"):
    font = ufoLib2.Font.open(ufo.resolve(), lazy=True)

    font.info.versionMajor = v[0]
    font.info.versionMinor = v[1]

    font.save()
