from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Plan, build, test and document a small Python data application from a clear brief.",
    "Organise code into a **module**, a **test file** and a **README** that another person can run.",
    "Find and fix seeded defects under time pressure (mock practical), then explain the fix.",
    "Prepare and deliver a 5-minute demonstration that links design decisions to evidence.",
    "Reflect honestly on what you can now do, and what to practise next.",
]

ITEMS = [
    md("""## 1. From exercises to a finished piece of work
Weeks 1 to 11 built the parts. This week you assemble them into **one reliable mini-application** and learn how professionals *deliver* it: code that runs, tests that prove it, and documentation that lets someone else use it.

### The project: Student Records Analyser (fictional data)
| Stage | What the program does | Weeks used |
|---|---|---|
| 1. Generate | Create a reproducible table of student records (`seed=42`) | 9, 10 |
| 2. Clean/validate | Reject impossible values, standardise labels | 3, 11 |
| 3. Store | Save and load records with **parameterised SQLite** queries | 11 |
| 4. Analyse | Grade bands, pass rate, best programme, top students | 4, 5, 10 |
| 5. Report | A chart and a printed summary | 11 |
| 6. Verify | Automated tests with `pytest` | 11 |
| 7. Document | A `README.md` anyone can follow | 0 |

### Marking guide for the final project (100 marks)
| Criterion | Marks | Excellent looks like |
|---|---|---|
| Correctness | 30 | Every function gives the right answer on normal, boundary and invalid input |
| Code quality | 20 | Clear names, every line understood, functions that do **one** job, no repeated code |
| Testing | 20 | Normal + boundary + invalid tests that fail when the code is broken |
| Documentation | 15 | README with install, usage, tests, limitations, author |
| Demonstration | 15 | 5 minutes, live run, honest about limitations |

> **Academic integrity.** You may discuss ideas, but the code you submit must be your own and you must be able to explain every line. Cite any help (a person, a tutorial, an AI tool) in your README. Being unable to explain your own submission is treated as a breach of integrity.

### The professional habit: *small, run, test, repeat*
Write a few lines, run them, test them, commit them. Do not write 200 lines and then debug. In the lab practical you will also be asked to **find a bug**: read the error, reproduce it with the smallest example, form a hypothesis, change one thing, test again.
"""),
    demo('''%%writefile records_app.py
"""records_app.py : the data layer of the Student Records Analyser (fictional data).
Author: Dr Sakinat Folorunso, Department of Computer Science, Olabisi Onabanjo University (teaching module).
"""
import sqlite3                                      # database (built into Python)
import numpy as np                                  # numerical arrays and random numbers
import pandas as pd                                 # tables

PROGRAMMES = ["CS", "DS", "CYB", "SE", "ICT"]       # the official programme codes

def make_records(n=30, seed=42):
    """Return a reproducible table of n fictional student records."""
    rng = np.random.default_rng(seed)               # seeded generator: same numbers every run
    return pd.DataFrame({
        "student_id": np.arange(1, n + 1),                              # 1, 2, ..., n
        "programme": rng.choice(PROGRAMMES, size=n),                    # random programme code
        "score": rng.integers(25, 100, size=n),                         # whole-number scores in [25, 99]
    })

def pass_rate(df, pass_mark=40):
    """Fraction of students with score >= pass_mark (a number between 0 and 1)."""
    return float((df["score"] >= pass_mark).mean())   # True counts as 1, so the mean is the fraction

def save_to_db(df, con):
    """Store a records table in SQLite using parameterised queries."""
    with con:                                       # one transaction
        con.execute("CREATE TABLE IF NOT EXISTS records (student_id INTEGER PRIMARY KEY, programme TEXT NOT NULL, score INTEGER)")
        rows = [(int(i), str(p), int(s)) for i, p, s in df.itertuples(index=False)]   # numpy ints -> plain Python ints
        con.executemany("INSERT OR REPLACE INTO records(student_id, programme, score) VALUES (?, ?, ?)", rows)

def load_from_db(con):
    """Return all stored records as a table, ordered by student_id."""
    return pd.read_sql_query("SELECT student_id, programme, score FROM records ORDER BY student_id", con)'''),
    demo('''# --- DEMO 1: use the module like a user of your application would -----------------------------------------------
import sqlite3
import numpy as np                               # used later in the tasks
import pandas as pd
import records_app as ra                           # import the file we just wrote

df = ra.make_records()                             # stage 1: generate (seed 42 inside)
print(df.head())                                   # first five rows
print("rows:", len(df), "| pass rate:", round(ra.pass_rate(df), 3))

con = sqlite3.connect(":memory:")                  # stage 3: store
ra.save_to_db(df, con)
back = ra.load_from_db(con)
print("round trip identical:", back.equals(df))    # the data survives a trip through SQLite
con.close()'''),
    demo('''%%writefile test_records_app.py
# test_records_app.py : the safety net for records_app.py (run with pytest)
import sqlite3
import records_app as ra

def test_make_records_is_reproducible():            # NORMAL: same seed gives same table
    assert ra.make_records(10, seed=42).equals(ra.make_records(10, seed=42))

def test_make_records_scores_in_range():            # BOUNDARY: scores must stay inside [25, 99]
    df = ra.make_records(200, seed=1)
    assert df["score"].min() >= 25 and df["score"].max() <= 99

def test_pass_rate_boundary():                      # BOUNDARY: exactly 40 passes, 39 does not
    df = ra.make_records(3)
    df["score"] = [40, 39, 100]
    assert abs(ra.pass_rate(df) - 2 / 3) < 1e-9

def test_database_round_trip():                     # NORMAL: save then load returns identical data
    con = sqlite3.connect(":memory:")
    df = ra.make_records(15)
    ra.save_to_db(df, con)
    assert ra.load_from_db(con).equals(df)
    con.close()'''),
    demo('''# --- DEMO 2: run the whole test suite ---------------------------------------------------------------------------
import pytest
code = pytest.main(["-q", "test_records_app.py"])  # -q = quiet output
print("exit code:", int(code), "(0 means all tests passed)")'''),
    demo('''# --- DEMO 3: a README is part of the program --------------------------------------------------------------------
readme_example = """# Student Records Analyser

## Purpose
Generates, cleans, stores and summarises fictional student records.

## Installation
Python 3.11+ and: pip install numpy pandas matplotlib pytest

## Usage
    import records_app as ra
    df = ra.make_records()
    print(ra.pass_rate(df))

## Testing
    pytest -q

## Limitations
Data are synthetic; scores are whole numbers from 25 to 99.

## Author
Your Name, Matric Number, Department of Computer Science, Olabisi Onabanjo University
"""
print(readme_example)'''),
    activity(
        "Spot the bug before you run",
        "This function should return the fraction of scores that are **at least** 40. Predict the output for `[40, 39, 100]`, then run it.",
        '''def buggy_pass_rate(scores):
    passed = 0
    for s in scores:
        if s > 40:                       # <- suspicious
            passed += 1
    return passed / len(scores)

print(buggy_pass_rate([40, 39, 100]))''',
        "It prints `0.333...` but the correct answer is `0.666...`. The comparison `s > 40` excludes the boundary value 40. This is an **off-by-one at the boundary**, the most common class of bug. A boundary test (`[40, 39, 100]`) exposes it immediately, which is why boundary tests matter. Fix: `s >= 40`."),
    activity(
        "Why seed_everything?",
        "Run the cell twice (use Runtime > Run all). Predict which line changes between runs and which never changes.",
        '''import random
import numpy as np
print("unseeded :", random.random())
print("seeded   :", np.random.default_rng(42).integers(0, 100, size=3))''',
        "The unseeded line changes on every run; the seeded line is always the same (`[8 77 65]`). Reproducibility lets a marker, a teammate, or you next month obtain the *same* results. In research this is a basic requirement."),
    md("""## 🛠️ Tasks
These tasks complete the *analysis* layer of the application. The module `records_app` from the demos is already imported as `ra`.
"""),
    task(1, "Grade bands",
         "Write `grade_band(score)` using these cut-offs: **A** 70 to 100, **B** 60 to 69, **C** 50 to 59, **D** 45 to 49, **E** 40 to 44, **F** 0 to 39. A score below 0, above 100, or not a number must raise `ValueError`.",
         '''def grade_band(score):
    # TODO: validate first (number, 0..100), then return "A".."F" with if / elif
    pass

print(grade_band(72))''',
         '''def grade_band(score):
    if not isinstance(score, (int, float)) or isinstance(score, bool):   # reject text, None and True/False
        raise ValueError(f"Score must be a number, got {score!r}")
    if score < 0 or score > 100:                                         # reject impossible values
        raise ValueError(f"Score out of range: {score}")
    if score >= 70:                                                      # test the HIGHEST band first
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    return "F"                                                           # everything else is below 40

print(grade_band(72))''',
         '''cases = {100: "A", 70: "A", 69: "B", 60: "B", 59: "C", 50: "C", 49: "D", 45: "D", 44: "E", 40: "E", 39: "F", 0: "F"}
wrong = {s: grade_band(s) for s, g in cases.items() if grade_band(s) != g}
check(not wrong, "all 12 boundary scores are in the correct band", f"check these scores: {wrong}")
def _raises(v):
    try:
        grade_band(v)
    except ValueError:
        return True
    return False
check(all(_raises(v) for v in (-1, 101, "70", None)), "invalid inputs raise ValueError", "validate before comparing")'''),
    task(2, "Summary statistics",
         "Write `summarise(df)` returning a dictionary with keys `n` (rows), `mean` (mean score rounded to 2 dp), `median`, `pass_rate` (use `ra.pass_rate`, rounded to 3 dp) and `best_programme` (the programme with the highest **mean** score).",
         '''def summarise(df):
    # TODO: build and return the dictionary
    pass

records = ra.make_records()
print(summarise(records))''',
         '''def summarise(df):
    means = df.groupby("programme")["score"].mean()          # mean score per programme
    return {
        "n": int(len(df)),                                    # number of rows
        "mean": round(float(df["score"].mean()), 2),
        "median": float(df["score"].median()),
        "pass_rate": round(ra.pass_rate(df), 3),              # reuse the tested function
        "best_programme": str(means.idxmax()),                # label of the largest mean
    }

records = ra.make_records()
print(summarise(records))''',
         '''small = pd.DataFrame({"student_id": [1, 2, 3, 4], "programme": ["CS", "CS", "SE", "SE"], "score": [90, 30, 60, 70]})
s = summarise(small)
check(set(s) == {"n", "mean", "median", "pass_rate", "best_programme"}, "dictionary has the five keys", "use exactly these key names")
check(s["n"] == 4 and s["mean"] == 62.5 and s["median"] == 65.0, "n, mean, median", "mean=62.5, median=65.0")
check(s["pass_rate"] == 0.75 and s["best_programme"] == "SE", "pass_rate 0.75 and best programme SE", "SE mean 65 beats CS mean 60")
full = summarise(ra.make_records())
check(full["n"] == 30 and 25 <= full["mean"] <= 99, "works on the full generated table", "do not hard-code numbers")'''),
    task(3, "Mock practical: fix the seeded bugs",
         "The function `top_students(df, n)` should return the `n` students with the **highest** scores (highest first). The function `programme_counts(df)` should return a dictionary `{programme: number_of_students}`. Each has **one** bug. Find and fix them, then in `bug_report` explain each bug in one sentence (what was wrong, how you found it).",
         '''def top_students(df, n):
    return df.sort_values("score").head(n)                   # BUG somewhere in this line

def programme_counts(df):
    counts = {}
    for programme in df["programme"]:
        counts[programme] = 1                                # BUG somewhere in this line
    return counts

bug_report = []   # TODO: two strings, one per bug

probe = pd.DataFrame({"student_id": [1, 2, 3], "programme": ["CS", "CS", "SE"], "score": [50, 90, 70]})
print(top_students(probe, 2)["score"].tolist(), programme_counts(probe))''',
         '''def top_students(df, n):
    return df.sort_values("score", ascending=False).head(n)  # FIX: sort descending so the highest come first

def programme_counts(df):
    counts = {}
    for programme in df["programme"]:
        counts[programme] = counts.get(programme, 0) + 1     # FIX: add 1 to the running count instead of resetting to 1
    return counts

bug_report = [
    "top_students sorted ascending, so it returned the lowest scores; I found it because probe scores came back as [50, 70] instead of [90, 70].",
    "programme_counts set every count to 1 instead of adding to it; I found it because CS should be 2 but the dictionary showed 1.",
]

probe = pd.DataFrame({"student_id": [1, 2, 3], "programme": ["CS", "CS", "SE"], "score": [50, 90, 70]})
print(top_students(probe, 2)["score"].tolist(), programme_counts(probe))''',
         '''probe = pd.DataFrame({"student_id": [1, 2, 3], "programme": ["CS", "CS", "SE"], "score": [50, 90, 70]})
check(top_students(probe, 2)["score"].tolist() == [90, 70], "top_students returns the highest scores, highest first", "sort_values(..., ascending=False)")
check(top_students(probe, 10)["score"].tolist() == [90, 70, 50], "n larger than the table is handled", "head(n) already handles this")
check(programme_counts(probe) == {"CS": 2, "SE": 1}, "programme_counts counts correctly", "increase the existing count with counts.get(key, 0) + 1")
check(isinstance(bug_report, list) and len(bug_report) == 2 and all(len(b.split()) >= 8 for b in bug_report), "two bug explanations written", "one sentence per bug: what was wrong and how you found it")'''),
    task(4, "Write the README",
         "Assign to `readme` a Markdown string for **your own** version of the project. It must contain the headings `# `, `## Purpose`, `## Installation`, `## Usage`, `## Testing`, `## Limitations` and `## Author` (your name, matric number, department).",
         '''readme = """
# TODO project title

## Purpose
TODO

"""
print(readme)''',
         '''readme = """# Student Records Analyser

## Purpose
Generates, validates, stores (SQLite) and summarises fictional student records for CSC 333.

## Installation
Python 3.11 or later. Install the libraries with: pip install numpy pandas matplotlib pytest

## Usage
    import records_app as ra
    df = ra.make_records()          # reproducible data (seed=42)
    print(ra.pass_rate(df))

## Testing
    pytest -q

## Limitations
The data are synthetic and scores are whole numbers from 25 to 99. No real student data are used.

## Author
Ada Student, Matric No. 20/0000, Department of Computer Science, Olabisi Onabanjo University
"""
print(readme)''',
         '''needed = ["# ", "## Purpose", "## Installation", "## Usage", "## Testing", "## Limitations", "## Author"]
missing = [h for h in needed if h not in readme]
check(not missing, "README has all required headings", f"missing: {missing}")
check(len(readme.split()) >= 60 and "TODO" not in readme, "README is complete (60+ words, no TODO)", "replace every TODO with real content")'''),
    task(5, "Plan a 5-minute demonstration",
         "Create `demo_plan`: a list of **at least 5** `(step, minutes)` tuples (for example `(\"Show the problem and the data\", 1)`). The total must be **at most 5 minutes** and must include a step that mentions `test` and a step that mentions `limitation`.",
         '''demo_plan = [
    # ("Introduce the problem", 1),
]
print(sum(m for _, m in demo_plan))''',
         '''demo_plan = [
    ("Introduce the problem and the data", 1),
    ("Run the program live and explain one key function line by line", 1.5),
    ("Show the database round trip", 0.5),
    ("Run the tests and show one test catching a broken function", 1),
    ("State two limitations and what you would improve next", 1),
]
print(sum(m for _, m in demo_plan))                           # 5.0''',
         '''text = " ".join(s.lower() for s, _ in demo_plan)
check(len(demo_plan) >= 5 and all(isinstance(t, tuple) and len(t) == 2 for t in demo_plan), "at least five (step, minutes) tuples", "write tuples like (\\"Run the tests\\", 1)")
check(0 < sum(m for _, m in demo_plan) <= 5, "total time is at most 5 minutes", "adjust the minutes")
check("test" in text and "limitation" in text, "includes testing and limitations", "mention both in step descriptions")'''),
    task(6, "Reflection (honest and specific)",
         "Assign to `reflection` a dictionary with keys `strongest_skill`, `hardest_concept`, `next_step` and `evidence`. Each value must be a full sentence (at least 8 words). `evidence` must point to **something you actually produced** (a task, test, or bug you fixed).",
         '''reflection = {
    "strongest_skill": "",
    "hardest_concept": "",
    "next_step": "",
    "evidence": "",
}''',
         '''reflection = {
    "strongest_skill": "I can now break a problem into small functions and test each one with boundary cases.",
    "hardest_concept": "Understanding NumPy broadcasting and when a shape mismatch is a bug rather than a feature.",
    "next_step": "I will practise one Pandas groupby exercise each day for two weeks using a new dataset.",
    "evidence": "In the mock practical I found that programme_counts reset the count to 1 and fixed it with counts.get.",
}''',
         '''keys = {"strongest_skill", "hardest_concept", "next_step", "evidence"}
check(set(reflection) == keys, "four keys present", "use exactly these key names")
check(all(len(str(v).split()) >= 8 for v in reflection.values()), "each answer is a full sentence", "write at least 8 words per answer")'''),
    quiz([
        ("Why does a README matter if the code already works?", "Because someone else (a marker, teammate, or you in six months) must know how to install, run and test it, and what its limits are."),
        ("A test passes on correct code. How do you know the test is *good*?", "A good test also fails when the code is broken. Try deliberately breaking the function (or use boundary and invalid inputs) and confirm the test catches it."),
        ("Where do bugs most often hide in selection and loops?", "At boundaries: `>` vs `>=`, off-by-one in ranges, and the first or last element."),
        ("Why use `seed=42` in an assessed project?", "So that anyone running the code obtains the same data and results, making your work reproducible and checkable."),
    ]),
    assignment(
        "**Final Project (individual).** Extend the Student Records Analyser into your own mini-application of about 150 lines. You may keep the student-records theme or choose a different **fictional or openly licensed** dataset.\n\nSubmit in your GitHub repository:\n1. `app.py` (or a module) with at least **5 functions**, every line explained in comments\n2. `test_app.py` with at least **8 tests** (normal, boundary, invalid)\n3. `README.md` with all required headings\n4. One saved chart (`.png`) with title and labelled axes\n5. This notebook with all tasks completed\n\nIn the cell below, record your submission details and a self-assessment against the marking guide.",
        '''submission = {
    "repository_url": "",         # TODO: link to your GitHub repository
    "function_count": 0,          # TODO: number of functions in your app
    "test_count": 0,              # TODO: number of tests
    "uses_sqlite": False,         # TODO: True / False
    "ai_or_help_declared": "",    # TODO: who/what helped you? Write "none" if no help
}
print(submission)''',
        '''submission = {
    "repository_url": "https://github.com/your-username/csc333-final-project",
    "function_count": 6,
    "test_count": 9,
    "uses_sqlite": True,
    "ai_or_help_declared": "none; I discussed the design with a classmate but wrote all code myself.",
}
print(submission)''',
        '''check(str(submission["repository_url"]).startswith("https://github.com/"), "repository link looks valid", "paste your GitHub repository URL")
check(isinstance(submission["function_count"], int) and submission["function_count"] >= 5, "at least 5 functions", "add functions")
check(isinstance(submission["test_count"], int) and submission["test_count"] >= 8, "at least 8 tests", "add normal, boundary and invalid tests")
check(isinstance(submission["uses_sqlite"], bool) and len(str(submission["ai_or_help_declared"]).split()) >= 1, "SQLite flag and help declaration completed", "declare any help honestly; write none if none")'''),
]


def build():
    return build_week(12, "integrated_project_and_review", "Integrated Project, Testing, Documentation and Review",
                      OUTCOMES, ITEMS)
