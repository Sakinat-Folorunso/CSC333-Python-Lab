from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Open, run, edit and save a Google Colab notebook and explain the difference between text cells and code cells.",
    "Install Python 3.11+, VS Code, Jupyter and Git on your own computer (Windows, macOS or Linux), or explain how to do so.",
    "Create a GitHub account and repository and save a Colab notebook to it.",
    "Verify your Python version and the libraries NumPy, Pandas and Matplotlib using code.",
    "Use a virtual environment and `pip` and describe why they matter.",
]

ITEMS = [
    md("""# 👋 Welcome to CSC 333

This course is a **hands-on laboratory**. You learn Python by *writing* Python. Every week you will get **two notebooks**:

| Notebook | What it is |
|---|---|
| **Starter** | Explanations, worked examples with every line commented, class activities, tasks with `TODO`s, and an assignment. **This is the one you work in.** |
| **Solution** | The same notebook with all tasks and the assignment solved. Use it *after* you have tried, to compare your thinking. |

> **Golden rule:** a solution you copied teaches you nothing. A solution you struggled with, even if wrong, teaches you a lot.

### The course road-map (simple → advanced)
| Weeks | Theme |
|---|---|
| 0 | Set-up, installation and downloads (today) |
| 1–2 | First programs, data types, operators |
| 3 | Control structures: decisions and loops |
| 4–5 | Strings and data structures: lists, tuples, dictionaries, sets, stacks, queues |
| 6 | Functions, modules, recursion |
| 7 | Object-oriented programming |
| 8 | Algorithms: searching, sorting, linked lists, complexity |
| 9 | Numerical computing with **NumPy** |
| 10 | Data manipulation with **Pandas** |
| 11 | Data cleaning, charts, files, SQLite, testing |
| 12 | Integrated individual project and practical demonstration |
"""),
    md("""## 1. Your main workspace: Google Colab (no installation needed)

**Google Colab** runs Python in your browser on Google's computers. You only need a Google account and internet access.

### 1.1 Open a notebook from GitHub
1. Go to the course GitHub repository (link given in class).
2. Click the week's folder, then the **Starter** notebook.
3. Click the **Open in Colab** badge at the top of the notebook, **or** go to [colab.research.google.com](https://colab.research.google.com) → **File → Open notebook → GitHub tab** and paste the repository address.

### 1.2 The two kinds of cell
| Cell type | Used for | How to run |
|---|---|---|
| **Text (Markdown) cell** | Explanations, notes, answers in words | Double-click to edit, `Shift + Enter` to display |
| **Code cell** | Python programs | Click the ▶ button or press `Shift + Enter` |

### 1.3 Things every Colab user must know
- **Run order matters.** Cells share memory. If you skip a cell that creates a variable, a later cell may fail. Fix: **Runtime → Restart session and run all**.
- **Colab forgets.** When the session ends, variables and uploaded files vanish. **Save your notebook** (below).
- **Saving to GitHub:** **File → Save a copy in GitHub**, choose your repository, and write a commit message such as `Week 00 done`.
- **Saving to Drive:** **File → Save a copy in Drive**.
- **Getting help:** put the cursor on a name and press `Shift + Tab`, or run `help(print)`.
"""),
    md("""## 2. Working on your own computer (recommended for Week 12 project)

Colab is perfect for lab work, but professionals also work locally. Install these **in this order**.

### 2.1 Download list
| # | Tool | What it is for | Where to download |
|---|---|---|---|
| 1 | **Python 3.11 or newer** | The language itself | [python.org/downloads](https://www.python.org/downloads/) |
| 2 | **Visual Studio Code (VS Code)** | A code editor | [code.visualstudio.com](https://code.visualstudio.com/) |
| 3 | **Git** | Tracks versions of your code | [git-scm.com/downloads](https://git-scm.com/downloads) |
| 4 | **GitHub account** | Stores your code online | [github.com](https://github.com/) (sign up, free) |
| 5 | **Jupyter** (installed with `pip`) | Notebooks on your own PC | see §2.4 |
| 6 | **NumPy, Pandas, Matplotlib** (installed with `pip`) | Data libraries used from Week 9 | see §2.5 |

### 2.2 Install Python
**Windows**
1. Download the installer from python.org.
2. **Tick “Add python.exe to PATH”** at the bottom of the first screen (the most common mistake is forgetting this).
3. Click **Install Now**.
4. Open **Command Prompt** and type `python --version`.

**macOS**
1. Download the macOS installer from python.org and run it.
2. Open **Terminal** and type `python3 --version`.

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

You should see something like `Python 3.12.x`. Any version **3.11 or higher** is fine.

### 2.3 Install VS Code and the Python extension
1. Install VS Code from the link above.
2. Open VS Code → click the **Extensions** icon (four squares) → search **Python** (by Microsoft) → **Install**.
3. Also install **Jupyter** (by Microsoft) in the same way.

### 2.4 Virtual environments and pip
A **virtual environment** is a private folder of Python packages for *one* project, so projects never clash.
```bash
# 1. make a project folder and go into it
mkdir CSC333
cd CSC333

# 2. create a virtual environment called .venv
python -m venv .venv            # on macOS/Linux use: python3 -m venv .venv

# 3. activate it
.venv\\Scripts\\activate          # Windows
source .venv/bin/activate        # macOS / Linux

# 4. install what we need (needed from Week 9; do it now if your internet is good)
pip install numpy pandas matplotlib jupyter pytest

# 5. launch notebooks on your PC
jupyter notebook
```
When the environment is active your prompt starts with `(.venv)`. To leave it, type `deactivate`.

### 2.5 Install Git and connect to GitHub
```bash
git --version                                   # confirm Git is installed
git config --global user.name  "Your Name"      # who you are
git config --global user.email "you@example.com"
git clone https://github.com/YOUR-USERNAME/CSC333-Python-Lab.git   # copy a repo to your PC
```
Your three most-used Git commands later: `git add .` (stage), `git commit -m "message"` (save a snapshot), `git push` (upload).
"""),
    md("""## 3. Low-bandwidth and offline strategy
Data is expensive and lab internet can be unreliable. Plan ahead:

- **Download once, use many times.** Download the Python installer and VS Code on a good connection and keep them on a flash drive.
- **Pre-download packages:** `pip download numpy pandas matplotlib -d wheels` saves installable files in a `wheels` folder. Later, on any computer: `pip install --no-index --find-links wheels numpy pandas matplotlib`.
- **Colab on mobile data:** a notebook uses little data (a few hundred KB). Avoid streaming video while it runs.
- **Ask your lecturer** for the offline package folder for the laboratory machines.

## 4. Troubleshooting table
| Symptom | Likely cause | Fix |
|---|---|---|
| `'python' is not recognized` | Python not on PATH (Windows) | Re-run installer, tick *Add to PATH*; or try `py --version` |
| `pip: command not found` | pip missing / wrong command | Use `python -m pip install ...` |
| `ModuleNotFoundError: No module named 'pandas'` | Library not installed in *this* environment | Activate `.venv`, then `pip install pandas` |
| Colab cell stuck on `[*]` | Previous cell still running / session dropped | **Runtime → Restart session** |
| `NameError: name 'x' is not defined` | Cell that defines `x` was not run | Run cells in order; **Run all** |
| `IndentationError` | Spaces/tabs mixed up | Use 4 spaces per level; never mix tabs |
| Notebook lost after closing Colab | Not saved | **File → Save a copy in GitHub/Drive** |
"""),
    md("""## 5. Your first lines of Python
Python reads a program **one line at a time, top to bottom**. A line starting with `#` is a **comment**: Python ignores it; it is a note for humans. In this course *every line of code is explained by a comment* so you can read like a detective.
"""),
    demo('''# --- DEMO 1: the classic first program -----------------------------
print("Hello, OOU!")                 # print() shows text on the screen; the text sits inside quotes
print("I am learning Python.")       # each print() starts a new line of output
print(2 + 3)                         # Python can also do arithmetic; numbers need no quotes
print("2" + "3")                     # in quotes, 2 and 3 are TEXT, so + joins them together'''),
    md("""### Environment check: is my Python ready?
The next cell is a tiny program that **inspects your environment** and prints a report. You will use it to prove your set-up works.
"""),
    demo('''# --- DEMO 2: environment check ---------------------------------------
import sys                                          # sys: information about the running Python
import platform                                     # platform: information about the computer
from importlib import metadata                      # metadata: lets us ask "which version of a library is installed?"

print("Python version :", sys.version.split()[0])   # sys.version is a long text; split()[0] keeps just e.g. "3.12.4"
print("Operating sys  :", platform.system())        # Windows, Linux (Colab runs Linux) or Darwin (macOS)

in_colab = "google.colab" in sys.modules            # True only inside Google Colab (the name appears in sys.modules)
print("Running in Colab:", in_colab)                # show the True/False answer

for library in ["numpy", "pandas", "matplotlib"]:   # loop over three library names, one at a time
    try:                                            # try the next line; if it fails, jump to "except"
        version = metadata.version(library)         # ask Python for the installed version of this library
        print(f"{library:<11} installed, version {version}")   # f-string: {library:<11} left-aligns the name in 11 spaces
    except metadata.PackageNotFoundError:           # this error means the library is NOT installed
        print(f"{library:<11} NOT installed (pip install {library})")  # tell the student how to fix it'''),
    activity(
        "Text versus numbers",
        "Look at the code below. **Before you run it**, write down exactly what you think will be printed on each of the three lines.",
        '''print(10 + 5)          # numbers: addition
print("10" + "5")      # text: joining (concatenation)
print("10" * 3)        # text times a number: repeat the text three times''',
        "Line 1 prints `15` (arithmetic). Line 2 prints `105` because quotes make `\"10\"` and `\"5\"` text, so `+` glues them. Line 3 prints `101010` because `*` repeats text. **Lesson:** the *type* of a value (number or text) decides what an operator does. Week 2 explores this properly."),
    md("""## 🛠️ Tasks
Complete the tasks below. Replace each `TODO`, run the cell, then run the ✅ check cell underneath.
"""),
    task(1, "Environment evidence",
         "Store your Python version and your operating system name in the two variables below. Use `sys.version.split()[0]` and `platform.system()` exactly as in Demo 2.",
         '''import sys                                  # import the sys module
import platform                              # import the platform module

python_version = None    # TODO: put the Python version text here
os_name = None           # TODO: put the operating system name here

print("Python:", python_version)             # show what you stored
print("OS:", os_name)                        # show what you stored''',
         '''import sys                                  # import the sys module
import platform                              # import the platform module

python_version = sys.version.split()[0]      # first word of the long version text, e.g. "3.12.4"
os_name = platform.system()                  # "Linux", "Windows" or "Darwin"

print("Python:", python_version)             # show what we stored
print("OS:", os_name)                        # show what we stored''',
         '''check(isinstance(python_version, str) and python_version.count(".") >= 1,
      "python_version looks like a version number", "use sys.version.split()[0]")
major, minor = (int(x) for x in python_version.split(".")[:2]) if isinstance(python_version, str) else (0, 0)
check((major, minor) >= (3, 11), "you have Python 3.11 or newer", "install Python 3.11+ (see Section 2.2)")
check(os_name in ("Windows", "Linux", "Darwin"), "os_name is valid", "use platform.system()")'''),
    task(2, "Introduce yourself",
         "Create the variables `full_name`, `programme` (e.g. `\"Data Science\"`), and `level` (use the number `300`). Then print one sentence: `Hello, my name is <name>, a <level> level <programme> student at OOU.` using an **f-string**. Use your own details.",
         '''full_name = None       # TODO: your name in quotes
programme = None       # TODO: your programme in quotes
level = None           # TODO: a whole number, no quotes

# TODO: print the sentence using an f-string, e.g. print(f"Hello, {...}")''',
         '''full_name = "Amina Bello"                     # text, so it goes in quotes
programme = "Data Science"                    # text again
level = 300                                   # a whole number: no quotes

print(f"Hello, my name is {full_name}, a {level} level {programme} student at OOU.")  # {} inserts each variable's value''',
         '''check(isinstance(full_name, str) and len(full_name) > 2, "full_name is set", "give full_name a text value")
check(isinstance(programme, str) and len(programme) > 1, "programme is set", "give programme a text value")
check(level == 300, "level is 300", "set level = 300 (a number, no quotes)")'''),
    task(3, "Library check function",
         "Write a function `is_installed(name)` that returns `True` if the library called `name` is installed and `False` otherwise. Use `importlib.metadata.version(name)` inside `try/except` as in Demo 2. Then test it.",
         '''from importlib import metadata

def is_installed(name):
    # TODO: try to read metadata.version(name); return True if it works
    # TODO: if metadata.PackageNotFoundError happens, return False
    pass

print(is_installed("numpy"))                  # may be True or False
print(is_installed("surely_not_a_real_lib"))  # must be False''',
         '''from importlib import metadata                   # lets us ask for installed library versions

def is_installed(name):
    try:                                          # try to find the library's version
        metadata.version(name)                    # raises an error if the library is missing
        return True                               # no error means it IS installed
    except metadata.PackageNotFoundError:         # error means NOT installed
        return False                              # report that

print(is_installed("numpy"))                      # True in Colab
print(is_installed("surely_not_a_real_lib"))      # False for a made-up name''',
         '''check(is_installed("surely_not_a_real_lib") is False, "missing library returns False", "return False in the except branch")
check(is_installed("pip") is True, "installed library returns True", "return True after metadata.version() works")'''),
    task(4, "GitHub readiness (no code: tick and tell)",
         "Work through this list in class. Then fill in the dictionary with `True`/`False` for what you have **actually completed**.\n\n- Created a Google account used for Colab\n- Created a GitHub account\n- Created a repository named `CSC333-Python-Lab` (public or private)\n- Saved this notebook into it with *File → Save a copy in GitHub*",
         '''ready = {
    "google_account": None,      # TODO: True or False
    "github_account": None,      # TODO: True or False
    "repository_created": None,  # TODO: True or False
    "notebook_saved_to_github": None,  # TODO: True or False
}
print(ready)''',
         '''ready = {
    "google_account": True,               # needed to open Colab
    "github_account": True,               # needed to store the work
    "repository_created": True,           # the CSC333-Python-Lab repository
    "notebook_saved_to_github": True,     # File -> Save a copy in GitHub
}
print(ready)                              # show the dictionary''',
         '''check(all(isinstance(v, bool) for v in ready.values()), "every entry is True or False", "replace each None with True or False")'''),
    quiz([
        ("What is the difference between a text cell and a code cell in Colab?",
         "A text (Markdown) cell holds explanations and notes and is *displayed*; a code cell holds Python and is *run*."),
        ("Why do we use a virtual environment?",
         "It gives each project its own private set of packages and versions so projects never conflict."),
        ("What does `#` do at the start of a line in Python?",
         "It starts a comment: Python ignores the line; it is a note for humans."),
        ("A student gets `ModuleNotFoundError: No module named 'pandas'`. Give two likely fixes.",
         "Install it with `pip install pandas` in the *active* environment; or activate the correct virtual environment first."),
    ]),
    assignment(
        "**A. Install locally (do this at home or in the lab).** Install Python 3.11+, VS Code and Git. Create the folder `CSC333/Week00`, a file `hello.py` containing `print(\"Hello from my own computer\")`, and run it in the terminal with `python hello.py`. Keep a **screenshot** of the terminal showing the output (you will upload it with this notebook).\n\n**B. In the cell below** complete the function `setup_report()` that returns a dictionary with the keys `python`, `os`, `numpy`, `pandas`, `matplotlib` (versions as text, or `\"missing\"`).\n\n**C. In a text cell**, explain in 3 sentences why Colab notebooks should be saved to GitHub.",
        '''from importlib import metadata
import platform
import sys

def setup_report():
    report = {}
    # TODO: report["python"] = ...            (version text)
    # TODO: report["os"] = ...                (operating system)
    # TODO: for each library in numpy, pandas, matplotlib store its version or "missing"
    return report

print(setup_report())''',
        '''from importlib import metadata                     # to read installed versions
import platform                                    # to read the operating system
import sys                                         # to read the Python version

def setup_report():
    report = {}                                    # start with an empty dictionary
    report["python"] = sys.version.split()[0]      # e.g. "3.12.4"
    report["os"] = platform.system()               # e.g. "Linux"
    for lib in ["numpy", "pandas", "matplotlib"]:  # go through each library name
        try:
            report[lib] = metadata.version(lib)    # store the version text
        except metadata.PackageNotFoundError:      # library not installed
            report[lib] = "missing"                # store the word "missing"
    return report                                  # give the finished dictionary back

print(setup_report())                              # display the report''',
        '''r = setup_report()
check(set(r) == {"python", "os", "numpy", "pandas", "matplotlib"}, "all five keys present", "the dictionary needs exactly: python, os, numpy, pandas, matplotlib")
check(all(isinstance(v, str) for v in r.values()), "all values are text", "store versions as text")'''),
]


def build():
    return build_week(0, "setup_and_installation", "Set-up, Installation and Downloads",
                      OUTCOMES, ITEMS, duration="3 hours (orientation + set-up clinic)")
