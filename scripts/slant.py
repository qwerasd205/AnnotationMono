"""
Create slanted versions of the base UFOs as a first
step in producing the slanted forms for the font.
"""

import math
import ufoLib2

from pathlib import Path

def sign(x):
    return 1 if x >= 0 else -1

VAR_COMP = "com.black-foundry.variable-components"

angle = -15
off = -50
slope = math.tan(-angle * (math.pi / 180))

src_dir = Path(Path(__file__).resolve().parent, "../src/").resolve()
for ufo in src_dir.glob("*.ufo"):
    if f"[slnt={angle}]" in ufo.resolve().name:
        continue
    new_name = f"{ufo.resolve().name.split('.')[0]}[slnt={angle}].ufo"
    new_path = src_dir / new_name
    font = ufoLib2.Font.open(ufo.resolve(), lazy=True)

    font.info.italicAngle = angle

    for guideline in font.guidelines:
        if guideline.angle == 90:
            guideline.angle = 90 - math.fabs(angle)
            guideline.x = guideline.x + off if guideline.x else off

    bar_bounds = font['bar'].getBounds(font.layers.defaultLayer)
    assert bar_bounds
    factor = (-angle / 90) * (bar_bounds.xMax - bar_bounds.xMin) + 5

    for glyph in font:
        for cmp in glyph.components:
            tran = cmp.transformation
            dcmp = tran.toDecomposed()
            flip = 1 - sign(dcmp.scaleX * dcmp.scaleY)
            cmp.transformation = tran.skew(-flip * slope, 0)
            cmp.move((dcmp.translateY * slope + flip * off, 0))
        if VAR_COMP in glyph.lib:
            for cmp in glyph.lib[VAR_COMP]:
                if "transformation" not in cmp:
                    continue
                tran = cmp["transformation"]
                flip = 1 - sign(tran["scaleX"] * tran["scaleY"])
                cmp["transformation"]["skewX"] += flip * angle
                cmp["transformation"]["translateX"] += (
                    tran["translateY"] * slope + flip * off
                )
                if tran["rotation"] % 90 != 0:
                    cmp["transformation"]["translateY"] += off * (
                        1 - (tran["rotation"] % 90) / 90
                    )
                    cmp["transformation"]["rotation"] += angle
        for anc in glyph.anchors:
            anc.x += slope * anc.y + off
        for cnt in glyph.contours:
            for p in cnt:
                p.x += slope * p.y + off
            # for i, p in enumerate(cnt):
            #     if p.type is not None and p.smooth:
            #         other = cnt[i - 1]
            #         pangle = math.atan2(other.y - p.y, other.x - p.x)
            #         offset = factor * 0.5 * math.cos(pangle + angle * (math.pi / 180))
            #         p.x += offset
            #         cnt[i - 1].x += offset
            #         cnt[(i + 1) % len(cnt)].x += offset

    font.save(new_path, overwrite=True)
