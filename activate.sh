#!/bin/sh -e

cd "$(readlink -f "$(dirname "$0")")"

echo "Creating virtual environment..."
python3 -m venv venv
echo "Activating..."
. ./venv/bin/activate
echo ""
echo "================"
echo ""
echo "Installing requirements..."
pip3 install -r ./requirements.txt
echo ""
echo "================"
echo ""
echo "Done setting up virtual environment."
echo "Use the venv in your shell by calling \`source venv/bin/activate\`, or \`. venv/bin/activate.fish\` for fish shell."
echo "Deactivate with \`deactivate\`."
