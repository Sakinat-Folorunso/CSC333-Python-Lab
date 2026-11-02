from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Detect missing values, duplicates, wrong types, impossible values and inconsistent categories.",
    "Apply a **justified** cleaning workflow and keep a decision log of row counts before and after each step.",
    "Create clear, labelled charts (histogram, bar chart) with Matplotlib.",
    "Read and write **CSV** and **JSON** files, and perform **SQLite** CRUD operations with **parameterised queries**.",
    "Write automated tests (normal, boundary and invalid cases) and run them with `pytest`.",
]

ITEMS = [
    md("""## 1. Real data is messy
Data collected by people and machines contains **missing values, duplicates, typing mistakes, impossible numbers and inconsistent labels** (`"CS"`, `"cs "`, `"Computer Science"`). Models and charts built on messy data give wrong answers confidently, so cleaning is not optional.

### A defensible cleaning workflow
1. **Look first, change later:** `info()`, `isna().sum()`, `duplicated().sum()`, `value_counts()`.
2. **Decide** what each problem means *in this dataset* (is a score of `150` a typo or a different scale?).
3. **Change** with a small, named step; **record** the decision and the **row count after each step**.
4. **Never overwrite the raw data.** Keep the original and work on a copy.

| Problem | Typical fixes | Risk to think about |
|---|---|---|
| Duplicate rows | `drop_duplicates()` | Are two identical rows really the *same* event? |
| Wrong type (`"70"` text) | `pd.to_numeric(..., errors="coerce")` | `"N/A"` silently becomes `NaN` |
| Inconsistent labels | `.str.strip().str.upper()` then `.map({...})` | Unmapped labels become `NaN`: check! |
| Impossible values | set to `NaN`, or drop, or flag | Dropping rows can bias the sample |
| Missing values | drop, fill (median/mean/mode), or flag | Filling shrinks variance; dropping may remove a *group* |

### Charts that communicate
Every chart needs a **title, labelled axes, and units**. Use a **histogram** for the *distribution* of one number, a **bar chart** to compare *categories*.

### Files and databases
| Format | Best for | Python |
|---|---|---|
| **CSV** | tables | `pandas.read_csv`, `to_csv` |
| **JSON** | nested records, settings, APIs | `json.dump`, `json.load` |
| **SQLite** | many records you must add, find, update, delete | `sqlite3` (built into Python) |

**CRUD** = **C**reate, **R**ead, **U**pdate, **D**elete → SQL `INSERT`, `SELECT`, `UPDATE`, `DELETE`.

### 🔐 Security: parameterised queries
Never build SQL by gluing user text into a string. Use **placeholders** (`?`) and pass the values separately. The database then treats them strictly as *data*, never as SQL commands. This blocks **SQL injection**, a top real-world attack.

```python
# UNSAFE (never do this)      : f"SELECT * FROM records WHERE name = '{name}'"
# SAFE (always do this)       : con.execute("SELECT * FROM records WHERE name = ?", (name,))
```

### Testing basics
A **test** is a small function that checks one behaviour with `assert`. Good tests cover **normal**, **boundary** and **invalid** inputs. `pytest` finds functions named `test_...` and runs them.
"""),
    demo('''# --- DEMO 1: a small, deliberately messy dataset (fictional) ------------------------------
import numpy as np
import pandas as pd

def messy_df():
    return pd.DataFrame({
        "student_id": [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11],            # note: id 5 appears twice
        "programme": ["CS", "cs ", " DS", "Data Science", "ICT", "ICT",   # inconsistent labels
                      "SE", "CS", "DS", "ICT", "SE", "CS"],
        "score": ["70", "55", "N/A", "88", "61", "61",                    # scores stored as TEXT; "N/A", "" , 150, -5 are problems
                  "150", "47", "", "72", "-5", "90"],
        "attendance": [90, 85, 70, None, 95, 95, 60, 88, 92, None, 80, 99],   # two missing values
    })

raw = messy_df()                                  # the RAW data: we will never modify this variable
print(raw)                                        # look at everything (it is small)'''),
    demo('''# --- DEMO 2: inspect before you clean --------------------------------------------------------
print(raw.shape)                                  # (12, 4)
print(raw.dtypes)                                 # score is object (text), not a number
print("Missing values per column:")
print(raw.isna().sum())                           # attendance has 2 true missing values (None -> NaN)
print("Exact duplicate rows:", raw.duplicated().sum())      # 1: the second copy of student 5
print(raw["programme"].value_counts())            # shows the inconsistent spellings
bad_text = raw[pd.to_numeric(raw["score"], errors="coerce").isna()]   # rows whose score cannot become a number
print(bad_text[["student_id", "score"]])          # N/A and an empty string'''),
    demo('''# --- DEMO 3: a cleaning pipeline WITH a decision log ----------------------------------------------
PROGRAMME_MAP = {"CS": "CS", "DS": "DS", "DATA SCIENCE": "DS", "ICT": "ICT", "SE": "SE"}   # agreed spellings

def clean_demo(raw):
    log = []                                                   # one entry per step: what we did and the effect
    def note(step, d):                                         # small helper to record row counts
        log.append({"step": step, "rows": len(d), "missing_scores": int(d["score"].isna().sum())})

    df = raw.copy()                                            # NEVER modify the raw data
    note("start", df)
    df = df.drop_duplicates()                                  # identical rows are the same record entered twice
    note("drop_duplicates", df)
    df["programme"] = df["programme"].str.strip().str.upper().map(PROGRAMME_MAP)   # tidy then map to official codes
    note("standardise_programme", df)
    df["score"] = pd.to_numeric(df["score"], errors="coerce")  # text -> number; "N/A" and "" become NaN
    note("coerce_scores", df)
    df.loc[(df["score"] < 0) | (df["score"] > 100), "score"] = np.nan   # impossible values: mark missing, keep the row
    note("invalid_to_nan", df)
    median = df["score"].median()                              # median is robust to extreme values
    df["score"] = df["score"].fillna(median)                   # fill remaining gaps with the median of VALID scores
    note("fill_median", df)
    return df, log

cleaned, log = clean_demo(raw)
for entry in log:
    print(entry)                                               # the row counts tell the story of each step
print(cleaned)'''),
    demo('''# --- DEMO 4: charts with Matplotlib ------------------------------------------------------------------
import matplotlib.pyplot as plt                   # the standard plotting module

fig, ax = plt.subplots(figsize=(6, 4))            # one figure with one set of axes (the drawing area)
ax.hist(cleaned["score"], bins=5, edgecolor="black")   # histogram: how are scores distributed?
ax.set_title("Distribution of cleaned scores")    # EVERY chart needs a title ...
ax.set_xlabel("Score (0-100)")                    # ... and labelled axes with units
ax.set_ylabel("Number of students")
fig.tight_layout()                                # stop labels overlapping
plt.show()                                        # display (in a script: also fig.savefig("hist.png"))

means = cleaned.groupby("programme")["score"].mean()   # one number per category -> a bar chart
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.bar(means.index, means.values)                # bar(x_labels, heights)
ax2.set_title("Average score by programme")
ax2.set_xlabel("Programme")
ax2.set_ylabel("Mean score")
ax2.set_ylim(0, 100)                              # an honest scale: start the axis at 0
fig2.tight_layout()
plt.show()'''),
    demo('''# --- DEMO 5: CSV and JSON files with pathlib ---------------------------------------------------------------
import json                                       # standard library: JSON reading/writing
from pathlib import Path                          # a modern, safe way to handle file paths

folder = Path("lab_output")                       # a folder name
folder.mkdir(exist_ok=True)                       # create it (no error if it already exists)
csv_path = folder / "cleaned_scores.csv"          # "/" joins path pieces on any operating system
cleaned.to_csv(csv_path, index=False)             # write the table
print(csv_path.exists(), csv_path.stat().st_size > 0)   # True True

settings = {"course": "CSC 333", "week": 11, "tags": ["cleaning", "sqlite"], "language": "Yorùbá"}
json_path = folder / "settings.json"
with open(json_path, "w", encoding="utf-8") as f:           # "with" closes the file automatically, even after an error
    json.dump(settings, f, ensure_ascii=False, indent=2)    # ensure_ascii=False keeps characters like "ù" readable
with open(json_path, encoding="utf-8") as f:                # always state the encoding
    loaded = json.load(f)
print(loaded == settings, loaded["language"])               # True Yorùbá  (a round trip)'''),
    demo('''# --- DEMO 6: SQLite CRUD with parameterised queries ---------------------------------------------------------
import sqlite3                                    # built into Python: no installation needed

con = sqlite3.connect(":memory:")                 # a temporary database in RAM (use "lab_records.db" for a real file)
with con:                                         # "with con" = one TRANSACTION: commit on success, roll back on error
    con.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id INTEGER PRIMARY KEY,        -- a unique number the database assigns
            name TEXT NOT NULL,                   -- a name is required
            score REAL                            -- a decimal number (may be empty)
        )
    """)
with con:                                         # CREATE a record: the ? placeholders receive the values safely
    con.execute("INSERT INTO records(name, score) VALUES (?, ?)", ("Amina", 82.5))
    con.execute("INSERT INTO records(name, score) VALUES (?, ?)", ("Tola", 60))
print(con.execute("SELECT record_id, name, score FROM records").fetchall())       # READ everything: a list of tuples
print(con.execute("SELECT name FROM records WHERE score > ?", (70,)).fetchone())  # READ one row: ('Amina',)
with con:                                         # UPDATE
    con.execute("UPDATE records SET score = ? WHERE name = ?", (65, "Tola"))
with con:                                         # DELETE
    con.execute("DELETE FROM records WHERE name = ?", ("Amina",))
print(con.execute("SELECT * FROM records").fetchall())                            # [(2, 'Tola', 65.0)]

evil = "x'); DROP TABLE records;--"               # what an attacker might type as a "name"
with con:
    con.execute("INSERT INTO records(name, score) VALUES (?, ?)", (evil, 1))      # stored as harmless TEXT
print(con.execute("SELECT COUNT(*) FROM records").fetchone())                     # (2,): the table still exists!
con.close()                                       # release the database when finished'''),
    demo('''%%writefile test_demo.py
# test_demo.py : pytest finds files named test_*.py and functions named test_*
def average(values):                              # the code under test (normally imported from your module)
    if not values:
        raise ValueError("empty list")
    return sum(values) / len(values)

def test_average_normal():                        # NORMAL case
    assert average([10, 20, 30]) == 20

def test_average_boundary():                      # BOUNDARY case: the smallest legal input
    assert average([7]) == 7

def test_average_invalid():                       # INVALID case: expect the error
    try:
        average([])
        assert False, "should have raised ValueError"
    except ValueError:
        pass'''),
    demo('''# --- DEMO 7: run the tests with pytest -------------------------------------------------------------------------
import pytest                                     # preinstalled in Colab; on your PC: pip install pytest
exit_code = pytest.main(["-q", "test_demo.py"])   # same as typing  pytest -q test_demo.py  in a terminal
print("pytest exit code:", int(exit_code))        # 0 means every test passed'''),
    activity(
        "Mean or median?",
        "A class of scores is `[55, 60, 62, 58, 61, 5]` (the 5 is a data-entry typo). Predict which fill value is more sensible for a *missing* score: the mean or the median? Then run.",
        '''import statistics
scores = [55, 60, 62, 58, 61, 5]
print("mean  :", round(statistics.mean(scores), 1))
print("median:", statistics.median(scores))''',
        "Mean 50.2, median 59.0. The single typo pulls the **mean** far below every real score, so filling a gap with the mean would invent a score nobody got. The **median** is robust to extreme values. (Better still: investigate the typo first. Filling *all* gaps with one number also hides real variation.)"),
    activity(
        "Why does the injection fail?",
        "Run the cell and explain why the table survives even though the name looks like SQL.",
        '''con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE people (name TEXT)")
attack = "Bob'); DROP TABLE people;--"
con.execute("INSERT INTO people(name) VALUES (?)", (attack,))     # parameterised
print(con.execute("SELECT name FROM people").fetchall())
print(con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
unsafe_sql = f"INSERT INTO people(name) VALUES ('{attack}')"      # we only PRINT the unsafe text; we never run it
print(unsafe_sql)''',
        "The placeholder sends `attack` to the database as a **value**, so it is stored as ordinary text and the table `people` is still there. The unsafe version pastes the text *into the SQL command*, so the quote `'` ends the string early and `DROP TABLE` would become part of the command. That is SQL injection. **Rule:** values go in parameters, never inside the SQL string."),
    md("""## 🛠️ Tasks
The datasets are **fictional**. Use the `messy_df()` function from Demo 1 to get a fresh copy of the raw data.
"""),
    task(1, "Clean the dataset and log every step",
         "Write `clean_scores(raw)` returning `(clean_df, log)`. Perform **exactly** these steps in order, appending a log entry `{\"step\", \"rows\", \"missing_scores\"}` after each (`missing_scores` = number of `NaN` in the `score` column at that moment):\n\n1. `start` · 2. `drop_duplicates` · 3. `standardise_programme` (strip, upper-case, map with `PROGRAMME_MAP`) · 4. `coerce_scores` (`pd.to_numeric(errors=\"coerce\")`) · 5. `invalid_to_nan` (scores below 0 or above 100) · 6. `fill_median` (median of the remaining valid scores).\n\nThe **raw data must not be changed.**",
         '''PROGRAMME_MAP = {"CS": "CS", "DS": "DS", "DATA SCIENCE": "DS", "ICT": "ICT", "SE": "SE"}

def clean_scores(raw):
    log = []
    def note(step, d):
        log.append({"step": step, "rows": len(d), "missing_scores": int(d["score"].isna().sum())})

    df = raw.copy()
    note("start", df)
    # TODO 2: drop duplicates, then note("drop_duplicates", df)
    # TODO 3: standardise programme, then note("standardise_programme", df)
    # TODO 4: coerce scores to numbers, then note("coerce_scores", df)
    # TODO 5: out-of-range scores -> NaN, then note("invalid_to_nan", df)
    # TODO 6: fill remaining NaN scores with the median, then note("fill_median", df)
    return df, log

cleaned_df, decision_log = clean_scores(messy_df())
for entry in decision_log:
    print(entry)''',
         '''PROGRAMME_MAP = {"CS": "CS", "DS": "DS", "DATA SCIENCE": "DS", "ICT": "ICT", "SE": "SE"}   # agreed official codes

def clean_scores(raw):
    log = []                                                   # decision log
    def note(step, d):
        log.append({"step": step, "rows": len(d), "missing_scores": int(d["score"].isna().sum())})

    df = raw.copy()                                            # protect the raw data
    note("start", df)
    df = df.drop_duplicates()                                  # step 2
    note("drop_duplicates", df)
    df["programme"] = df["programme"].str.strip().str.upper().map(PROGRAMME_MAP)   # step 3
    note("standardise_programme", df)
    df["score"] = pd.to_numeric(df["score"], errors="coerce")  # step 4: text -> numbers
    note("coerce_scores", df)
    df.loc[(df["score"] < 0) | (df["score"] > 100), "score"] = np.nan   # step 5
    note("invalid_to_nan", df)
    df["score"] = df["score"].fillna(df["score"].median())    # step 6
    note("fill_median", df)
    return df, log

cleaned_df, decision_log = clean_scores(messy_df())
for entry in decision_log:
    print(entry)''',
         '''raw_check = messy_df()
c, lg = clean_scores(raw_check)
steps = [e["step"] for e in lg]
check(steps == ["start", "drop_duplicates", "standardise_programme", "coerce_scores", "invalid_to_nan", "fill_median"], "log has the six steps in order", "append a note() after each step with the exact step names")
check([e["rows"] for e in lg] == [12, 11, 11, 11, 11, 11], "row counts: 12 then 11", "only drop_duplicates removes a row")
check([e["missing_scores"] for e in lg] == [0, 0, 0, 2, 4, 0], "missing scores 0,0,0,2,4,0", "N/A and empty become NaN first; then 150 and -5")
check(set(c["programme"].unique()) == {"CS", "DS", "ICT", "SE"} and c["score"].isna().sum() == 0, "programmes standardised, no missing scores", "map with PROGRAMME_MAP; fillna(median)")
check(float(c.loc[c["student_id"] == 3, "score"].iloc[0]) == 70.0, "gaps filled with the median of VALID scores (70)", "compute the median AFTER invalid values became NaN")
check(len(raw_check) == 12 and raw_check["score"].iloc[2] == "N/A", "raw data untouched", "start with raw.copy()")'''),
    task(2, "Two honest charts",
         "Write `plot_score_hist(df, path)` and `plot_programme_means(df, path)`. Each must create a figure, give it a **title, x-label and y-label**, save it to `path` with `fig.savefig(path)` and **return the figure**. The bar chart must draw **one bar per programme**.",
         '''import matplotlib.pyplot as plt
import os

def plot_score_hist(df, path):
    # TODO: histogram of df["score"], with title and axis labels; save and return the figure
    pass

def plot_programme_means(df, path):
    # TODO: bar chart of the mean score per programme; title, labels; save and return the figure
    pass

sample = pd.DataFrame({"programme": ["CS", "DS", "CS", "ICT"], "score": [70, 80, 60, 90]})
f1 = plot_score_hist(sample, "hist.png")
plt.show()''',
         '''import matplotlib.pyplot as plt
import os

def plot_score_hist(df, path):
    fig, ax = plt.subplots(figsize=(6, 4))                   # new figure and axes
    ax.hist(df["score"], bins=5, edgecolor="black")          # distribution of one number
    ax.set_title("Distribution of scores")                   # title
    ax.set_xlabel("Score (0-100)")                           # labelled axes with units
    ax.set_ylabel("Number of students")
    fig.tight_layout()
    fig.savefig(path)                                        # save to a file
    return fig

def plot_programme_means(df, path):
    means = df.groupby("programme")["score"].mean()          # one value per programme
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(means.index, means.values)                        # one bar per category
    ax.set_title("Average score by programme")
    ax.set_xlabel("Programme")
    ax.set_ylabel("Mean score")
    ax.set_ylim(0, 100)                                      # honest axis from 0
    fig.tight_layout()
    fig.savefig(path)
    return fig

sample = pd.DataFrame({"programme": ["CS", "DS", "CS", "ICT"], "score": [70, 80, 60, 90]})
f1 = plot_score_hist(sample, "hist.png")
plt.show()''',
         '''sample = pd.DataFrame({"programme": ["CS", "DS", "CS", "ICT"], "score": [70, 80, 60, 90]})
f1 = plot_score_hist(sample, "hist_check.png")
f2 = plot_programme_means(sample, "bar_check.png")
a1, a2 = f1.axes[0], f2.axes[0]
check(os.path.exists("hist_check.png") and os.path.exists("bar_check.png"), "both files were saved", "call fig.savefig(path)")
check(all(a.get_title().strip() and a.get_xlabel().strip() and a.get_ylabel().strip() for a in (a1, a2)), "titles and axis labels present", "use set_title, set_xlabel, set_ylabel")
check(len(a2.patches) == 3, "bar chart has one bar per programme (3)", "ax.bar(means.index, means.values)")
check(len(a1.patches) >= 2, "histogram drew bars", "ax.hist(df['score'], bins=5)")'''),
    task(3, "SQLite CRUD with parameterised queries",
         "Complete the five functions. **Use `?` placeholders for every value.** `add_record` returns the new `record_id`; `get_record` returns a tuple `(record_id, name, score)` or `None`; `update_score` and `delete_record` return `True` only if a row was changed.",
         '''import sqlite3

def create_table(con):
    # TODO: CREATE TABLE IF NOT EXISTS records (record_id INTEGER PRIMARY KEY, name TEXT NOT NULL, score REAL)
    pass

def add_record(con, name, score):
    # TODO: INSERT using ? placeholders; return the new id (cursor.lastrowid)
    pass

def get_record(con, record_id):
    # TODO: SELECT ... WHERE record_id = ?  ->  fetchone()
    pass

def update_score(con, record_id, score):
    # TODO: UPDATE ... ; return cursor.rowcount > 0
    pass

def delete_record(con, record_id):
    # TODO: DELETE ... ; return cursor.rowcount > 0
    pass

db = sqlite3.connect(":memory:")
create_table(db)
print(add_record(db, "Amina", 82.5))''',
         '''import sqlite3

def create_table(con):
    with con:                                                # transaction: commit automatically
        con.execute("""
            CREATE TABLE IF NOT EXISTS records (
                record_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score REAL
            )
        """)

def add_record(con, name, score):
    with con:
        cur = con.execute("INSERT INTO records(name, score) VALUES (?, ?)", (name, score))   # values travel separately
    return cur.lastrowid                                     # id assigned by the database

def get_record(con, record_id):
    return con.execute("SELECT record_id, name, score FROM records WHERE record_id = ?", (record_id,)).fetchone()

def update_score(con, record_id, score):
    with con:
        cur = con.execute("UPDATE records SET score = ? WHERE record_id = ?", (score, record_id))
    return cur.rowcount > 0                                  # rowcount = number of rows changed

def delete_record(con, record_id):
    with con:
        cur = con.execute("DELETE FROM records WHERE record_id = ?", (record_id,))
    return cur.rowcount > 0

db = sqlite3.connect(":memory:")
create_table(db)
print(add_record(db, "Amina", 82.5))                         # 1''',
         '''con = sqlite3.connect(":memory:")
create_table(con); create_table(con)                          # running twice must be harmless (IF NOT EXISTS)
i1 = add_record(con, "Amina", 82.5); i2 = add_record(con, "Tola", 60)
check(i1 != i2 and get_record(con, i1) == (i1, "Amina", 82.5), "create and read", "return cursor.lastrowid; fetchone() gives a tuple")
check(get_record(con, 999) is None, "missing record gives None", "fetchone() returns None when nothing matches")
check(update_score(con, i2, 65) is True and get_record(con, i2)[2] == 65 and update_score(con, 999, 1) is False, "update", "rowcount > 0 means a row changed")
check(delete_record(con, i1) is True and get_record(con, i1) is None and delete_record(con, i1) is False, "delete", "second delete finds nothing")
evil = "x'); DROP TABLE records;--"
j = add_record(con, evil, 1)
check(get_record(con, j)[1] == evil and con.execute("SELECT COUNT(*) FROM records").fetchone()[0] == 2, "SQL injection attempt stored as plain text; table intact", "never build SQL with f-strings: use ? placeholders")'''),
    task(4, "Validate, then test",
         "Write `validate_score(value)`: return the score as a **float** if it is a number (or numeric text such as `\"85.5\"`) between 0 and 100 **inclusive**; otherwise raise `ValueError` (this includes `None`, `\"abc\"`, `\"\"`, `-1`, `101`). Then write `test_validate_score()` containing **at least one normal, two boundary and three invalid** assertions. A good test also catches *broken* code: your test will be run against a faulty validator.",
         '''def validate_score(value):
    # TODO: convert with float(); convert TypeError/ValueError into ValueError; check the 0..100 range
    pass

def raises_value_error(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False

def test_validate_score():
    # TODO: normal case, e.g.  assert validate_score(70) == 70.0
    # TODO: boundary cases: 0 and 100
    # TODO: invalid cases, e.g.  assert raises_value_error(validate_score, 101)
    pass

test_validate_score()
print("tests finished")''',
         '''def validate_score(value):
    try:
        number = float(value)                                # accepts 70, 85.5 and "85.5"
    except (TypeError, ValueError):                          # None -> TypeError, "abc" -> ValueError
        raise ValueError(f"Not a number: {value!r}")         # one consistent error type for the caller
    if not 0 <= number <= 100:                               # also rejects NaN, because comparisons with NaN are False
        raise ValueError(f"Score out of range: {number}")
    return number

def raises_value_error(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False

def test_validate_score():
    assert validate_score(70) == 70.0                        # NORMAL
    assert validate_score("85.5") == 85.5                    # NORMAL (text input)
    assert validate_score(0) == 0.0                          # BOUNDARY: lowest legal
    assert validate_score(100) == 100.0                      # BOUNDARY: highest legal
    assert raises_value_error(validate_score, -1)            # INVALID: just below
    assert raises_value_error(validate_score, 101)           # INVALID: just above
    assert raises_value_error(validate_score, "abc")         # INVALID: not a number
    assert raises_value_error(validate_score, None)          # INVALID: missing

test_validate_score()
print("tests finished")''',
         '''check(validate_score(70) == 70.0 and validate_score("85.5") == 85.5 and type(validate_score(70)) is float, "valid scores accepted as floats", "return float(value)")
check(validate_score(0) == 0.0 and validate_score(100) == 100.0, "boundaries 0 and 100 are valid", "use 0 <= number <= 100")
check(all(raises_value_error(validate_score, bad) for bad in (-1, 101, "abc", None, "")), "invalid inputs raise ValueError", "wrap float() in try/except and re-raise ValueError")
real = validate_score
test_validate_score()
validate_score = lambda v: float(v)                      # a deliberately BROKEN validator (no range check)
try:
    test_validate_score(); caught_bug = False
except AssertionError:
    caught_bug = True
finally:
    validate_score = real
check(caught_bug, "your tests catch a broken validator", "add invalid and boundary assertions such as assert raises_value_error(validate_score, 101)")'''),
    task(5, "JSON round trip",
         "Write `save_json(data, path)` and `load_json(path)` using `pathlib.Path`, `json` and **UTF-8**. The saved file must keep characters like `ù` readable (`ensure_ascii=False`).",
         '''import json
from pathlib import Path

def save_json(data, path):
    # TODO: open with encoding="utf-8" and json.dump(..., ensure_ascii=False, indent=2)
    pass

def load_json(path):
    # TODO
    pass

save_json({"language": "Yorùbá"}, "demo.json")
print(load_json("demo.json"))''',
         '''import json
from pathlib import Path

def save_json(data, path):
    with open(Path(path), "w", encoding="utf-8") as f:       # "with" closes the file safely
        json.dump(data, f, ensure_ascii=False, indent=2)     # keep accents readable; indent for humans

def load_json(path):
    with open(Path(path), encoding="utf-8") as f:
        return json.load(f)

save_json({"language": "Yorùbá"}, "demo.json")
print(load_json("demo.json"))''',
         '''payload = {"language": "Yorùbá", "scores": [70, 82, 91], "week": 11}
save_json(payload, "roundtrip.json")
check(load_json("roundtrip.json") == payload, "round trip returns identical data", "dump then load with the same encoding")
check("Yorùbá" in Path("roundtrip.json").read_text(encoding="utf-8"), "accented text stored readably", "json.dump(..., ensure_ascii=False)")'''),
    task(6, "Extension: data-quality report",
         "Write `quality_report(before, after)` returning a dictionary with `rows_before`, `rows_after`, `missing_before`, `missing_after` (total number of missing cells in the whole table). Then explain in `bias_note` **how one cleaning decision could bias the analysis** (2 sentences).",
         '''def quality_report(before, after):
    # TODO
    pass

bias_note = ""   # TODO

c, _ = clean_scores(messy_df())
print(quality_report(messy_df(), c))''',
         '''def quality_report(before, after):
    return {
        "rows_before": int(len(before)),
        "rows_after": int(len(after)),
        "missing_before": int(before.isna().sum().sum()),     # NaN in every cell, summed twice (columns, then total)
        "missing_after": int(after.isna().sum().sum()),
    }

bias_note = ("Filling every missing score with the median pulls those students towards the middle, which shrinks "
             "the spread and can hide very weak or very strong students. If the missing scores are not random "
             "(for example, absent students), the cleaned data will also misrepresent the class.")

c, _ = clean_scores(messy_df())
print(quality_report(messy_df(), c))''',
         '''a = pd.DataFrame({"x": [1, None, 3], "y": [None, None, 6]})
b = pd.DataFrame({"x": [1, 2], "y": [5, 6]})
check(quality_report(a, b) == {"rows_before": 3, "rows_after": 2, "missing_before": 3, "missing_after": 0}, "report values", "df.isna().sum().sum() counts missing cells")
check(len(bias_note.split()) >= 25, "bias note written", "explain one decision and its effect in 2 sentences")'''),
    quiz([
        ("What is a duplicate record?", "A row that repeats the same information as another row, usually from entering or exporting the same record twice."),
        ("When might dropping missing values be inappropriate?", "When the missing values are not random (e.g. one group is missing more often) or when dropping would remove too many rows; it can bias results."),
        ("Why use a context manager (`with`) for a database connection or file?", "It guarantees the transaction is committed or rolled back and files are closed even when an error occurs. (For SQLite use `with con:` for the transaction and call `con.close()` when finished.)"),
        ("What is the purpose of a parameterised query?", "It sends user values separately from the SQL command so they can never be executed as SQL, which prevents SQL injection."),
    ]),
    assignment(
        "**A.** In `why_parameterised` explain (2 to 3 sentences) why parameterised SQL is safer than building SQL with string concatenation.\n\n**B.** In `mean_fill_risks` describe **two** risks of filling *all* missing numeric values with the mean.\n\n**C.** In `test_plan` write at least **six** test cases for a function `validate_record(record)` that checks a student record dictionary (`student_id`, `name`, `score`). Each entry is a string such as `\"normal: valid record -> accepted\"`. Include normal, boundary and invalid cases.",
        '''why_parameterised = ""      # TODO
mean_fill_risks = []        # TODO: a list of two strings
test_plan = []              # TODO: a list of six or more strings, e.g. "normal: ... -> ..."

print(len(test_plan))''',
        '''why_parameterised = ("With parameterised queries the SQL command and the user's values travel separately, so the database "
                     "treats the values only as data. If you join strings instead, a user can type SQL code that becomes part "
                     "of the command, which is SQL injection and can leak or destroy data.")

mean_fill_risks = [
    "The mean is pulled by extreme values, so the filled number may not represent a typical student.",
    "Filling every gap with the same number reduces the natural variation in the data and makes later statistics look more certain than they are.",
]

test_plan = [
    "normal: id=1, name='Ada', score=70 -> accepted",
    "boundary: score=0 -> accepted",
    "boundary: score=100 -> accepted",
    "invalid: score=-1 -> rejected with ValueError",
    "invalid: score=101 -> rejected with ValueError",
    "invalid: score='abc' -> rejected with ValueError",
    "invalid: missing 'name' key -> rejected with an error message",
    "invalid: empty name '' -> rejected",
]

print(len(test_plan))                                       # 8''',
        '''check(len(why_parameterised.split()) >= 25, "explanation written", "2 to 3 sentences")
check(isinstance(mean_fill_risks, list) and len(mean_fill_risks) == 2 and all(len(r.split()) >= 8 for r in mean_fill_risks), "two risks described", "a list of exactly two sentences")
low = [t.lower() for t in test_plan]
check(len(test_plan) >= 6 and sum("normal" in t for t in low) >= 1 and sum("boundary" in t for t in low) >= 2 and sum("invalid" in t for t in low) >= 3, "plan has normal, boundary (2+) and invalid (3+) cases", "label each case: normal / boundary / invalid")'''),
]


def build():
    return build_week(11, "cleaning_visualisation_files_sqlite", "Data Cleaning, Visualisation, File Processing and Introductory SQLite",
                      OUTCOMES, ITEMS)
