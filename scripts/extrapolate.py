"""
Extrapolate out-of-bounds instance UFOs in to the instances dir.
"""

from ufoProcessor import ufoOperator
from pathlib import Path

srcdir = Path(Path(__file__).resolve().parent, "../src").resolve()
src = Path(srcdir, "AnnotationMono.designspace")
print(srcdir, src)
doc = ufoOperator.UFOOperator(
    None,
    useVarlib=False,
    extrapolate=True,
)
doc.path = src
doc.debug = True
doc.doc.read(src)
doc.loadFonts(reload = True)
doc.generateUFOs()
