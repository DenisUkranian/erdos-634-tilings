#!/bin/sh
set -eu
base=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
c++ -O3 -std=c++20 -DREFLEX_FILTER -DSPAN_FILTER -DLOCATED_SPANS -DSIGN_FILTER -DBANK_PROBES "$base/pentphase.cpp" -o "$tmp/solver"
for record in '-3 1 330044' '-2 2 340375' '-1 3 340378' '0 4 313078'
do
 set -- $record
 got=$("$tmp/solver" 35 13 43 11 2 "$1" "$2" 800000 4 3)
 test "$got" = "NO(in palette) $3"
 echo "[$1,$2] $got"
done
"$tmp/solver" 35 13 43 4 0 -1 1 100000 0 0 > "$tmp/control"
head -1 "$tmp/control" | grep '^YES '
