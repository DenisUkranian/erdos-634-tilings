#!/bin/sh
set -eu
base=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
python3 "$base/check_nesting.py" prepare "$tmp/both"
c++ -O3 -std=c++20 "$base/hulls.cpp" -o "$tmp/hulls"
"$tmp/hulls" 300 10000 < "$tmp/both" > "$tmp/cavities" 2> "$tmp/progress"
grep -Fx 'finish expanded 506 remaining 0 pass 128' "$tmp/progress"
cmp "$tmp/cavities" "$base/cavities.txt"
python3 "$base/check_nesting.py" check "$tmp/cavities"
