#!/usr/bin/env bash
set -euo pipefail

# Build a Chrome Web Store upload ZIP from this directory.
# The ZIP must contain manifest.json at its root, so we zip the
# directory *contents*, excluding docs and this script.

cd "$(dirname "$0")"

VERSION=$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")
OUT_DIR="../dist"
OUT="$OUT_DIR/civico-downloader-v$VERSION.zip"

mkdir -p "$OUT_DIR"
rm -f "$OUT"

zip -r "$OUT" manifest.json popup.html popup.css popup.js icons \
    -x "*.DS_Store"

echo "Built $OUT"
unzip -l "$OUT"
