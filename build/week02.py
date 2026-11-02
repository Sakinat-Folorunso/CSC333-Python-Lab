from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Identify `int`, `float`, `str` and `bool` values and check them with `type()`.",
    "Convert between types using `int()`, `float()` and `str()`.",
    "Use arithmetic (`+ - * / // % **`), comparison and logical operators correctly.",
    "Apply operator precedence and use parentheses to control it.",
    "Format numeric output (decimal places, thousands separators) with f-strings.",
]

ITEMS = [
    md("""## 1. Data types: what kind of thing is this value?
Every value in Python has a **type**. The type decides *what you can do* with the value.

| Type | Name | Example | Use |
|---|---|---|---|
| `int` | integer | `42`, `-7` | counting, indexes |
| `float` | decimal number | `3.14`, `-0.5` | measurements, money calculations |
| `str` | string (text) | `"OOU"`, `'hello'` | names, messages |
| `bool` | Boolean | `True`, `False` | answers to yes/no questions |

### Operators
| Group | Operators | Notes |
|---|---|---|
| Arithmetic | `+  -  *  /  //  %  **` | `/` true division, `//` floor division, `%` remainder, `**` power |
| Comparison | `==  !=  <  <=  >  >=` | always give `True` or `False` |
| Logical | `and  or  not` | combine `bool` values |
| Membership | `in  not in` | “is this inside that?” |

### Precedence (order of work), highest first
1. `()` brackets
2. `**` powers
3. `* / // %`
4. `+ -`
5. comparisons, then `not`, `and`, `or`

When in doubt, **use brackets**. They cost nothing and make your intention obvious.

### Floating-point warning
Computers store decimals in binary, so `0.1 + 0.2` is **not exactly** `0.3`. Never compare floats with `==`; round or use a tolerance.
"""),
    demo('''# --- DEMO 1: the four basic types -----------------------------------
count = 12                                  # int: a whole number
price = 49.99                               # float: has a decimal point
course = "CSC 333"                          # str: text inside quotes
passed = True                               # bool: only True or False (capital first letter!)
print(type(count))                          # <class 'int'>
print(type(price))                          # <class 'float'>
print(type(course))                         # <class 'str'>
print(type(passed))                         # <class 'bool'>
print(isinstance(count, int))               # isinstance asks: "is count an int?" -> True'''),
    demo('''# --- DEMO 2: arithmetic operators ------------------------------------
a = 17                                      # first number
b = 5                                       # second number
print(a + b)                                # addition: 22
print(a - b)                                # subtraction: 12
print(a * b)                                # multiplication: 85
print(a / b)                                # true division: 3.4 (always a float)
print(a // b)                               # floor division: 3 (how many whole 5s fit in 17)
print(a % b)                                # remainder (modulus): 2 (what is left over)
print(a ** 2)                               # power: 17 squared = 289
print(divmod(a, b))                         # divmod gives (quotient, remainder) together: (3, 2)'''),
    demo('''# --- DEMO 3: conversion (casting) -------------------------------------
text_five = "5"                             # looks like a number, but it is TEXT
text_four = "4"                             # also text
print(text_five + text_four)                # "54": text is joined, not added
print(int(text_five) + int(text_four))      # int() converts text to whole numbers first: 9
print(float("3.5") * 2)                     # float() converts text to a decimal: 7.0
print(str(2026) + " is the year")           # str() converts a number to text so it can be joined
print(int(7.9))                             # int() CUTS OFF the decimal part (no rounding): 7
print(round(7.9))                           # round() rounds to the nearest whole number: 8
print(bool(0), bool(5), bool(""), bool("hi"))  # 0 and "" are False; everything non-empty/non-zero is True'''),
    demo('''# --- DEMO 4: comparison and logical operators ---------------------------
score = 68                                  # a test score
print(score >= 50)                          # True: 68 is at least 50
print(score == 68)                          # True: == asks "equal?"
print(score != 100)                         # True: != asks "not equal?"
print(0 <= score <= 100)                    # True: Python allows chained comparison for a valid-range test
print(score >= 50 and score < 60)           # True only if BOTH are True (a "D" band, say)
print(score < 40 or score > 90)             # True if AT LEAST ONE is True: here False
print(not (score >= 50))                    # not flips True/False: False
print("OO" in "OOU")                        # membership: is "OO" inside "OOU"? True'''),
    demo('''# --- DEMO 5: formatting output with f-strings -----------------------------
total = 1234567.891                         # a large decimal number
print(f"{total}")                           # plain: 1234567.891
print(f"{total:.2f}")                       # .2f = fixed 2 decimal places: 1234567.89
print(f"{total:,.2f}")                      # , adds thousands separators: 1,234,567.89
print(f"{0.256:.1%}")                       # .1% shows a fraction as a percentage: 25.6%
print(f"{42:05d}")                          # 05d pads a whole number with zeros to 5 digits: 00042
print(f"{'left':<10}|{'right':>10}|")       # < left-aligns, > right-aligns inside a width of 10
print(f"₦{15000:,}")                        # money-style output: ₦15,000'''),
    demo('''# --- DEMO 6: a mini calculator (guarded division) ----------------------------
a = float(input("First number: "))          # read first number as text, convert to float
b = float(input("Second number: "))         # read second number the same way
print(f"Sum: {a + b:.2f}")                  # add and format
print(f"Difference: {a - b:.2f}")           # subtract and format
print(f"Product: {a * b:.2f}")              # multiply and format
if b != 0:                                  # only divide when the divisor is NOT zero
    print(f"Quotient: {a / b:.2f}")         # safe to divide
else:                                       # b IS zero
    print("Cannot divide by zero.")         # friendly message instead of a crash'''),
    activity(
        "Floating-point surprise",
        "What do you think each line prints? Is `0.1 + 0.2 == 0.3`? Then explain.",
        '''print(0.1 + 0.2)                            # decimals are stored in binary
print(0.1 + 0.2 == 0.3)                     # exact comparison of floats
print(round(0.1 + 0.2, 2) == 0.3)           # round first, then compare
print(abs((0.1 + 0.2) - 0.3) < 1e-9)        # or: is the difference tiny?''',
        "`0.30000000000000004`, `False`, `True`, `True`. Decimal fractions like 0.1 cannot be stored exactly in binary, so tiny errors appear. For comparisons, **round** or test that the **difference is very small**. For money in real systems, whole kobo/cents or the `decimal` module are used."),
    activity(
        "Operator precedence",
        "Evaluate by hand, **then** run. Which brackets change the answer?",
        '''print(4 + 3 * 2 ** 2)       # powers, then multiply, then add
print((4 + 3) * 2 ** 2)     # brackets first
print(((4 + 3) * 2) ** 2)   # brackets inside brackets
print(17 // 5 * 5 + 17 % 5) # is this 17 again?''',
        "`16`, `28`, `196`, `17`. First: 2**2=4, 3*4=12, 4+12=16. Second: (4+3)=7, 7*4=28. Third: (7*2)=14, 14**2=196. Last line shows the division identity `(a // b) * b + a % b == a`."),
    md("""## 🛠️ Tasks
Write the **processing** as functions so your results can be checked automatically.
"""),
    task(1, "Safe calculator",
         "Write `calculate(a, b, op)` where `op` is one of `\"+\"`, `\"-\"`, `\"*\"`, `\"/\"`. Return the result. For `\"/\"` with `b == 0` return the text `\"Cannot divide by zero\"`; for any other symbol return `\"Unknown operation\"`.",
         '''def calculate(a, b, op):
    # TODO: use if / elif / else to choose the operation
    pass

print(calculate(8, 2, "+"))
print(calculate(8, 0, "/"))''',
         '''def calculate(a, b, op):
    if op == "+":                              # addition requested
        return a + b
    elif op == "-":                            # subtraction requested
        return a - b
    elif op == "*":                            # multiplication requested
        return a * b
    elif op == "/":                            # division requested
        if b == 0:                             # guard against dividing by zero
            return "Cannot divide by zero"
        return a / b                           # safe division
    else:                                      # any other symbol
        return "Unknown operation"

print(calculate(8, 2, "+"))                    # 10
print(calculate(8, 0, "/"))                    # Cannot divide by zero''',
         '''check(calculate(8, 2, "+") == 10, "addition", "return a + b for +")
check(calculate(8, 2, "-") == 6, "subtraction", "return a - b for -")
check(calculate(8, 2, "*") == 16, "multiplication", "return a * b for *")
check(calculate(8, 2, "/") == 4, "division", "return a / b for /")
check(calculate(8, 0, "/") == "Cannot divide by zero", "division by zero guarded", "test b == 0 first")
check(calculate(8, 2, "^") == "Unknown operation", "unknown operator", "use else for other symbols")'''),
    task(2, "Minutes to hours and minutes",
         "Write `to_hours_minutes(total_minutes)` returning a **tuple** `(hours, minutes)`. Use `//` and `%`. Example: 135 → `(2, 15)`.",
         '''def to_hours_minutes(total_minutes):
    # TODO: hours = whole hours, minutes = what is left over
    pass

print(to_hours_minutes(135))''',
         '''def to_hours_minutes(total_minutes):
    hours = total_minutes // 60                # how many whole 60s fit in total_minutes
    minutes = total_minutes % 60               # remainder: minutes left over
    return hours, minutes                      # returning two values makes a tuple

print(to_hours_minutes(135))                   # (2, 15)''',
         '''check(to_hours_minutes(135) == (2, 15), "135 -> (2, 15)", "use // 60 and % 60")
check(to_hours_minutes(59) == (0, 59), "59 -> (0, 59)", "hours can be 0")
check(to_hours_minutes(120) == (2, 0), "120 -> (2, 0)", "minutes can be 0")'''),
    task(3, "Simple interest",
         "Write `simple_interest(principal, rate, time)` using **I = (P × R × T) / 100**. Return the interest. Then write `total_amount(principal, rate, time)` = principal + interest.",
         '''def simple_interest(principal, rate, time):
    # TODO
    pass

def total_amount(principal, rate, time):
    # TODO: use simple_interest() inside this function
    pass

print(simple_interest(10000, 5, 2))''',
         '''def simple_interest(principal, rate, time):
    return (principal * rate * time) / 100     # the textbook formula

def total_amount(principal, rate, time):
    return principal + simple_interest(principal, rate, time)   # reuse the first function

print(simple_interest(10000, 5, 2))            # 1000.0''',
         '''check(simple_interest(10000, 5, 2) == 1000, "interest is 1000", "(P * R * T) / 100")
check(total_amount(10000, 5, 2) == 11000, "total is 11000", "principal + interest")
check(simple_interest(0, 5, 2) == 0, "zero principal", "result should be 0")'''),
    task(4, "Divisible by 3 and 5",
         "Write `divisible_by_3_and_5(n)` returning `True` or `False` (a **bool**). Use `%` and `and`. Do **not** use `if`.",
         '''def divisible_by_3_and_5(n):
    # TODO: return a single Boolean expression
    pass

print(divisible_by_3_and_5(30), divisible_by_3_and_5(9))''',
         '''def divisible_by_3_and_5(n):
    return n % 3 == 0 and n % 5 == 0           # remainder 0 means "divides exactly"; and needs BOTH

print(divisible_by_3_and_5(30), divisible_by_3_and_5(9))   # True False''',
         '''check(divisible_by_3_and_5(30) is True, "30 -> True", "30 divides by 3 and by 5")
check(divisible_by_3_and_5(9) is False, "9 -> False", "9 is not divisible by 5")
check(divisible_by_3_and_5(15) is True, "15 -> True", "15 = 3 x 5")
check(divisible_by_3_and_5(0) is True, "0 -> True", "0 % 3 == 0 and 0 % 5 == 0")'''),
    task(5, "Extension: BMI (computation only)",
         "Write `bmi(weight_kg, height_m)` = weight / height². Return the value rounded to 1 decimal place. *This lab is about numerical computation, not medical interpretation.*",
         '''def bmi(weight_kg, height_m):
    # TODO: weight divided by height squared, rounded to 1 decimal place
    pass

print(bmi(70, 1.75))''',
         '''def bmi(weight_kg, height_m):
    value = weight_kg / (height_m ** 2)        # square the height FIRST (brackets!), then divide
    return round(value, 1)                     # round to 1 decimal place

print(bmi(70, 1.75))                           # 22.9''',
         '''check(bmi(70, 1.75) == 22.9, "70 kg, 1.75 m -> 22.9", "weight / height ** 2, then round(..., 1)")
check(bmi(50, 1.6) == 19.5, "50 kg, 1.6 m -> 19.5", "check your brackets")'''),
    quiz([
        ("Why does `input()` normally require conversion for arithmetic?", "`input()` returns text; `int()` or `float()` turn it into a number so arithmetic works."),
        ("What is the result of `17 // 5` and `17 % 5`?", "`3` and `2`."),
        ("What does a Boolean expression produce?", "One of the two values `True` or `False`."),
        ("Why is `0.1 + 0.2 == 0.3` risky?", "Floats are stored approximately in binary, so tiny errors occur; compare with rounding or a tolerance."),
    ]),
    assignment(
        "**A.** Write `average_of_four(a, b, c, d)` returning the average **rounded to 2 decimal places**.\n\n**B.** In the string `division_notes`, explain the difference between `/`, `//` and `%` with one example each.\n\n**C.** Evaluate `(4 + 3) × 2²` using Python in the variable `answer`, and in `why_brackets` explain why the brackets matter.",
        '''def average_of_four(a, b, c, d):
    # TODO
    pass

division_notes = ""    # TODO
answer = None          # TODO: write the Python expression for (4 + 3) x 2 squared
why_brackets = ""      # TODO

print(average_of_four(70, 65, 80, 75), answer)''',
        '''def average_of_four(a, b, c, d):
    return round((a + b + c + d) / 4, 2)      # add all four FIRST (brackets), then divide by 4

division_notes = ("/ is true division and always gives a float, e.g. 7 / 2 = 3.5. "
                  "// is floor division and gives the whole part, e.g. 7 // 2 = 3. "
                  "% gives the remainder, e.g. 7 % 2 = 1.")          # one possible answer

answer = (4 + 3) * 2 ** 2                     # 7 * 4 = 28
why_brackets = ("Without brackets, Python does 2 ** 2 first, then multiplies, then adds, "
                "so 4 + 3 * 2 ** 2 = 16. The brackets force 4 + 3 to be done first, giving 28.")

print(average_of_four(70, 65, 80, 75), answer)   # 72.5 28''',
        '''check(average_of_four(70, 65, 80, 75) == 72.5, "average is 72.5", "sum divided by 4")
check(average_of_four(1, 2, 2, 2) == 1.75, "rounding to 2 dp works", "use round(..., 2)")
check(answer == 28, "answer is 28", "write (4 + 3) * 2 ** 2")
check(len(division_notes.split()) >= 15 and len(why_brackets.split()) >= 10, "explanations written", "write full sentences")'''),
]


def build():
    return build_week(2, "data_types_and_operators", "Data Types, Operators, Expressions and Formatted Output",
                      OUTCOMES, ITEMS)
