#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir=${1:-"$here/../../../../../2026-11-19/nov19/equilateral231/cert"}
work_dir=${2:-"$(mktemp -d)"}
mkdir -p "$work_dir"
cp "$source_dir/make_trace.cpp" "$source_dir/verify.cpp" "$work_dir/"
cd "$work_dir"
printf '%s\n' '5977e63e86bd55542efad1f11ff3e70e35b1492b6726821bd35700f23e367d96  make_trace.cpp' '29134e48fc4158590fef64db35df315524d616d3d1382fb9712ef858795ec58b  verify.cpp' | sha256sum -c -
patch -s -p0 < "$here/target.patch"
c++ -O3 -std=c++17 verify.cpp -o verify_endpoints
c++ -O3 -std=c++17 make_trace.cpp -o prefilter
c++ -O3 -std=c++17 "$here/check_lines.cpp" -o check_lines
for lo in -1 0
do
    hi=$((lo+1))
    ./prefilter "$lo" "$hi" "board_$lo" 86400 1 0 2> "board_$lo.log"
    sed -n "/  board_${lo}\.remaining\.txt$/p" "$here/SHA256SUMS" | sha256sum -c -
    ./verify_endpoints "$lo" "$hi" "board_$lo.bitmap_trace.bin" "board_$lo.remaining.txt"
    ./check_lines "board_$lo.remaining.txt" target packed > "board_$lo.packed"
    ./check_lines "board_$lo.remaining.txt" target scalar > "board_$lo.scalar"
    cmp "board_$lo.packed" "board_$lo.scalar"
    cat "board_$lo.packed"
    ./prefilter "$lo" "$hi" "grid_$lo" 86400 0 2 2> "grid_$lo.log"
    ./check_lines "grid_$lo.remaining.txt" control scalar
done
