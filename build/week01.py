from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Explain the difference between a source file, the Python interpreter and program output.",
    "Write, run and modify short Python programs using comments, variables, `print()` and `input()`.",
    "Choose valid identifiers (variable names) and follow Python naming conventions.",
    "Describe a problem as **Input → Process → Output (IPO)** before coding it.",
    "Separate the *processing* of a program (a function) from its *input/output*.",
]

ITEMS = [
    md("""## 1. Big ideas: how Python runs your code

| Word | Meaning | Everyday analogy |
|---|---|---|
| **Source code / script** | The text file you write (`.py`) | A recipe on paper |
| **Interpreter** | The program that reads your code line by line and carries it out | The cook following the recipe |
| **Output** | What appears on screen after the code runs | The meal |
| **Editor / IDE** | A friendly place to write code (VS Code, Colab) | The kitchen |

### Interactive shell versus script
- **Interactive** (a Colab cell, or typing `python` in a terminal): you type one statement, Python answers immediately. Great for experiments.
- **Script** (a `.py` file): many statements saved together, run in one go. Needed for real programs.

### Four rules you must know now
1. **Statements run top to bottom**, one after another.
2. **Indentation matters.** Python uses leading spaces (4 per level) to show which lines belong together. Wrong spaces → `IndentationError`.
3. **Comments** start with `#` and are ignored by Python.
4. **Python is case-sensitive:** `Name`, `name` and `NAME` are three different variables.

### Variables: labelled boxes
A **variable** is a name that points to a value. `age = 20` means: *create the name `age` and let it point to the number 20.* The `=` sign is **assignment** (“store this”), *not* mathematical equality.
Python uses **dynamic typing**: you do not declare a type; the value decides its type.

### Naming rules (identifiers)
- Letters, digits and underscores only; **cannot start with a digit**.
- No spaces; cannot be a Python keyword (`if`, `for`, `class`, ...).
- Convention: `lowercase_with_underscores` (`total_score`, not `TotalScore`).
- Choose **meaningful** names: `average_mark` beats `x`.

### The IPO model
Before you code, answer three questions: **What goes IN? What PROCESSING happens? What comes OUT?**

| Problem | Input | Process | Output |
|---|---|---|---|
| Rectangle perimeter | length, width | 2 × (length + width) | the perimeter |
"""),
    demo('''# --- DEMO 1: variables and print() --------------------------------
student = "Tola"                      # create a variable called student; store the TEXT "Tola" in it
age = 20                              # create a variable called age; store the whole number 20
height = 1.68                         # create a variable called height; store a decimal number
print(student)                        # show the value stored in student: Tola
print(age, height)                    # print() can show several values separated by a space
print("Student:", student)            # mixing a label (text) and a variable
age = age + 1                         # read age (20), add 1, store the result (21) back in age
print("Next year", student, "will be", age)   # age now holds 21
print(type(student), type(age), type(height)) # type() reveals each value's type: str, int, float'''),
    demo('''# --- DEMO 2: input() ALWAYS returns text --------------------------
name = input("Enter your name: ")            # show the question, wait for the user, store their answer as TEXT
programme = input("Enter your programme: ")  # a second question; the answer is also stored as text
print(f"Welcome, {name}.")                   # f-string: the {name} part is replaced by the variable's value
print(f"Programme: {programme}")             # same idea for programme
print(type(name))                            # confirm that input() gave us a str (text)'''),
    demo('''# --- DEMO 3: a complete IPO program (rectangle perimeter) ----------
length = float(input("Length: "))            # INPUT: read text, convert to a decimal number with float()
width = float(input("Width: "))              # INPUT: same for the width
perimeter = 2 * (length + width)             # PROCESS: the formula; * means multiply, brackets act first
print(f"Perimeter = {perimeter:.2f}")        # OUTPUT: {perimeter:.2f} shows exactly 2 decimal places'''),
    md("""### Why `float(input(...))`?
`input()` gives **text**. You cannot multiply text by 2 and get arithmetic: `"5" * 2` is `"55"`! So we **convert** with `float()` (decimal) or `int()` (whole number). You will practise conversion thoroughly in Week 2.

### Running a *script file* from Colab
Colab lets you write a `.py` file and run it, which mimics what you do in VS Code. The `%%writefile` line saves the cell as a file; `!python` runs it.
"""),
    demo('''%%writefile hello_script.py
# the line above is a Colab "magic": it saves THIS cell as a file named hello_script.py
print("This line came from a saved .py script")      # a normal Python statement inside the file
total = 3 + 4                                         # simple arithmetic
print("3 + 4 =", total)                              # show the result'''),
    demo('''!python hello_script.py'''),
    md("""### Error gallery (read, do not fear)
Errors are **messages from Python telling you what to fix**. Learn to read them from the *bottom line up*.

| You wrote | Python says | Meaning |
|---|---|---|
| `print("Hi)` | `SyntaxError: unterminated string literal` | A quote is not closed |
| `prnt("Hi")` | `NameError: name 'prnt' is not defined` | Typing error in a name |
| `    print("x")` at line start | `IndentationError: unexpected indent` | Extra spaces at the start |
| `"5" + 2` | `TypeError: can only concatenate str (not "int") to str` | Mixed text and number |
| `int("abc")` | `ValueError: invalid literal for int()` | Text cannot become a number |
"""),
    activity(
        "Follow the variable",
        "Trace this program by hand. What are `a`, `b` and `c` at the end?",
        '''a = 5                    # a is 5
b = 8                     # b is 8
c = a + b                 # c is a + b
a = 10                    # a changes to 10; does c change?
b = a                     # b now points to the same value as a
print(a, b, c)            # what is printed?''',
        "`10 10 13`. `c` was calculated *once* from the old `a` and `b` (5 + 8 = 13) and does **not** update when `a` changes. A variable stores a value, not a formula."),
    activity(
        "Text or number?",
        "Predict the output of each line. Pay attention to the quotes.",
        '''x = "7"                   # TEXT
y = 7                     # NUMBER
print(x + x)              # text + text
print(y + y)              # number + number
print(x * 3)              # text repeated 3 times
print(type(x) == type(y)) # are the two types the same?''',
        "`77`, `14`, `777`, `False`. Quotes create text, and operators behave differently on text and numbers."),
    md("""## 🛠️ Tasks
**Good habit:** put the *processing* inside a **function** (a reusable block you will study properly in Week 6). A function `def f(a, b): return ...` takes inputs and gives back a result. This also makes your code *testable*, which is why the ✅ checks can mark you automatically.
"""),
    task(1, "IPO tables",
         "Complete the IPO description of the **circle area** problem by filling the three strings. (Area of a circle is π × r².)",
         '''ipo_circle = {
    "input":   None,   # TODO: what does the user supply? (text)
    "process": None,   # TODO: the formula in words or symbols
    "output":  None,   # TODO: what is displayed?
}
print(ipo_circle)''',
         '''ipo_circle = {
    "input":   "radius r (a decimal number)",        # the only thing the user must provide
    "process": "area = pi * r * r (pi is about 3.14159)",   # multiply pi by r twice
    "output":  "the area, shown to 2 decimal places",       # what the program prints
}
print(ipo_circle)                                   # display the table''',
         '''check(all(isinstance(v, str) and len(v) > 3 for v in ipo_circle.values()), "all three IPO parts are written", "replace each None with a short description")
check("r" in ipo_circle["process"].lower() and ("pi" in ipo_circle["process"].lower() or "3.14" in ipo_circle["process"]), "process mentions pi and r", "the formula uses pi and r")'''),
    task(2, "Welcome message builder",
         "Write `welcome(name, matric, department, level)` that **returns** this exact text format:\n\n`Welcome, <name> (<matric>) of <department>, <level> Level.`\n\nUse fictional data. Then call it with your own details.",
         '''def welcome(name, matric, department, level):
    # TODO: return an f-string in the exact format shown above
    pass

print(welcome("Amina Bello", "OOU/2026/001", "Computer Science", 300))''',
         '''def welcome(name, matric, department, level):
    return f"Welcome, {name} ({matric}) of {department}, {level} Level."   # f-string fills each {} with the argument

print(welcome("Amina Bello", "OOU/2026/001", "Computer Science", 300))     # test with fictional data''',
         '''check(welcome("Amina Bello", "OOU/2026/001", "Computer Science", 300) == "Welcome, Amina Bello (OOU/2026/001) of Computer Science, 300 Level.", "exact format matches", "match the format exactly, including brackets, comma and full stop")'''),
    task(3, "Rectangle calculator",
         "Write `rectangle_area(length, width)` and `rectangle_perimeter(length, width)`. Each returns a number. Then run the interactive cell under it (it uses `input()`).",
         '''def rectangle_area(length, width):
    # TODO: return the area
    pass

def rectangle_perimeter(length, width):
    # TODO: return the perimeter
    pass

# Interactive part (works as soon as your functions are written)
l = float(input("Length: "))
w = float(input("Width: "))
print(f"Area = {rectangle_area(l, w)}, Perimeter = {rectangle_perimeter(l, w)}")   # TODO (bonus): format to 2 decimal places with :.2f''',
         '''def rectangle_area(length, width):
    return length * width                          # area = length times width

def rectangle_perimeter(length, width):
    return 2 * (length + width)                    # perimeter = twice the sum of two sides

# Interactive part
l = float(input("Length: "))                       # read the length as text and convert to float
w = float(input("Width: "))                        # read the width and convert
print(f"Area = {rectangle_area(l, w):.2f}, Perimeter = {rectangle_perimeter(l, w):.2f}")   # use the functions and format to 2 d.p.''',
         '''check(rectangle_area(4, 5) == 20, "area of 4 x 5 is 20", "area = length * width")
check(rectangle_perimeter(4, 5) == 18, "perimeter of 4 x 5 is 18", "perimeter = 2 * (length + width)")
check(abs(rectangle_area(2.5, 2) - 5.0) < 1e-9, "works with decimals", "do not convert to int")'''),
    task(4, "Circle area",
         "Write `circle_area(radius)`. State your approximation of π **as a named constant** `PI = 3.14159` at the top (naming constants in CAPITALS is a convention). Return the area.",
         '''PI = None   # TODO: the approximation of pi stated in the course notes

def circle_area(radius):
    # TODO: return PI * radius squared (radius * radius)
    pass

print(circle_area(2))      # TODO (bonus): round the result to 2 decimal places''',
         '''PI = 3.14159                          # a named constant: CAPITALS mean "do not change"

def circle_area(radius):
    return PI * radius * radius           # pi times r times r

print(round(circle_area(2), 2))           # expected 12.57''',
         '''check(PI == 3.14159, "PI constant is set", "set PI = 3.14159")
check(round(circle_area(2), 2) == 12.57, "area for radius 2 is 12.57", "area = PI * radius * radius")
check(circle_area(0) == 0, "radius 0 gives area 0", "multiplying by 0 should give 0")'''),
    task(5, "Extension: a three-option menu",
         "Write `menu_choice(number)` which returns `\"Computer Science\"` for 1, `\"Data Science\"` for 2, `\"Cyber Security\"` for 3 and `\"Invalid option\"` for anything else. *(Full input validation comes in Week 3; use `if / elif / else`.)*",
         '''def menu_choice(number):
    # TODO: use if / elif / else to return the right text
    pass

print(menu_choice(2))''',
         '''def menu_choice(number):
    if number == 1:                       # == asks "are these equal?" (a question), unlike = (store)
        return "Computer Science"
    elif number == 2:                     # elif = "else if": tried only when earlier tests failed
        return "Data Science"
    elif number == 3:
        return "Cyber Security"
    else:                                 # catches every other number
        return "Invalid option"

print(menu_choice(2))                     # Data Science''',
         '''check(menu_choice(1) == "Computer Science", "option 1", "return \\"Computer Science\\" for 1")
check(menu_choice(3) == "Cyber Security", "option 3", "return \\"Cyber Security\\" for 3")
check(menu_choice(9) == "Invalid option", "invalid option handled", "use else for everything else")'''),
    quiz([
        ("What type of value does `input()` return?", "Always `str` (text), even if the user types digits."),
        ("What is the role of indentation in Python?", "It shows which statements belong to the same block (e.g., the body of a function or `if`); wrong indentation is an error."),
        ("Differentiate assignment `=` from equality comparison `==`.", "`=` stores a value in a variable; `==` asks whether two values are equal and gives `True` or `False`."),
        ("Why is `2nd_score` not a valid variable name?", "Identifiers cannot start with a digit."),
    ]),
    assignment(
        "**A. IPO table.** For a *library book-loan fee calculator* (fee = days late × ₦50), complete the dictionary `ipo_library`.\n\n**B. Kilometres to miles.** Write `km_to_miles(km)` using `miles = km × 0.621371`.\n\n**C. Explain** in the string `explanation` the difference between a Python **source file**, the **interpreter** and the **output** (2 to 3 sentences, your own words).",
        '''ipo_library = {"input": None, "process": None, "output": None}   # TODO: fill each with text

def km_to_miles(km):
    # TODO: return km multiplied by 0.621371
    pass

explanation = ""   # TODO: your own words

print(ipo_library)
print(km_to_miles(10))
print(explanation)''',
        '''ipo_library = {
    "input": "number of days the book is late (a whole number)",   # what the librarian types
    "process": "fee = days_late * 50 naira",                        # the calculation
    "output": "the fee in naira",                                   # what is shown
}

def km_to_miles(km):
    return km * 0.621371                      # conversion factor given in the question

explanation = ("A source file is the text of the program that a human writes. "
               "The interpreter is the program that reads that file and carries out its instructions line by line. "
               "The output is what appears on screen as a result of running the code.")   # one possible answer

print(ipo_library)                            # show the IPO table
print(km_to_miles(10))                        # 6.21371
print(explanation)                            # show the explanation''',
        '''check(all(isinstance(v, str) and len(v) > 3 for v in ipo_library.values()), "IPO table complete", "fill all three entries")
check(abs(km_to_miles(10) - 6.21371) < 1e-9, "10 km = 6.21371 miles", "multiply by 0.621371")
check(len(explanation.split()) >= 15, "explanation has enough words", "write 2 to 3 sentences")'''),
]


def build():
    return build_week(1, "python_environment_first_programs", "Python Environment, First Programs and the Input–Process–Output Model",
                      OUTCOMES, ITEMS)
