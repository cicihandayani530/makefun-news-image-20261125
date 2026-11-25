#!/usr/bin/env python3
"""THE TIDEWATER POST — News Image, Tuesday 25 November 2026 (Akun 3).

The front page ships inside this repository as entry.png; running this
file simply places that page at /output/entry.png, unchanged. Nothing
here draws, downloads or computes: standard library only.
"""
import os
import shutil

PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
TARGET_DIR = "/output"


def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    target = os.path.join(TARGET_DIR, "entry.png")
    shutil.copyfile(PAGE, target)
    print("entry.png ->", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
