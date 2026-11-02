from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Define and call functions with parameters, default arguments and return values.",
    "Explain local versus global scope and why returning values beats printing everywhere.",
    "Split a program into **modules**, and import user-defined and standard-library modules.",
    "Use `if __name__ == \"__main__\":` to control what runs on import.",
    "Write and trace **recursive** functions, identifying the base case and recursive case.",
]

ITEMS = [
    md("""## 1. Functions: name a piece of work once, use it many times
A **function** packages instructions under a name. You have already *used* functions (`print`, `len`); now you *write* them.

```python
def average(values):               # def + name + (parameters) + colon
    total = sum(values)            # the indented body
    return total / len(values)     # return sends a result BACK to the caller
```

| Word | Meaning |
|---|---|
| **parameter** | the variable name in the `def` line (`values`) |
| **argument** | the actual value you pass when calling (`average([4, 6])`) |
| **return value** | what the function gives back; if there is no `return`, it gives back `None` |
| **default argument** | a parameter with a preset value: `def power(x, n=2)` |
| **keyword argument** | passing by name: `power(x=3, n=4)` |

### Why `return` instead of `print`?
A function that **returns** can be reused, tested and combined (`round(average(x), 1)`). A function that only **prints** is a dead end.

### Scope
Variables created *inside* a function are **local**: invisible outside. Pass data in through parameters, get it out through `return`.

## 2. Modules and packages
- A **module** is just a `.py` file. A **package** is a folder of modules.
- `import math` → use `math.sqrt(9)`.
- `from math import sqrt` → use `sqrt(9)` directly.
- `import statistics as st` → give it a short alias.
- **Standard library** modules you will use: `math`, `random`, `statistics`, `datetime`, `collections`, `json`, `sqlite3`.
- `if __name__ == "__main__":` runs code **only when the file is executed directly**, not when it is imported. This lets one file be both a *tool* and a *program*.

## 3. Recursion: a function that calls itself
A recursive solution has two parts:
1. **Base case:** a situation simple enough to answer directly (stops the recursion).
2. **Recursive case:** reduce the problem to a *smaller* version and call yourself.

`factorial(4) = 4 × factorial(3) = 4 × 3 × factorial(2) = ... = 4 × 3 × 2 × 1`

Each call waits on the **call stack** (the same LIFO idea from Week 5!). With no reachable base case Python raises `RecursionError` (default depth about 1000).
"""),
    demo('''# --- DEMO 1: writing and calling functions -----------------------------------
def greet(name, greeting="Hello"):              # greeting has a DEFAULT value, so it is optional
    return f"{greeting}, {name}!"               # build the text and SEND IT BACK (no print here)

print(greet("Amina"))                           # uses the default: Hello, Amina!
print(greet("Tola", "Welcome"))                 # positional: second argument replaces the default
print(greet(greeting="Good day", name="Chika")) # keyword arguments: order does not matter when names are given

def stats(values):                              # a function can return SEVERAL values (a tuple)
    return min(values), max(values), sum(values) / len(values)

low, high, avg = stats([4, 8, 9])               # unpack the returned tuple into three variables
print(low, high, round(avg, 2))                 # 4 9 7.0

result = print("hi")                            # print() RETURNS None: it only displays
print(result)                                   # None'''),
    demo('''# --- DEMO 2: scope ---------------------------------------------------------------------
tax_rate = 0.075                                # a GLOBAL variable (defined outside any function)

def price_with_tax(price):
    total = price * (1 + tax_rate)              # a function may READ a global variable ...
    return round(total, 2)                      # ... and `total` is LOCAL: it dies when the function ends

print(price_with_tax(1000))                     # 1075.0
# print(total)                                  # NameError if uncommented: `total` does not exist out here

def bad_counter():
    count = 0                                   # local variable, created fresh on EVERY call
    count += 1
    return count

print(bad_counter(), bad_counter())             # 1 1 : the value is NOT remembered between calls'''),
    md("""### Creating our own module
We save a file called `utils.py` using the Colab `%%writefile` magic, then import it in the next cell. On your own computer you would simply create `utils.py` in VS Code and a `main.py` next to it.
"""),
    demo('''%%writefile utils.py
# utils.py : a small reusable module (the line above saves this cell as a file)

def calculate_average(values):
    """Return the mean of a list of numbers. Raises ValueError for an empty list."""
    if len(values) == 0:                        # protect against dividing by zero
        raise ValueError("At least one value is required")   # raise = signal an error on purpose
    return sum(values) / len(values)            # total divided by count

def factorial(n):
    """Return n! computed recursively."""
    if n < 0:                                   # factorial is not defined for negatives
        raise ValueError("n must be non-negative")
    if n in (0, 1):                             # BASE CASE: 0! = 1! = 1
        return 1
    return n * factorial(n - 1)                 # RECURSIVE CASE: n times the factorial of a smaller number

if __name__ == "__main__":                      # True only when you run `python utils.py` directly
    print("Running utils.py directly")          # skipped when another file imports utils
    print(factorial(5))                         # 120'''),
    demo('''# --- DEMO 3: importing our module and a standard-library module ---------------------
import math                                     # standard library: mathematics
import random                                   # standard library: random numbers
import statistics                               # standard library: mean, median, ...
from utils import calculate_average, factorial  # OUR module: take two names from utils.py

scores = [70, 82, 91]                           # sample data
print(calculate_average(scores))                # 81.0 (our function)
print(statistics.mean(scores))                  # 81 (the library's version gives the same idea)
print(factorial(5))                             # 120
print(math.sqrt(144), math.pi)                  # 12.0 3.141592653589793
random.seed(42)                                 # fix the "random" sequence so results are reproducible
print(random.randint(1, 6))                     # a repeatable die roll between 1 and 6'''),
    demo('''# --- DEMO 4: tracing recursion (printing every call) ------------------------------
def factorial_trace(n, depth=0):
    indent = "  " * depth                       # indentation shows how deep we are
    print(f"{indent}factorial({n}) called")     # entering the call
    if n <= 1:                                  # base case
        print(f"{indent}-> base case, returns 1")
        return 1
    answer = n * factorial_trace(n - 1, depth + 1)   # wait for the smaller problem to finish
    print(f"{indent}-> returns {answer}")       # leaving the call with the finished value
    return answer

factorial_trace(4)                              # watch the calls go DOWN, then the answers come back UP'''),
    demo('''# --- DEMO 5: iteration versus recursion --------------------------------------------------
def factorial_loop(n):                          # the iterative (loop) version
    result = 1                                  # accumulator
    for i in range(2, n + 1):                   # multiply 2 * 3 * ... * n
        result *= i
    return result

def factorial_rec(n):                           # the recursive version
    return 1 if n <= 1 else n * factorial_rec(n - 1)

print(factorial_loop(6), factorial_rec(6))      # 720 720 : same answer
def countdown(n):                               # a second recursive pattern: do something, then recurse
    if n == 0:                                  # base case
        print("Go!")
        return
    print(n)                                    # work for this level
    countdown(n - 1)                            # smaller problem

countdown(3)                                    # 3 2 1 Go!'''),
    activity(
        "Print or return?",
        "What does each line print? What is the value of `x` and of `y` at the end?",
        '''def double_print(n):
    print(n * 2)

def double_return(n):
    return n * 2

x = double_print(4)
y = double_return(4)
print(x, y)''',
        "First `8` is printed by the call inside `double_print`; then `print(x, y)` shows `None 8`. `double_print` gave back `None` because it had no `return`, so `x` is useless in later calculations, while `y` is a real number we can reuse."),
    activity(
        "Trace recursion by hand",
        "Without running: what does `mystery(3)` return? Draw the calls on paper.",
        '''def mystery(n):
    if n == 0:
        return 0
    return n + mystery(n - 1)

print(mystery(3))''',
        "`6`. `mystery(3) = 3 + mystery(2) = 3 + 2 + mystery(1) = 3 + 2 + 1 + mystery(0) = 3 + 2 + 1 + 0`. It adds the integers from 1 to n: the base case `n == 0` stops the calls."),
    md("""## 🛠️ Tasks
"""),
    task(1, "Utility functions",
         "Write `average(values)`, `value_range(values)` (max minus min) and `classify(score)` returning `\"Distinction\"` (70+), `\"Merit\"` (60–69), `\"Pass\"` (50–59), `\"Fail\"` (below 50). Return values; do **not** print inside them.",
         '''def average(values):
    # TODO
    pass

def value_range(values):
    # TODO
    pass

def classify(score):
    # TODO
    pass

print(average([2, 4, 9]), value_range([2, 4, 9]), classify(65))''',
         '''def average(values):
    return sum(values) / len(values)            # total / count

def value_range(values):
    return max(values) - min(values)            # spread of the data

def classify(score):
    if score >= 70:
        return "Distinction"
    elif score >= 60:
        return "Merit"
    elif score >= 50:
        return "Pass"
    return "Fail"                               # nothing above matched

print(average([2, 4, 9]), value_range([2, 4, 9]), classify(65))   # 5.0 7 Merit''',
         '''check(average([2, 4, 9]) == 5, "average", "sum / len")
check(value_range([2, 4, 9]) == 7, "range", "max - min")
check([classify(s) for s in (75, 65, 55, 40)] == ["Distinction", "Merit", "Pass", "Fail"], "classify bands", "70, 60, 50 are the boundaries")'''),
    task(2, "Recursive sum and GCD",
         "Write `sum_to(n)` = 1 + 2 + ... + n (recursive; `sum_to(0)` is 0) and `gcd(a, b)` using **Euclid's algorithm**: `gcd(a, 0) = a`, otherwise `gcd(b, a % b)`.",
         '''def sum_to(n):
    # TODO: base case, then recursive case
    pass

def gcd(a, b):
    # TODO
    pass

print(sum_to(4), gcd(48, 18))''',
         '''def sum_to(n):
    if n == 0:                                  # base case
        return 0
    return n + sum_to(n - 1)                    # n plus the sum of everything smaller

def gcd(a, b):
    if b == 0:                                  # base case: nothing left to divide
        return a
    return gcd(b, a % b)                        # Euclid: replace (a, b) by (b, a mod b)

print(sum_to(4), gcd(48, 18))                   # 10 6''',
         '''check(sum_to(4) == 10 and sum_to(0) == 0 and sum_to(100) == 5050, "sum_to", "base case n == 0; else n + sum_to(n-1)")
check(gcd(48, 18) == 6 and gcd(7, 13) == 1 and gcd(10, 0) == 10, "gcd", "gcd(a, 0) = a; else gcd(b, a % b)")'''),
    task(3, "Your own module",
         "Cell A creates a module file `temperature.py`. Complete `celsius_to_fahrenheit(c)` (`c * 9/5 + 32`) and `fahrenheit_to_celsius(f)`. Cell B imports it and tests. *(On your own PC, create the two files in VS Code instead.)*",
         '''%%writefile temperature.py
# temperature.py : temperature conversion module

def celsius_to_fahrenheit(c):
    # TODO: return the Fahrenheit value
    pass

def fahrenheit_to_celsius(f):
    # TODO: return the Celsius value
    pass''',
         '''%%writefile temperature.py
# temperature.py : temperature conversion module

def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32                       # standard formula

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9                     # inverse formula (brackets first!)''',
         '''import importlib, temperature                      # import the file we just wrote
importlib.reload(temperature)                      # pick up edits if you re-run this cell
check(temperature.celsius_to_fahrenheit(100) == 212, "100 C = 212 F", "c * 9 / 5 + 32")
check(temperature.fahrenheit_to_celsius(32) == 0, "32 F = 0 C", "(f - 32) * 5 / 9")
check(round(temperature.fahrenheit_to_celsius(temperature.celsius_to_fahrenheit(37)), 6) == 37, "round trip works", "the two functions must be inverses")'''),
    task(4, "Recursive binary search (extension)",
         "Write `binary_search_rec(items, target, low, high)` on a **sorted** list: return the index of `target` or `-1`. Base case: `low > high` means not found. Compare with the middle item and recurse on the correct half.",
         '''def binary_search_rec(items, target, low, high):
    # TODO: base case, find the middle, compare, recurse
    pass

data = [3, 8, 12, 19, 25, 31]
print(binary_search_rec(data, 19, 0, len(data) - 1))''',
         '''def binary_search_rec(items, target, low, high):
    if low > high:                               # base case 1: empty search range -> not found
        return -1
    mid = (low + high) // 2                      # middle index
    if items[mid] == target:                     # base case 2: found it
        return mid
    if items[mid] < target:                      # target is in the right half
        return binary_search_rec(items, target, mid + 1, high)
    return binary_search_rec(items, target, low, mid - 1)   # otherwise the left half

data = [3, 8, 12, 19, 25, 31]
print(binary_search_rec(data, 19, 0, len(data) - 1))        # 3''',
         '''d = [3, 8, 12, 19, 25, 31]
check(binary_search_rec(d, 19, 0, 5) == 3, "finds 19 at index 3", "compare with items[mid] and recurse on one half")
check(binary_search_rec(d, 3, 0, 5) == 0 and binary_search_rec(d, 31, 0, 5) == 5, "first and last items", "mid + 1 / mid - 1")
check(binary_search_rec(d, 20, 0, 5) == -1 and binary_search_rec([], 1, 0, -1) == -1, "missing / empty gives -1", "base case: low > high")'''),
    quiz([
        ("What is the difference between a parameter and an argument?", "A parameter is the name in the function definition; an argument is the actual value passed in a call."),
        ("What is a base case?", "The simplest situation the function answers directly without calling itself; it stops the recursion."),
        ("Why split a program into modules?", "Reuse, organisation, easier testing and teamwork; each file has one clear job."),
        ("What happens if a recursive function has no reachable base case?", "It keeps calling itself until Python raises `RecursionError` (maximum depth exceeded)."),
    ]),
    assignment(
        "**A.** Write `recursive_sum(values)` (a list) using recursion only (no loops, no `sum`). Base case: empty list.\n\n**B.** Write a second recursive function `power(base, exp)` for non-negative integer `exp`.\n\n**C.** In `recursion_vs_iteration` compare recursion and iteration in 2 to 3 sentences.",
        '''def recursive_sum(values):
    # TODO: base case = empty list; otherwise first item + sum of the rest
    pass

def power(base, exp):
    # TODO
    pass

recursion_vs_iteration = ""   # TODO

print(recursive_sum([1, 2, 3, 4]), power(2, 5))''',
        '''def recursive_sum(values):
    if len(values) == 0:                         # base case: nothing to add
        return 0
    return values[0] + recursive_sum(values[1:])  # first item + sum of the REST (a smaller list)

def power(base, exp):
    if exp == 0:                                  # base case: anything to the power 0 is 1
        return 1
    return base * power(base, exp - 1)            # base times a smaller power

recursion_vs_iteration = ("Recursion solves a problem by calling itself on a smaller version, which can be "
                          "elegant for naturally nested problems but uses extra memory for each call. "
                          "Iteration uses loops, is usually faster and uses constant memory, "
                          "so it is often preferred when both are easy to write.")

print(recursive_sum([1, 2, 3, 4]), power(2, 5))   # 10 32''',
        '''check(recursive_sum([1, 2, 3, 4]) == 10 and recursive_sum([]) == 0, "recursive_sum", "first item + recursive_sum(rest)")
check(power(2, 5) == 32 and power(5, 0) == 1 and power(3, 1) == 3, "power", "base * power(base, exp - 1)")
check(len(recursion_vs_iteration.split()) >= 20, "comparison written", "write 2 to 3 sentences")'''),
]


def build():
    return build_week(6, "functions_modules_recursion", "Functions, Modules and Recursion",
                      OUTCOMES, ITEMS)
