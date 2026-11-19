"""Change the sign of one actual inference in an otherwise identical proof."""
from pathlib import Path
import shutil
import struct
import sys

source, output = map(Path, sys.argv[1:3])
if source.resolve() == output.resolve():
    raise SystemExit("Choose a separate output for the negative control.")
shutil.copyfile(source, output)
record = struct.Struct("<IIIQQ")
with output.open("r+b") as stream:
    stream.seek(-record.size, 2)
    d, y, w, positive, negative = record.unpack(stream.read(record.size))
    stream.seek(-record.size, 2)
    stream.write(record.pack(d, y, w, negative, positive))
