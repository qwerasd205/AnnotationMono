#!/usr/bin/env sh

set -e

# Make sure we're starting from the root directory
# of the repo where this build script is located.
cd "$(readlink -f "$(dirname "$0")")"

# Activate python virtual environment.
./activate.sh
. ./venv/bin/activate

echo "Cleaning build dir..."
mkdir -p ./build
rm -rf ./build/*

# Process our file in to a form appropriate for building with fontmake.
echo "Preparing UFOs..."
fontra-workflow workflow.yaml --output-dir build
# Copy the original designspace document to the build dir since for
# some reason fontra-workflow strips the instance definitions from it...
cp ./src/AnnotationMono.designspace ./build/AnnotationMono.designspace
# Call prep script, fixes some stuff fontra messes up.
python3 prepare_build.py

# Call fontmake to build our OTF and TTF fonts.
echo "Making fonts..."

fontmake -f -m ./build/AnnotationMono.designspace \
  --filter DecomposeTransformedComponentsFilter \
  --filter PropagateAnchorsFilter \
  --fea-include-dir ./src/features/ \
  --output-dir ./dist/otf -o otf -i

fontmake -f -m ./build/AnnotationMono.designspace \
  --filter DecomposeTransformedComponentsFilter \
  --filter PropagateAnchorsFilter \
  --fea-include-dir ./src/features/ \
  --output-dir ./dist/ttf -o ttf -i

fontmake -f -m ./build/AnnotationMono.designspace \
  --filter DecomposeTransformedComponentsFilter \
  --filter PropagateAnchorsFilter \
  --fea-include-dir ./src/features/ \
  --output-dir ./dist/variable -o variable

# Fix GASP table to ensure quality rasterization in more scenarios.
find ./dist/otf/*.otf -print0 | xargs -0 -I {} gftools fix-nonhinting --no-backup {} {}
find ./dist/ttf/*.ttf -print0 | xargs -0 -I {} gftools fix-nonhinting --no-backup {} {}
find ./dist/variable/*.ttf -print0 | xargs -0 -I {} gftools fix-nonhinting --no-backup {} {}

# Create woff2 fonts from our TTFs.
find ./dist/ttf/*.ttf -print0 | xargs -0 -I {} woff2_compress {}
mv ./dist/ttf/*.woff2 ./dist/woff2
find ./dist/variable/*.ttf -print0 | xargs -0 -I {} woff2_compress {}
mv ./dist/variable/*.woff2 ./dist/variable_woff2
