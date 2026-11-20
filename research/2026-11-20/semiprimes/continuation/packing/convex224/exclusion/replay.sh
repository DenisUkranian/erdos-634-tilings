#!/bin/sh
set -eu
cd "$(dirname "$0")"
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT HUP INT TERM
python3 profiles.py
c++ -std=c++20 -O3 check.cpp -o "$build/check"
"$build/check" 9 0 2 > "$build/control"
awk 'NF!=3 || $3!=2 {exit 1} END {if(NR!=3)exit 1}' "$build/control"
for m in 0 1 2 3 5; do
 "$build/check" "$m" 0 42 > "$build/out$m" &
done
wait
for m in 0 1 2 3 5; do
 awk -v m="$m" 'NF!=3 || $1!=m || $2!=NR-1 || $3!=0 {exit 1} END {if(NR!=43)exit 1}' "$build/out$m"
done
echo "All 215 candidate lists fail at a required corner. The 3 positive-control lists each retain the two grid triangles."
