#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
rm -f Results/native_wolfram_results.json
if ! command -v wolframscript >/dev/null 2>&1; then
  echo 'ERROR: wolframscript not installed. No native certificate was produced.' >&2
  exit 2
fi
wolframscript -file Examples/RunNative.wls
python validation/verify_native.py
