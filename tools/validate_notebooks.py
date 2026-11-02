"""Validate the CSC 333 notebooks.

* Solution notebooks: executed top to bottom; any exception or any '❌' check = FAIL.
* Starter notebooks : every code cell must parse; they are also executed and must
  not raise (the '❌ Not yet' messages are expected there).

input() is simulated with CANNED answers (matched by prompt substring) so notebooks
that call input() can run unattended.

Usage:  python tools/validate_notebooks.py [week_number ...]
"""
import ast
import contextlib
import glob
import importlib
import io
import os
import re
import sys
import tempfile
import traceback

import nbformat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# substring of the prompt -> canned reply
CANNED = [
    ("name", "Amina"), ("programme", "Data Science"), ("department", "Computer Science"),
    ("matric", "OOU/2026/001"), ("level", "300"), ("length", "5"), ("width", "3"),
    ("radius", "2"), ("mark", "70"), ("score", "75"), ("number", "12"), ("first", "8"),
    ("second", "2"), ("choice", "1"), ("option", "1"), ("operation", "+"), ("minutes", "135"),
    ("principal", "10000"), ("rate", "5"), ("time", "2"), ("sentence", "Python is fun to learn"),
    ("guess", "7"), ("km", "10"), ("kilometres", "10"), ("password", "oou123"),
    ("how many", "3"), ("n", "4"),
]


def fake_input(prompt=""):
    low = str(prompt).lower()
    for key, val in CANNED:
        if key in low:
            return val
    return "5"


def code_of(nb):
    out = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        first = c.source.split("\n", 1)[0].strip()
        if first.startswith("%%writefile"):
            # emulate Colab: save the cell body as a file instead of running it
            fname = first.split(None, 1)[1].strip()
            body = c.source.split("\n", 1)[1] if "\n" in c.source else ""
            out.append((i, f"open({fname!r}, 'w', encoding='utf-8').write({body!r})"))
            continue
        lines = [ln for ln in c.source.split("\n")
                 if not ln.lstrip().startswith(("!", "%"))]
        out.append((i, "\n".join(lines)))
    return out


def run(path, strict):
    nb = nbformat.read(path, as_version=4)
    cells = code_of(nb)
    problems = []
    for i, src in cells:                       # 1. syntax check everywhere
        try:
            ast.parse(src)
        except SyntaxError as e:
            problems.append(f"cell {i}: SyntaxError {e}")
    if problems:
        return problems, ""
    ns = {"__name__": "__main__", "input": fake_input}
    outbuf = io.StringIO()
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        sys.path.insert(0, tmp)                 # like Jupyter: the working folder is importable
        try:
            for i, src in cells:
                importlib.invalidate_caches()   # so files written by %%writefile can be imported
                try:
                    with contextlib.redirect_stdout(outbuf):
                        exec(compile(src, f"<cell {i}>", "exec"), ns)
                except SystemExit:
                    pass
                except Exception:
                    tb = traceback.format_exc(limit=3)
                    problems.append(f"cell {i}: {tb.strip().splitlines()[-1]}")
                    if strict:
                        break
        finally:
            os.chdir(cwd)
            if tmp in sys.path:
                sys.path.remove(tmp)
            for name, mod in list(sys.modules.items()):      # forget modules imported from the temp folder
                f = getattr(mod, '__file__', None)
                if f and str(f).startswith(tmp):
                    sys.modules.pop(name, None)
    text = outbuf.getvalue()
    if strict:
        bad = [ln for ln in text.splitlines() if "❌" in ln]
        problems += [f"failed check -> {ln}" for ln in bad]
    return problems, text


def main():
    import matplotlib
    matplotlib.use("Agg")
    weeks = [int(a) for a in sys.argv[1:]]
    paths = sorted(glob.glob(os.path.join(ROOT, "notebooks", "week*", "*.ipynb")))
    if weeks:
        paths = [p for p in paths if int(re.search(r"week(\d+)_", p).group(1)) in weeks]
    failed = 0
    for p in paths:
        strict = p.endswith("_Solution.ipynb")
        probs, _ = run(p, strict)
        tag = os.path.relpath(p, ROOT)
        if probs:
            failed += 1
            print(f"FAIL {tag}")
            for pr in probs[:8]:
                print("     ", pr)
        else:
            print(f"ok   {tag}")
    print(f"\n{len(paths) - failed}/{len(paths)} notebooks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
