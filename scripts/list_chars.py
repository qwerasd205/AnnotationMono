"""
Generate a string with all unicode chars supported by the font.
Based on the TTF, rather than the source files.
"""

from fontTools.ttLib.ttFont import TTFont

from pathlib import Path


dist_dir = Path(Path(__file__).resolve().parent, "../dist/").resolve()
font = TTFont((dist_dir / "variable/AnnotationMono-VF.ttf").resolve())

unis = list(font.getBestCmap().keys())
unis.sort()
print(''.join([f"<span>{chr(u)}</span>" for u in unis]))
