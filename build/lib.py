"""Notebook generator for OOU-CSC 333 (Computer Programming III, Laboratory).

One week-spec produces TWO notebooks:
  * Starter  : explained demos + activities + tasks with TODO skeletons
  * Solution : the same notebook with every task and assignment solved

Item constructors (used by week files):
  md(text)                       markdown shown in both notebooks
  demo(code)                     fully commented code shown in both notebooks
  activity(title, ask, code, explain)   Predict-Run-Explain class activity
  task(num, title, prompt, starter, solution, tests="")   graded practical task
  quiz([(question, answer), ...])       quick formative check
  assignment(prompt, starter, solution, tests="")         take-home assignment
"""
import os
import nbformat as nbf

# ---------------------------------------------------------------- config
COURSE = "OOU-CSC 333 · Computer Programming III (Laboratory)"
INSTRUCTOR = "Dr Sakinat Folorunso"
RANK = "Associate Professor of AI Systems"
DEPT = "Department of Computer Science"
UNIVERSITY = "Olabisi Onabanjo University, Ago-Iwoye, Nigeria"
EMAIL = "sakinat.folorunso@oouagoiwoye.edu.ng"
import os
GITHUB_USER = os.environ.get("GITHUB_USER", "YOUR-GITHUB-USERNAME")      # set with: GITHUB_USER=yourname python build/build_all.py
REPO = "CSC333-Python-Lab"                # <- replace if you rename the repo

SETUP_CODE = '''# ===== SETUP CELL: run this first in every notebook =====
# check() is a small helper that tells you whether your answer is right.
# It never crashes your notebook: it only prints a friendly message.
def check(condition, success, hint):
    # condition : True or False, the result of a test you pass in
    # success   : message printed when the test passes
    # hint      : message printed when the test fails
    if condition:                       # if the test passed ...
        print("✅ Correct:", success)     # ... celebrate
    else:                               # otherwise ...
        print("❌ Not yet:", hint)        # ... show a hint and try again

print("Setup complete. Helper check() is ready.")  # confirm the cell ran'''


# ---------------------------------------------------------------- item constructors
def md(text):
    return ("md", text)


def demo(code):
    return ("demo", code)


def activity(title, ask, code, explain):
    return ("activity", title, ask, code, explain)


def task(num, title, prompt, starter, solution, tests=""):
    return ("task", num, title, prompt, starter, solution, tests)


def quiz(qa):
    return ("quiz", qa)


def assignment(prompt, starter, solution, tests=""):
    return ("assignment", prompt, starter, solution, tests)


# ---------------------------------------------------------------- builders
def _badge(folder, fname):
    url = (f"https://colab.research.google.com/github/{GITHUB_USER}/{REPO}"
           f"/blob/main/notebooks/{folder}/{fname}")
    return ("[![Open In Colab](https://colab.research.google.com/assets/"
            f"colab-badge.svg)]({url})")


def _header(week, title, mode, outcomes, folder, fname, duration):
    wk = f"Week {week}" if week > 0 else "Week 0"
    role = ("🟦 **STARTER notebook**: you will complete the activities, tasks and "
            "assignment yourself." if mode == "Starter" else
            "🟩 **SOLUTION notebook**: reference answers. Attempt the Starter first; "
            "then compare.")
    outs = "\n".join(f"- {o}" for o in outcomes)
    return f"""# {COURSE}
## {wk}: {title}  ·  {mode}

{_badge(folder, fname)}

| | |
|---|---|
| **Instructor** | {INSTRUCTOR}, {RANK} |
| **Department** | {DEPT} |
| **University** | {UNIVERSITY} |
| **Contact** | {EMAIL} |
| **Session length** | {duration} |

{role}

### 🎯 Learning outcomes
By the end of this lab you will be able to:

{outs}

### 🧭 How to work through this notebook
1. Run the **Setup cell** first (Runtime → Run all is fine, or press `Shift + Enter` on each cell).
2. Read each markdown explanation, then read the **comment on every line** of the code.
3. Do the **🧠 Predict–Run–Explain** activities *before* you run the code: write your guess first.
4. Complete the **🛠️ Tasks**. Replace every `TODO`. Run the ✅ check cell under each task.
5. Finish the **📝 Assignment**, answer the **Quick check**, then complete the reflection and declaration at the end.
"""


def _footer(week):
    return f"""---
## 🪞 Reflection (write 3 to 5 sentences)
1. What is the single most important idea you learned this week?
2. Which task was hardest, and how did you get unstuck?
3. What will you do differently in Week {week + 1 if week < 12 else 12}?

*(Double-click this cell and type your answers below.)*

**My reflection:** _write here_

---
## ✔️ Submission checklist
- [ ] Every `TODO` replaced and every ✅ check passes
- [ ] Notebook runs from top to bottom with **Runtime → Restart and run all** and no errors
- [ ] Each task has a short comment explaining *why* your solution works
- [ ] Reflection written
- [ ] Declaration below completed
- [ ] Saved to GitHub: **File → Save a copy in GitHub** (or downloaded as `.ipynb` and uploaded)

## 📜 Declaration of sources and AI assistance
I declare that this work is my own, except for the following:

- **Collaboration (names):** _none / write here_
- **External code or websites used:** _none / write here_
- **AI assistance used (tool, prompt, which part):** _none / write here_
- **I can explain every line I submitted:** _yes / no_

**Student name:** _________  **Matric no.:** _________  **Date:** _________

---
*{COURSE} · {INSTRUCTOR}, {RANK}, {DEPT}, {UNIVERSITY}*
"""


def _wrap_tests(tests, header):
    """Wrap check code in try/except so an unfinished TODO never crashes 'Run all'."""
    import textwrap
    body = textwrap.indent(tests.strip("\n"), "    ")
    return (f"{header}\n"
            "try:                                   # run the checks safely\n"
            f"{body}\n"
            "except Exception as err:               # an unfinished TODO can cause an error: that is normal\n"
            "    print('❌ Not yet: your code raised', type(err).__name__, '-', err, '(finish the TODO above first)')")


def _notebook(week, title, items, mode, outcomes, folder, fname, duration):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"provenance": [], "name": fname},
    }
    cells = [nbf.v4.new_markdown_cell(_header(week, title, mode, outcomes, folder, fname, duration)),
             nbf.v4.new_code_cell(SETUP_CODE)]
    solution = mode == "Solution"
    for it in items:
        kind = it[0]
        if kind == "md":
            cells.append(nbf.v4.new_markdown_cell(it[1]))
        elif kind == "demo":
            cells.append(nbf.v4.new_code_cell(it[1]))
        elif kind == "activity":
            _, atitle, ask, code, explain = it
            cells.append(nbf.v4.new_markdown_cell(
                f"### 🧠 Class activity: {atitle}\n**Predict → Run → Explain**\n\n{ask}\n\n"
                "**✍️ My prediction (write before running):** _write here_"))
            cells.append(nbf.v4.new_code_cell(code))
            cells.append(nbf.v4.new_markdown_cell(
                "**🔍 Explanation**\n\n" + (explain if solution else
                "_Compare the output with your prediction. In your own words, explain any "
                "difference. Write your explanation here._")))
        elif kind == "task":
            _, num, ttitle, prompt, starter, sol, tests = it
            cells.append(nbf.v4.new_markdown_cell(f"### 🛠️ Task {num}: {ttitle}\n\n{prompt}"))
            cells.append(nbf.v4.new_code_cell(sol if solution else starter))
            if tests:
                cells.append(nbf.v4.new_code_cell(_wrap_tests(tests, "# ✅ CHECK YOUR WORK: run this cell after you finish the task")))
        elif kind == "quiz":
            lines = ["### ❓ Quick check: answer in your own words first"]
            for i, (q, a) in enumerate(it[1], 1):
                lines.append(f"\n**Q{i}. {q}**\n")
                lines.append(f"> **Answer:** {a}" if solution else "> _Your answer:_ ")
            cells.append(nbf.v4.new_markdown_cell("\n".join(lines)))
        elif kind == "assignment":
            _, prompt, starter, sol, tests = it
            cells.append(nbf.v4.new_markdown_cell(f"## 📝 Take-home assignment\n\n{prompt}"))
            cells.append(nbf.v4.new_code_cell(sol if solution else starter))
            if tests:
                cells.append(nbf.v4.new_code_cell(_wrap_tests(tests, "# ✅ CHECK YOUR WORK")))
    cells.append(nbf.v4.new_markdown_cell(_footer(week)))
    nb.cells = cells
    nbf.validate(nb)
    return nb


def build_week(week, slug, title, outcomes, items, duration="3 hours", root=None):
    """Write Starter and Solution notebooks for one week; return their paths."""
    root = root or os.path.join(os.path.dirname(os.path.dirname(__file__)), "notebooks")
    folder = f"week{week:02d}_{slug}"
    os.makedirs(os.path.join(root, folder), exist_ok=True)
    paths = []
    for mode in ("Starter", "Solution"):
        fname = f"CSC333_Week{week:02d}_{mode}.ipynb"
        nb = _notebook(week, title, items, mode, outcomes, folder, fname, duration)
        path = os.path.join(root, folder, fname)
        nbf.write(nb, path)
        paths.append(path)
    return paths
