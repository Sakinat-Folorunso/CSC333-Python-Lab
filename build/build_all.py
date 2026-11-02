"""Build every week's Starter + Solution notebooks.  Usage: python build/build_all.py [week ...]"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

weeks = [int(a) for a in sys.argv[1:]] or list(range(0, 13))
for w in weeks:
    name = f"week{w:02d}"
    try:
        mod = importlib.import_module(name)
    except ModuleNotFoundError:
        print(f"(skip) {name} not written yet")
        continue
    for p in mod.build():
        print("built", os.path.relpath(p))
