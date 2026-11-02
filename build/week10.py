from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Create and inspect `Series` and `DataFrame` objects, and load a CSV file with `pd.read_csv()`.",
    "Select columns and rows with `[]`, `loc` and `iloc`, and filter rows with Boolean conditions.",
    "Sort data and create **derived columns**.",
    "Summarise data with `describe()`, `value_counts()`, `groupby()` and `agg()`.",
    "Export a filtered subset to a CSV file and explain what each step of your analysis answers.",
]

ITEMS = [
    md("""## 1. From arrays to labelled tables
NumPy arrays are fast but anonymous: you must remember that column 2 means *score*. **Pandas** adds **labels** and a spreadsheet-like view.

| Structure | Dimensions | Picture | Created with |
|---|---|---|---|
| **Series** | 1-D | one labelled column | `pd.Series([...])` |
| **DataFrame** | 2-D | a whole table of Series sharing one row index | `pd.DataFrame({...})`, `pd.read_csv("file.csv")` |

```
          student_id   programme    score    ← columns (each one is a Series)
  0       S001         Data Science  78
  1       S002         ICT           64      ← rows (the left numbers are the index)
```

### Your analysis toolkit
| Question | Tool |
|---|---|
| How big is it? What types? | `df.shape`, `df.dtypes`, `df.info()` |
| First look | `df.head()`, `df.tail()` |
| Quick statistics | `df.describe()` |
| One column / several columns | `df["score"]`, `df[["student_id", "score"]]` |
| Rows by label / by position | `df.loc[...]` / `df.iloc[...]` |
| Rows that satisfy a condition | `df[df["score"] >= 70]` |
| Order the rows | `df.sort_values("score", ascending=False)` |
| New column | `df["pass_status"] = ...` |
| Counts of each category | `df["programme"].value_counts()` |
| Summaries per group | `df.groupby("programme")["score"].agg(["count", "mean", "max"])` |
| Save | `df.to_csv("out.csv", index=False)` |

### `loc` vs `iloc`
- `loc` uses **labels** (`df.loc[3, "score"]`: row *labelled* 3, column named score). The end of a `loc` slice is **included**.
- `iloc` uses **positions** like NumPy (`df.iloc[3, 2]`: 4th row, 3rd column). The end of an `iloc` slice is **excluded**.

### Combining conditions
Use `&` (and), `|` (or), `~` (not) and put **each condition in brackets**: `df[(df["score"] >= 50) & (df["programme"] == "ICT")]`. The words `and` / `or` do **not** work on Series.

### Ethics note
Real student, patient or customer records are personal data. In this course we use **synthetic (made-up) data** only.
"""),
    demo('''# --- DEMO 1: a Series ---------------------------------------------------------------
import numpy as np                                   # numerical tools
import pandas as pd                                  # pd is the universal nickname for pandas

marks = pd.Series([70, 55, 88], index=["Amina", "Tola", "Chika"])   # values with LABELS (an index)
print(marks)                                         # shows labels, values and the dtype
print(marks["Tola"])                                 # access by label: 55
print(marks.iloc[0])                                 # access by position: 70
print(marks + 5)                                     # vectorised, like NumPy: every value gets +5
print(marks.mean(), marks.idxmax())                  # 71.0 and the LABEL of the largest value: Chika'''),
    demo('''# --- DEMO 2: a DataFrame from a dictionary of lists ------------------------------------
data = {                                             # each key becomes a COLUMN name
    "student": ["Amina", "Tola", "Chika", "Bola"],
    "programme": ["CS", "DS", "CS", "ICT"],
    "score": [78, 91, 67, 84],
}
small = pd.DataFrame(data)                           # build the table
print(small)                                         # the whole table (the left numbers are the row index)
print(small.shape)                                   # (4, 3): 4 rows, 3 columns
print(list(small.columns))                           # ['student', 'programme', 'score']
print(small["score"].mean())                         # 80.0 : pick one column, then summarise it
print(small[small["score"] >= 80])                   # filter: only rows where the condition is True'''),
    md("""### Our practice dataset
The next cell **creates a synthetic file** `student_scores.csv` (60 fictional students, seed 42) and then reads it back with `read_csv()`, exactly as you would with a downloaded file. Because the seed is fixed, **everyone gets identical data**.
"""),
    demo('''# --- DEMO 3: create and load the practice dataset -------------------------------------------
def make_student_scores(path="student_scores.csv", n=60, seed=42):
    rng = np.random.default_rng(seed)                # reproducible random generator
    programmes = ["Computer Science", "Data Science", "Cyber Security", "Software Engineering", "ICT"]
    table = pd.DataFrame({
        "student_id": [f"S{i:03d}" for i in range(1, n + 1)],      # S001, S002, ... (fictional IDs)
        "programme": rng.choice(programmes, size=n),                # a random programme for each student
        "course": rng.choice(["CSC 331", "CSC 333", "DTS 201"], size=n),
        "score": rng.integers(30, 100, size=n),                     # whole-number scores 30..99
        "attendance": rng.integers(50, 101, size=n),                # attendance percentage 50..100
    })
    table.to_csv(path, index=False)                  # save as CSV; index=False avoids an extra "Unnamed" column
    return table

make_student_scores()                                # create the file on disk
df = pd.read_csv("student_scores.csv")               # LOAD it back: this is how real data arrives
print(df.head())                                     # first 5 rows
print(df.shape)                                      # (60, 5)'''),
    demo('''# --- DEMO 4: first inspection ---------------------------------------------------------------------
df.info()                                            # columns, non-null counts and dtypes (prints by itself)
print(df.describe())                                 # count, mean, std, min, quartiles, max of the NUMBER columns
print(df.dtypes)                                     # type of every column: object (text) or int64
print(df["programme"].value_counts())                # how many students in each programme, largest first
print(df["course"].unique())                         # the distinct values in the course column'''),
    demo('''# --- DEMO 5: selecting columns and rows ---------------------------------------------------------------
print(df["score"].head(3))                           # ONE column -> a Series
print(df[["student_id", "score"]].head(3))           # SEVERAL columns -> a DataFrame (note the double brackets)
print(df.loc[0, "programme"])                        # label-based: row labelled 0, column "programme"
print(df.loc[0:2, ["student_id", "score"]])          # loc includes BOTH ends: rows 0, 1, 2
print(df.iloc[0:2, 0:3])                             # iloc excludes the end: rows 0-1, columns 0-2
print(df.iloc[-1])                                   # the last row'''),
    demo('''# --- DEMO 6: filtering with conditions ------------------------------------------------------------------
high = df[df["score"] >= 80]                         # one condition
print(len(high), "students scored 80 or more")
ds_pass = df[(df["programme"] == "Data Science") & (df["score"] >= 50)]   # TWO conditions: brackets + &
print(len(ds_pass))
either = df[(df["score"] < 40) | (df["attendance"] < 60)]                 # OR with |
print(len(either), "students at risk")
some = df[df["programme"].isin(["ICT", "Cyber Security"])]                # membership in a list
print(some["programme"].unique())
print(df[~(df["score"] >= 50)].shape[0], "failed")                        # ~ means NOT'''),
    demo('''# --- DEMO 7: sorting and derived columns --------------------------------------------------------------------
ranked = df.sort_values("score", ascending=False)    # a NEW table, best scores first (df itself is unchanged)
print(ranked[["student_id", "score"]].head(3))
work = df.copy()                                     # copy so we do not alter the original while experimenting
work["pass_status"] = np.where(work["score"] >= 50, "Pass", "Fail")   # DERIVED column: choose per row
work["score_pct"] = work["score"] / 100             # another derived column: score as a fraction
print(work[["student_id", "score", "pass_status"]].head(4))
print(work["pass_status"].value_counts())'''),
    demo('''# --- DEMO 8: groupby and aggregation ----------------------------------------------------------------------------
by_prog = df.groupby("programme")["score"].agg(["count", "mean", "max"])    # split -> apply -> combine
print(by_prog.round(2))                              # three statistics for every programme
print(df.groupby("course")["attendance"].mean().round(1))     # average attendance per course
best = by_prog["mean"].idxmax()                      # label (programme) with the highest mean
print("Highest average:", best)

report = df.groupby("programme").agg(                # several columns, with readable names
    students=("student_id", "count"),
    avg_score=("score", "mean"),
    avg_attendance=("attendance", "mean"),
).round(1)
print(report)'''),
    demo('''# --- DEMO 9: exporting results ----------------------------------------------------------------------------------------
top = df[df["score"] >= 90].sort_values("score", ascending=False)    # filter, then sort
top.to_csv("top_students.csv", index=False)          # write to a file; index=False keeps the file clean
check_back = pd.read_csv("top_students.csv")         # read it back to confirm it worked
print(check_back.shape, list(check_back.columns))
print(f"{len(top)} students with 90 or more were exported")'''),
    activity(
        "loc or iloc?",
        "Predict how many rows each selection returns from a table with the default index 0, 1, 2, ... Then run.",
        '''t = pd.DataFrame({"x": [10, 20, 30, 40, 50]})
print(len(t.loc[1:3]))     # label-based slice
print(len(t.iloc[1:3]))    # position-based slice
print(t.loc[1:3, "x"].tolist(), t.iloc[1:3, 0].tolist())''',
        "`3` and `2`. `loc[1:3]` includes **both** labels 1, 2, 3; `iloc[1:3]` excludes the end position (rows 1 and 2). Lists: `[20, 30, 40]` and `[20, 30]`."),
    activity(
        "Why brackets and `&`?",
        "Run the cell. One line is wrong on purpose; read the error message and fix it in the next cell.",
        '''ok = df[(df["score"] >= 50) & (df["attendance"] >= 75)]
print("with &:", len(ok))
try:
    bad = df[df["score"] >= 50 and df["attendance"] >= 75]   # "and" cannot compare whole Series
except ValueError as err:
    print("error ->", str(err)[:60], "...")''',
        "The first count works. The second raises *ValueError: The truth value of a Series is ambiguous* because Python's `and` wants a single True/False, not a whole column of them. **Use `&`, `|`, `~` with each condition in brackets.**"),
    md("""## 🛠️ Tasks
All tasks use the DataFrame `df` loaded above (each function receives it as an argument). **Check your answers by reasoning**, not just by running.
"""),
    task(1, "Overall statistics",
         "Write `overall_stats(df)` returning a dictionary: `records` (number of rows), `mean` (average score, 2 dp), `highest`, `lowest`. Use plain Python numbers (`int(...)`, `float(...)`).",
         '''def overall_stats(df):
    # TODO
    pass

print(overall_stats(df))''',
         '''def overall_stats(df):
    return {
        "records": int(len(df)),                       # number of rows
        "mean": round(float(df["score"].mean()), 2),   # average score
        "highest": int(df["score"].max()),
        "lowest": int(df["score"].min()),
    }

print(overall_stats(df))''',
         '''r = overall_stats(df)
scores = df["score"].tolist()
check(r["records"] == len(scores) == 60, "records", "len(df)")
check(r["highest"] == max(scores) and r["lowest"] == min(scores), "highest and lowest", "df['score'].max() / .min()")
check(abs(r["mean"] - round(sum(scores) / len(scores), 2)) < 1e-9, "mean", "round(df['score'].mean(), 2)")'''),
    task(2, "Average score by programme",
         "Write `mean_by_programme(df)` returning a Series of the **average score per programme, rounded to 2 dp, sorted from highest to lowest**.",
         '''def mean_by_programme(df):
    # TODO: groupby -> mean -> round -> sort_values
    pass

print(mean_by_programme(df))''',
         '''def mean_by_programme(df):
    means = df.groupby("programme")["score"].mean()    # split by programme, average each group
    return means.round(2).sort_values(ascending=False) # round, then largest first

print(mean_by_programme(df))''',
         '''res = mean_by_programme(df)
manual = {}
for p, s in zip(df["programme"], df["score"]):         # an independent calculation with a plain loop
    manual.setdefault(p, []).append(s)
manual = {p: round(sum(v) / len(v), 2) for p, v in manual.items()}
check(set(res.index) == set(manual), "one entry per programme", "group by 'programme'")
check(all(abs(res[p] - manual[p]) < 1e-9 for p in manual), "values match a manual calculation", "mean of 'score' for each group, rounded to 2 dp")
check(list(res.values) == sorted(res.values, reverse=True), "sorted high to low", "sort_values(ascending=False)")'''),
    task(3, "Pass status column",
         "Write `add_pass_status(df, threshold=50)` returning a **new** DataFrame with an extra column `pass_status` (`\"Pass\"` if score ≥ threshold else `\"Fail\"`). The original `df` must **not** be changed.",
         '''def add_pass_status(df, threshold=50):
    # TODO: copy first, then add the column
    pass

print(add_pass_status(df))   # after you finish, try  .head()  on this result''',
         '''def add_pass_status(df, threshold=50):
    out = df.copy()                                    # never change the caller's table
    out["pass_status"] = np.where(out["score"] >= threshold, "Pass", "Fail")   # choose per row
    return out

print(add_pass_status(df).head())''',
         '''new = add_pass_status(df)
check("pass_status" in new.columns and "pass_status" not in df.columns, "new column added, original untouched", "start with df.copy()")
check(((new["score"] >= 50) == (new["pass_status"] == "Pass")).all(), "status matches the rule", "score >= threshold means Pass")
check((add_pass_status(df, 70)["pass_status"] == "Pass").sum() == (df["score"] >= 70).sum(), "threshold argument works", "use the threshold parameter, not 50")
check(len(new) == len(df), "same number of rows", "do not drop any rows")'''),
    task(4, "Top N students",
         "Write `top_n(df, n, programme=None)` returning the top `n` rows by score (highest first; break ties by `student_id` ascending). If `programme` is given, consider only that programme.",
         '''def top_n(df, n, programme=None):
    # TODO: optional filter, then sort_values with two keys, then head(n)
    pass

print(top_n(df, 3))''',
         '''def top_n(df, n, programme=None):
    pool = df if programme is None else df[df["programme"] == programme]   # optional filter
    ordered = pool.sort_values(["score", "student_id"], ascending=[False, True])   # best first, ties by id
    return ordered.head(n)                              # keep the first n rows

print(top_n(df, 3))''',
         '''t = top_n(df, 5)
check(len(t) == 5 and t["score"].iloc[0] == df["score"].max(), "top 5 overall", "sort scores descending, then head(5)")
check(t["score"].is_monotonic_decreasing, "scores in descending order", "ascending=False for score")
p = top_n(df, 3, "ICT")
check(len(p) == 3 and (p["programme"] == "ICT").all(), "filtered by programme", "filter BEFORE sorting")
check(top_n(df, 1000).shape[0] == 60, "asking for more rows than exist is safe", "head(n) handles this")'''),
    task(5, "Export high scorers",
         "Write `export_high_scorers(df, path, cutoff=70)` that saves the rows with `score >= cutoff` to a CSV file (no index column) and **returns the number of rows written**.",
         '''def export_high_scorers(df, path, cutoff=70):
    # TODO
    pass

print(export_high_scorers(df, "high_scorers.csv"))''',
         '''def export_high_scorers(df, path, cutoff=70):
    subset = df[df["score"] >= cutoff]                 # choose the rows
    subset.to_csv(path, index=False)                   # write; index=False avoids a useless first column
    return len(subset)                                 # report how many rows were saved

print(export_high_scorers(df, "high_scorers.csv"))''',
         '''n = export_high_scorers(df, "high_scorers.csv", 70)
back = pd.read_csv("high_scorers.csv")
check(n == (df["score"] >= 70).sum(), "returned the right count", "return len(subset)")
check(len(back) == n and (back["score"] >= 70).all(), "file contains exactly the high scorers", "filter with df['score'] >= cutoff")
check(list(back.columns) == list(df.columns), "no extra 'Unnamed' index column", "to_csv(path, index=False)")'''),
    task(6, "Extension: questions the data can answer",
         "Write `attendance_score_corr(df)` returning the correlation between attendance and score, rounded to 3 dp (`Series.corr`). Then fill the list `my_questions` with **three useful questions** about this dataset that Pandas could answer (each ending in `?`) and answer one of them in code below the list.",
         '''def attendance_score_corr(df):
    # TODO
    pass

my_questions = [
    "",   # TODO question 1
    "",   # TODO question 2
    "",   # TODO question 3
]
print(attendance_score_corr(df))''',
         '''def attendance_score_corr(df):
    return round(float(df["attendance"].corr(df["score"])), 3)   # Pearson correlation between two columns

my_questions = [
    "Which programme has the highest average score?",
    "Do students with higher attendance score higher?",
    "What percentage of students in each course failed?",
]
print(attendance_score_corr(df))
# Answering question 3 in code:
fail_rate = (df["score"] < 50).groupby(df["course"]).mean().round(3) * 100
print(fail_rate)                                        # percentage failing per course''',
         '''c = attendance_score_corr(df)
check(isinstance(c, float) and -1 <= c <= 1 and abs(c - round(float(np.corrcoef(df["attendance"], df["score"])[0, 1]), 3)) < 1e-9, "correlation", "df['attendance'].corr(df['score'])")
check(len(my_questions) == 3 and all(q.strip().endswith("?") and len(q.split()) >= 4 for q in my_questions), "three real questions", "write full questions ending with ?")'''),
    quiz([
        ("What is a DataFrame?", "A two-dimensional labelled table whose columns are Series sharing the same row index."),
        ("What is the difference between `loc` and `iloc`?", "`loc` selects by label and includes the slice end; `iloc` selects by integer position and excludes the slice end."),
        ("What does `groupby()` enable?", "Splitting the table into groups, calculating something for each group, and combining the results (e.g. mean score per programme)."),
        ("Why must each condition be in brackets when using `&`?", "Because `&` binds tighter than comparison operators; without brackets Python evaluates in the wrong order and raises errors."),
    ]),
    assignment(
        "**A.** Write `build_df()` returning a DataFrame with **at least 8 rows and 4 columns**: `student`, `programme`, `score`, `level` (fictional data).\n\n**B.** Write `filter_and_group(df)` returning a tuple `(high, group_means)`: `high` = rows with `score >= 70`; `group_means` = Series of the mean score per programme.\n\n**C.** In the strings `series_vs_dataframe` and `info_vs_describe` explain (2 sentences each) *Series vs DataFrame* and *why `info()` and `describe()` give different information*.",
        '''def build_df():
    # TODO: return a DataFrame with >= 8 rows and the 4 required columns
    pass

def filter_and_group(df):
    # TODO
    pass

series_vs_dataframe = ""
info_vs_describe = ""

mine = build_df()
print(mine)''',
        '''def build_df():
    return pd.DataFrame({
        "student":   ["Ada", "Bola", "Chi", "Dayo", "Efe", "Funmi", "Gbenga", "Hauwa"],
        "programme": ["CS", "DS", "CS", "ICT", "DS", "SE", "ICT", "CS"],
        "score":     [78, 91, 67, 84, 55, 73, 49, 88],
        "level":     [300, 300, 200, 300, 400, 300, 200, 400],
    })

def filter_and_group(df):
    high = df[df["score"] >= 70]                        # rows with a high score
    group_means = df.groupby("programme")["score"].mean()   # mean score per programme
    return high, group_means

series_vs_dataframe = ("A Series is a single labelled column of values, while a DataFrame is a table made of several "
                       "Series that share the same row index.")
info_vs_describe = ("info() describes the structure of the table: column names, data types and how many values are "
                    "not missing. describe() calculates statistics such as mean, minimum and quartiles of the numeric columns.")

mine = build_df()
print(mine)''',
        '''mine = build_df()
check(mine.shape[0] >= 8 and {"student", "programme", "score", "level"} <= set(mine.columns), "DataFrame has 8+ rows and the 4 columns", "use a dictionary of 4 equal-length lists")
hi, gm = filter_and_group(mine)
check((hi["score"] >= 70).all() and len(hi) == (mine["score"] >= 70).sum(), "high scorers filtered", "mine[mine['score'] >= 70]")
check(set(gm.index) == set(mine["programme"]), "one mean per programme", "groupby('programme')['score'].mean()")
check(len(series_vs_dataframe.split()) >= 15 and len(info_vs_describe.split()) >= 15, "explanations written", "write 2 sentences each")'''),
]


def build():
    return build_week(10, "data_manipulation_pandas", "Data Manipulation and Analysis with Pandas",
                      OUTCOMES, ITEMS)
