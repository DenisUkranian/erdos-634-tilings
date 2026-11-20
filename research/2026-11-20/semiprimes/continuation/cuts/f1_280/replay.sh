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
c++ -O3 -std=c++17 make_trace.cpp -o make_trace
c++ -O3 -std=c++17 verify.cpp -o verify
for lo in -2 -1 0
do
    hi=$((lo+2))
    case "$lo" in
        -2) set -- 0 40 -33 0 ;;
        -1) set -- 1 1 0 1 ;;
         0) set -- 1 7 33 1 ;;
    esac
    ./make_trace "$lo" "$hi" "f1_$lo" 86400 1 0 2> "f1_$lo.log"
    sed -n "/  f1_${lo}\.bitmap_trace\.bin$/p" "$here/SHA256SUMS" | sha256sum -c -
    ./verify "$lo" "$hi" "f1_$lo.bitmap_trace.bin" "$@"
done
