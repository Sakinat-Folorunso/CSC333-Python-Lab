from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Create NumPy arrays and inspect `shape`, `ndim`, `size` and `dtype`.",
    "Index and slice 1-D and 2-D arrays, including Boolean masks.",
    "Replace Python loops with **vectorised** operations and explain why they are faster.",
    "Explain and use **broadcasting** and axis-wise aggregation (`axis=0`, `axis=1`).",
    "Generate reproducible random data with `np.random.default_rng(42)` and perform simple matrix operations.",
]

ITEMS = [
    md("""## 1. Why NumPy?
Python lists are flexible but slow for numbers, because each item is a full Python object. **NumPy** stores numbers in one compact block of memory and runs the maths in fast compiled code.

| | Python `list` | NumPy `ndarray` |
|---|---|---|
| Item types | anything, mixed | **one type** (e.g. all `int64` or all `float64`) |
| `x * 2` | repeats the list | doubles **every number** |
| Maths on a million numbers | slow loop | one fast operation |
| Dimensions | nested lists (awkward) | built-in 1-D, 2-D, 3-D ... |

### Key vocabulary
| Word | Meaning |
|---|---|
| **ndarray** | NumPy's array object |
| **shape** | size along each dimension: `(3, 4)` = 3 rows, 4 columns |
| **ndim** | number of dimensions (1 for a list-like, 2 for a table) |
| **dtype** | data type of the items |
| **axis** | direction of an operation: `axis=0` goes **down the rows** (one result per column); `axis=1` goes **across the columns** (one result per row) |
| **vectorisation** | applying an operation to a whole array at once, with no Python loop |
| **broadcasting** | NumPy's rule for combining arrays of different shapes (e.g. a row added to every row of a matrix) |

### Axis picture (for a table with students in rows, tests in columns)
```
              test1 test2 test3
 student A  [  70    75    80 ]   → axis=1 (across) gives A's average
 student B  [  65    72    78 ]
 student C  [  88    91    85 ]
                ↓
              axis=0 (down) gives each test's average
```

### Broadcasting rule (simple version)
Compare shapes **from the right**. Two dimensions are compatible if they are **equal** or **one of them is 1**. A dimension of size 1 is “stretched” to match.
"""),
    demo('''# --- DEMO 1: list versus ndarray ------------------------------------------------
import numpy as np                              # np is the universal nickname for NumPy

py_list = [1, 2, 3]                             # an ordinary Python list
arr = np.array([1, 2, 3])                       # build a NumPy array from the list
print(py_list * 2)                              # [1, 2, 3, 1, 2, 3]  : lists REPEAT
print(arr * 2)                                  # [2 4 6]             : arrays do MATHS on every item
print(arr + arr)                                # [2 4 6]             : element-by-element addition
print(type(arr), arr.dtype)                     # <class 'numpy.ndarray'> int64 (all items share one type)'''),
    demo('''# --- DEMO 2: creating arrays and inspecting them -------------------------------------
a = np.array([68, 75, 82, 91, 77])              # from a list
print(a.shape, a.ndim, a.size, a.dtype)         # (5,) 1 5 int64
print(np.arange(0, 10, 2))                      # like range: [0 2 4 6 8]
print(np.zeros(3))                              # [0. 0. 0.]  three zeros (floats)
print(np.ones((2, 3)))                          # 2 rows x 3 columns of ones
print(np.linspace(0, 1, 5))                     # 5 evenly spaced numbers from 0 to 1 (both included)
print(np.full((2, 2), 7))                       # 2 x 2 filled with 7
m = np.arange(12).reshape(3, 4)                 # numbers 0..11 rearranged into 3 rows x 4 columns
print(m)                                        # show the 2-D array
print(m.shape, m.ndim, m.size)                  # (3, 4) 2 12'''),
    demo('''# --- DEMO 3: indexing and slicing in 2-D ---------------------------------------------
marks = np.array([[70, 75, 80],                 # student 0
                  [65, 72, 78],                 # student 1
                  [88, 91, 85]])                # student 2
print(marks[0, 0])                              # row 0, column 0 -> 70  (note the single [row, col] style)
print(marks[1])                                 # the whole row 1 -> [65 72 78]
print(marks[:, 2])                              # ALL rows, column 2 -> [80 78 85]  (":" means "everything")
print(marks[0:2, 1:])                           # rows 0-1, columns 1 to the end -> [[75 80] [72 78]]
print(marks[-1, -1])                            # last row, last column -> 85
marks_copy = marks.copy()                       # slices are VIEWS (shared memory); copy() makes it independent
marks_copy[0, 0] = 0                            # change the copy only
print(marks[0, 0], marks_copy[0, 0])            # 70 0'''),
    demo('''# --- DEMO 4: vectorisation versus a Python loop ---------------------------------------------
import time                                     # to measure how long each version takes

big = np.arange(1_000_000)                      # one million numbers (1_000_000 : underscores aid reading)
start = time.perf_counter()                     # stopwatch on
squares_loop = [x * x for x in big]             # Python loop: one multiplication at a time
loop_time = time.perf_counter() - start         # stopwatch off
start = time.perf_counter()
squares_vec = big * big                         # VECTORISED: the whole array in one operation
vec_time = time.perf_counter() - start
print(f"loop {loop_time:.4f}s  vectorised {vec_time:.4f}s")   # exact numbers vary by computer
print("same answers:", np.array_equal(squares_loop, squares_vec))   # True: only the SPEED differs'''),
    demo('''# --- DEMO 5: broadcasting -------------------------------------------------------------------
scores = np.array([60, 70, 80])                 # shape (3,)
print(scores + 5)                               # a scalar is stretched to every item -> [65 75 85]
table = np.array([[1, 2, 3],
                  [4, 5, 6]])                   # shape (2, 3)
row = np.array([10, 20, 30])                    # shape (3,)
print(table + row)                              # the row is added to EACH row -> [[11 22 33] [14 25 36]]
col = np.array([[100], [200]])                  # shape (2, 1): a column vector
print(table + col)                              # the column is added to each COLUMN -> [[101 102 103] [204 205 206]]
print((np.array([[1], [2], [3]]) * np.array([1, 2, 3, 4])).shape)   # (3,1) * (4,) -> a (3,4) multiplication table'''),
    demo('''# --- DEMO 6: aggregation and the axis argument ------------------------------------------------
print(marks.sum(), marks.mean(), marks.max())   # whole table: total, average, largest
print(marks.mean(axis=1))                       # across columns -> one average PER STUDENT: [75. 71.67 88.]
print(marks.mean(axis=0))                       # down rows -> one average PER TEST: [74.33 79.33 81.]
print(marks.argmax(axis=1))                     # position of each student's best test: [2 2 1]
print(np.round(marks.std(axis=0), 2))           # spread of each test (population std, ddof=0 by default)
print(np.sort(marks[:, 0]))                     # sorted copy of the first test column: [65 70 88]'''),
    demo('''# --- DEMO 7: Boolean masks, np.where, np.clip ------------------------------------------------------
s = np.array([35, 48, 52, 67, 90, 41])          # six scores
mask = s >= 50                                  # element-wise comparison -> [False False True True True False]
print(mask)
print(s[mask])                                  # keep only the items where the mask is True -> [52 67 90]
print(mask.sum(), mask.mean())                  # True counts as 1: how many passed (3), what fraction (0.5)
print(np.where(s >= 50, "Pass", "Fail"))        # choose between two values for every item
print(np.clip(s + 10, 0, 100))                  # add 10 marks but never exceed 100'''),
    demo('''# --- DEMO 8: reproducible random numbers ---------------------------------------------------------------
rng = np.random.default_rng(42)                 # a random generator with a FIXED seed (42)
print(rng.integers(40, 100, size=8))            # eight whole numbers between 40 and 99
rng2 = np.random.default_rng(42)                # same seed again ...
print(rng2.integers(40, 100, size=8))           # ... gives EXACTLY the same numbers: reproducible science
temps = rng.normal(loc=30, scale=2, size=5)     # 5 numbers from a normal distribution: mean 30, std 2
print(np.round(temps, 1))                       # rounded for display'''),
    demo('''# --- DEMO 9: transpose and matrix multiplication ---------------------------------------------------------
A = np.array([[1, 2, 3],
              [4, 5, 6]])                       # shape (2, 3)
B = np.array([[1, 0],
              [0, 1],
              [2, 2]])                          # shape (3, 2)
print(A.T)                                      # transpose: rows become columns, shape (3, 2)
print(A @ B)                                    # matrix product: inner sizes (3 and 3) must match -> shape (2, 2)
print((A @ B).shape)                            # (2, 2): outer sizes of the two shapes
print(A * A)                                    # NOTE: * is element-by-element, NOT matrix multiplication'''),
    activity(
        "Axis detective",
        "For `m = [[1, 2, 3], [4, 5, 6]]` (shape 2 × 3) predict `m.sum(axis=0)`, `m.sum(axis=1)` and `m.sum()`. Think: *which direction collapses?*",
        '''m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m.sum(axis=0))
print(m.sum(axis=1))
print(m.sum())''',
        "`[5 7 9]`, `[ 6 15]`, `21`. `axis=0` collapses the **rows** (adds down each column, giving 3 results); `axis=1` collapses the **columns** (adds across each row, giving 2 results); no axis adds everything."),
    activity(
        "Will it broadcast?",
        "For each pair of shapes, predict `OK` or `error`: (3,4)+(4,) · (3,4)+(3,) · (3,4)+(3,1). Then run.",
        '''a = np.ones((3, 4))
for other_shape in [(4,), (3,), (3, 1)]:
    try:
        result = a + np.ones(other_shape)
        print(other_shape, "OK ->", result.shape)
    except ValueError as err:
        print(other_shape, "error:", err)''',
        "`(4,)` OK (compared from the right: 4 = 4). `(3,)` **error** (compared from the right: 4 vs 3, neither is 1). `(3, 1)` OK (the 1 is stretched to 4). Always compare shapes **from the right**."),
    md("""## 🛠️ Tasks
All arrays here use **fictional** data. Use `np.allclose(a, b)` (not `==`) to compare decimal arrays in your own tests.
"""),
    task(1, "Per-student and per-test averages",
         "Given a 2-D array `marks` (rows = students, columns = tests) write `student_means(marks)` and `test_means(marks)` using the `axis` argument, each rounded to 2 decimal places (`np.round`). **No loops.**",
         '''import numpy as np

def student_means(marks):
    # TODO
    pass

def test_means(marks):
    # TODO
    pass

marks = np.array([[70, 75, 80], [65, 72, 78], [88, 91, 85]])
print(student_means(marks), test_means(marks))''',
         '''import numpy as np

def student_means(marks):
    return np.round(marks.mean(axis=1), 2)         # across the columns: one mean per student

def test_means(marks):
    return np.round(marks.mean(axis=0), 2)         # down the rows: one mean per test

marks = np.array([[70, 75, 80], [65, 72, 78], [88, 91, 85]])
print(student_means(marks), test_means(marks))     # [75. 71.67 88.] [74.33 79.33 81.]''',
         '''marks = np.array([[70, 75, 80], [65, 72, 78], [88, 91, 85]])
check(np.allclose(student_means(marks), [75.0, 71.67, 88.0]), "student means", "marks.mean(axis=1)")
check(np.allclose(test_means(marks), [74.33, 79.33, 81.0]), "test means", "marks.mean(axis=0)")'''),
    task(2, "Temperature statistics",
         "Write `temp_stats(temps)` returning a dictionary with the keys `min`, `max`, `mean` and `std` (population standard deviation, NumPy's default), each as a **Python float** rounded to 2 dp.",
         '''def temp_stats(temps):
    # TODO
    pass

daily = np.array([29.5, 31.2, 30.1, 28.7, 32.4, 30.8, 29.9])
print(temp_stats(daily))''',
         '''def temp_stats(temps):
    return {
        "min": round(float(temps.min()), 2),        # float() turns NumPy's number into a plain Python float
        "max": round(float(temps.max()), 2),
        "mean": round(float(temps.mean()), 2),
        "std": round(float(temps.std()), 2),        # ddof=0 (population) is NumPy's default
    }

daily = np.array([29.5, 31.2, 30.1, 28.7, 32.4, 30.8, 29.9])
print(temp_stats(daily))''',
         '''daily = np.array([29.5, 31.2, 30.1, 28.7, 32.4, 30.8, 29.9])
r = temp_stats(daily)
check(set(r) == {"min", "max", "mean", "std"}, "four keys", "keys: min, max, mean, std")
check(r["min"] == 28.7 and r["max"] == 32.4, "min and max", "use .min() and .max()")
check(r["mean"] == 30.37 and r["std"] == 1.12, "mean and std", "mean 30.37, population std 1.12")
check(all(type(v) is float for v in r.values()), "plain Python floats", "wrap with float(...)")'''),
    task(3, "Normalise values (z-scores)",
         "Write `normalise(x)` returning `(x - mean) / std`. If the standard deviation is `0` (all values equal) return an array of zeros of the same shape instead of dividing by zero.",
         '''def normalise(x):
    # TODO
    pass

print(normalise(np.array([10.0, 20.0, 30.0])))''',
         '''def normalise(x):
    std = x.std()                                   # spread of the data
    if std == 0:                                    # all values identical: z-scores would be 0/0
        return np.zeros_like(x, dtype=float)        # same shape, filled with 0.0
    return (x - x.mean()) / std                     # vectorised: broadcasting subtracts/divides every item

print(normalise(np.array([10.0, 20.0, 30.0])))      # [-1.2247  0.  1.2247]''',
         '''z = normalise(np.array([10.0, 20.0, 30.0]))
check(np.allclose(z, [-1.22474487, 0.0, 1.22474487]), "z-scores of 10, 20, 30", "(x - x.mean()) / x.std()")
check(abs(z.mean()) < 1e-9 and abs(z.std() - 1) < 1e-9, "mean 0 and std 1", "this is what normalisation means")
check(np.array_equal(normalise(np.array([5.0, 5.0, 5.0])), np.zeros(3)), "constant array gives zeros", "handle std == 0 before dividing")'''),
    task(4, "Safe matrix multiplication",
         "Write `multiply_checked(a, b)` that returns `a @ b` but first verifies the dimensions: if `a.shape[1] != b.shape[0]` raise `ValueError` with a message containing both shapes.",
         '''def multiply_checked(a, b):
    # TODO
    pass

A = np.ones((2, 3)); B = np.ones((3, 4))
print(multiply_checked(A, B))   # expected: a 2 x 4 array of 3.0''',
         '''def multiply_checked(a, b):
    if a.shape[1] != b.shape[0]:                    # inner dimensions must agree
        raise ValueError(f"Cannot multiply shapes {a.shape} and {b.shape}")
    return a @ b                                    # matrix product

A = np.ones((2, 3)); B = np.ones((3, 4))
print(multiply_checked(A, B).shape)                 # (2, 4)''',
         '''A = np.ones((2, 3)); B = np.ones((3, 4))
check(multiply_checked(A, B).shape == (2, 4) and multiply_checked(A, B)[0, 0] == 3, "valid product", "return a @ b")
try:
    multiply_checked(B, B); raised = None
except ValueError as e:
    raised = str(e)
check(raised is not None and "(3, 4)" in raised, "bad shapes raise ValueError mentioning the shapes", "raise ValueError(f'... {a.shape} ... {b.shape}')")'''),
    task(5, "Pass counts and curving with masks",
         "Write `count_passes(scores, threshold=50)` (how many scores are at least the threshold) and `curve(scores, bonus)` (add `bonus` marks to everyone but never exceed 100). Use Boolean masks and `np.clip`; no loops.",
         '''def count_passes(scores, threshold=50):
    # TODO
    pass

def curve(scores, bonus):
    # TODO
    pass

s = np.array([35, 48, 52, 67, 90, 41])
print(count_passes(s), curve(s, 15))''',
         '''def count_passes(scores, threshold=50):
    return int((scores >= threshold).sum())         # the mask counts True as 1; int() gives a plain integer

def curve(scores, bonus):
    return np.clip(scores + bonus, 0, 100)          # add the bonus to all, then cap at 100

s = np.array([35, 48, 52, 67, 90, 41])
print(count_passes(s), curve(s, 15))                # 3 [ 50  63  67  82 100  56]''',
         '''s = np.array([35, 48, 52, 67, 90, 41])
check(count_passes(s) == 3 and count_passes(s, 40) == 5, "count_passes", "(scores >= threshold).sum()")
check(np.array_equal(curve(s, 15), [50, 63, 67, 82, 100, 56]), "curve is capped at 100", "np.clip(scores + bonus, 0, 100)")
check(np.array_equal(s, [35, 48, 52, 67, 90, 41]), "original array not modified", "do not use += on the input")'''),
    task(6, "Extension: reproducible synthetic dataset",
         "Write `make_scores(seed, n=30)` returning `n` integer scores between 40 and 99 using `np.random.default_rng(seed)`. The **same seed must give the same data**. Then write `describe_scores(scores)` returning `(mean, median, std)` rounded to 2 dp.",
         '''def make_scores(seed, n=30):
    # TODO
    pass

def describe_scores(scores):
    # TODO
    pass

data = make_scores(42)
print(data)
print(describe_scores(data) if data is not None else 'finish make_scores first')''',
         '''def make_scores(seed, n=30):
    rng = np.random.default_rng(seed)               # generator fixed by the seed
    return rng.integers(40, 100, size=n)            # upper bound is EXCLUDED, so 40..99

def describe_scores(scores):
    return (round(float(scores.mean()), 2),         # average
            round(float(np.median(scores)), 2),     # middle value
            round(float(scores.std()), 2))          # spread

data = make_scores(42)
print(data[:5], describe_scores(data))''',
         '''d1, d2, d3 = make_scores(42), make_scores(42), make_scores(7)
check(np.array_equal(d1, d2), "same seed, same data", "create the generator INSIDE the function from the seed")
check(not np.array_equal(d1, d3), "different seed, different data", "pass the seed to default_rng")
check(len(d1) == 30 and d1.min() >= 40 and d1.max() <= 99, "30 scores in 40..99", "rng.integers(40, 100, size=n)")
m, med, sd = describe_scores(d1)
check(40 <= m <= 99 and 40 <= med <= 99 and sd > 0, "summary looks sensible", "return (mean, median, std)")'''),
    quiz([
        ("What does `ndarray.shape` return?", "A tuple with the size of each dimension, e.g. `(3, 4)` for 3 rows and 4 columns."),
        ("What does `axis=0` mean for a two-dimensional array?", "The operation runs down the rows, giving one result per column."),
        ("What is vectorisation?", "Applying an operation to a whole array at once instead of looping item by item, which is shorter and much faster."),
        ("Why is `A * B` not matrix multiplication?", "`*` multiplies matching items one by one; matrix multiplication uses `A @ B`."),
    ]),
    assignment(
        "**A.** Write `row_col_means(a)` for any 2-D array: return `(row_means, column_means)`, each rounded to 2 dp. Test it on a 5 × 4 array made from `np.arange(20).reshape(5, 4)`.\n\n**B.** In the dictionary `numpy_notes` explain `vectorisation` and `broadcasting` with a small example each.\n\n**C.** In `list_or_numpy` give one situation where a plain Python list is enough (`list_is_enough`) and one where NumPy is clearly better (`numpy_is_better`).",
        '''def row_col_means(a):
    # TODO
    pass

numpy_notes = {"vectorisation": "", "broadcasting": ""}
list_or_numpy = {"list_is_enough": "", "numpy_is_better": ""}

grid = np.arange(20).reshape(5, 4)
print(row_col_means(grid))''',
        '''def row_col_means(a):
    return np.round(a.mean(axis=1), 2), np.round(a.mean(axis=0), 2)    # (one per row, one per column)

numpy_notes = {
    "vectorisation": "Applying an operation to a whole array at once, e.g. scores + 5 adds 5 to every score without a loop.",
    "broadcasting": "NumPy stretches a smaller array to match a larger one, e.g. adding a row [10, 20, 30] to every row of a 2 x 3 table.",
}
list_or_numpy = {
    "list_is_enough": "Storing the names of five students that I read one by one: a small list of text.",
    "numpy_is_better": "Computing the average and standard deviation of a million sensor readings, where vectorised arrays are far faster.",
}

grid = np.arange(20).reshape(5, 4)
print(row_col_means(grid))                          # row means [1.5 5.5 9.5 13.5 17.5], column means [8. 9. 10. 11.]''',
        '''grid = np.arange(20).reshape(5, 4)
rm, cm = row_col_means(grid)
check(np.allclose(rm, [1.5, 5.5, 9.5, 13.5, 17.5]) and np.allclose(cm, [8, 9, 10, 11]), "row and column means", "axis=1 for rows, axis=0 for columns")
check(all(len(v.split()) >= 8 for v in numpy_notes.values()), "both notes written with an example", "write a full sentence with an example")
check(all(len(v.split()) >= 6 for v in list_or_numpy.values()), "both situations described", "describe a concrete situation")'''),
]


def build():
    return build_week(9, "numerical_computing_numpy", "Numerical Computing with NumPy",
                      OUTCOMES, ITEMS)
