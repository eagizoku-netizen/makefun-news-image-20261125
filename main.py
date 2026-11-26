#!/usr/bin/env python3
"""Validate news.png and copy it byte-for-byte to the output directory.

Standard library only, no network. Deterministic: running twice produces
identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576


def fail(msg):
    print("error: " + msg)
    return 1


def main():
    src = "news.png"
    if not os.path.isfile(src):
        return fail("news.png not found")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("news.png is %d bytes, over 1 MiB" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("news.png is not a PNG file")
    if len(data) < 24:
        return fail("news.png is too short")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        return fail("news.png is %dx%d, expected 1024x1024" % (width, height))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./out")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    print("ok: news.png valid 1024x1024 %d bytes sha256=%s" % (len(data), sha))
    print("ok: copied to %s" % dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
