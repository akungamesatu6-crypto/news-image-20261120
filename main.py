#!/usr/bin/env python3
"""news-image-20261120 entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file; the program copies it to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader).
Deterministic: the same bytes out on every run. No network, no dependencies.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
