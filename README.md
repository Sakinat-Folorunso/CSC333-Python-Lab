# CSC 333 Computer Programming III (Laboratory): Python Lab Notebooks

**Instructor:** Dr Sakinat Folorunso, Associate Professor of AI Systems
**Department of Computer Science, Olabisi Onabanjo University, Ago-Iwoye, Nigeria**
sakinat.folorunso@oouagoiwoye.edu.ng

Thirteen weekly Google Colab lab sessions (Week 0 to Week 12) that take students from installing Python to a tested, documented mini-application. Each week has a **Starter** notebook (students work here) and a **Solution** notebook (released after the session).

## Weekly map (simple to hard)
| Week | Topic |
|---|---|
| 0 | Setup and installation: Colab, Python, VS Code, Git/GitHub, virtual environments, troubleshooting |
| 1 | Python environment, first programs, input-process-output |
| 2 | Data types and operators |
| 3 | Selection and iteration |
| 4 | Strings, lists, tuples |
| 5 | Dictionaries, sets, stacks, queues |
| 6 | Functions, modules, recursion |
| 7 | Object-oriented programming |
| 8 | Data structures and algorithms (searching, sorting, linked list, Big-O, timing) |
| 9 | NumPy |
| 10 | Pandas |
| 11 | Data cleaning, Matplotlib, files (CSV/JSON), SQLite, pytest |
| 12 | Integrated project, testing, documentation, review |

Every notebook contains: learning outcomes, concept explanations in Markdown, worked demos with **every line of code commented**, Predict-Run-Explain class activities, graded tasks with automatic self-checks, a quiz, an assignment and a reflection/submission checklist. All datasets are synthetic and generated in-notebook with `seed=42`; no downloads are needed.

## Publishing on GitHub (5 minutes)
1. Create a **public** repository named `CSC333-Python-Lab` on GitHub and upload this folder (or `git init`, `git add .`, `git commit`, `git push`).
2. Rebuild the notebooks so the "Open in Colab" badges point to your account (only needed once):
   ```bash
   pip install -r requirements.txt
   GITHUB_USER=your-github-username python build/build_all.py
   ```
3. Commit and push. Students open a notebook on GitHub and click the **Open in Colab** badge, or use `https://colab.research.google.com/github/<user>/CSC333-Python-Lab/blob/main/notebooks/<week_folder>/<file>.ipynb`.
4. Tip: keep Solution notebooks in a separate private branch or release them after each session.

## Quality assurance
`python tools/validate_notebooks.py` executes every notebook headlessly. Solutions must pass every check; Starters must run without crashing before students edit them. Current status: **26/26 notebooks pass.**

## Repository layout
```
notebooks/weekNN_topic/CSC333_WeekNN_Starter.ipynb
notebooks/weekNN_topic/CSC333_WeekNN_Solution.ipynb
build/      generator (one file per week; edit content here, then rebuild)
tools/      validate_notebooks.py
data/       sample CSV files (student_scores.csv, messy_scores.csv)
```
