from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Write decisions with `if`, `elif` and `else`, including compound conditions.",
    "Write repetition with `for` (with `range()`) and `while` loops.",
    "Use accumulators, counters, sentinels, `break` and `continue`.",
    "Use nested loops and trace a program by hand.",
    "Test boundary values and recognise infinite loops and off-by-one errors.",
]

ITEMS = [
    md("""## 1. The three building blocks of every program
Every algorithm, however large, is built from only **three control structures**:

| Structure | Question it answers | Python |
|---|---|---|
| **Sequence** | What happens one after another? | lines in order |
| **Selection** | Which path do I take? | `if / elif / else` |
| **Iteration** | What must be repeated? | `for`, `while` |

### Selection
```python
if condition_1:        # runs when condition_1 is True
    ...
elif condition_2:      # tried only if condition_1 was False
    ...
else:                  # runs when nothing above was True
    ...
```
- The colon `:` and the **indentation** are required.
- Python checks conditions **from top to bottom** and runs **only the first one that is True**.

### Iteration
| Loop | Use it when | Example |
|---|---|---|
| `for` | you know *how many times* or you are going *through a collection* | `for i in range(5)` |
| `while` | you repeat *until something changes* | `while password != "ok"` |

`range(stop)` → 0 … stop-1 · `range(start, stop)` · `range(start, stop, step)`. **The stop value is never included.**

### Loop tools
- **Accumulator:** a variable that builds up a result (`total = total + mark`, or `total += mark`).
- **Counter:** counts how many times something happens.
- **Sentinel:** a special input that means “stop” (e.g. `-1`).
- `break` leaves the loop immediately; `continue` skips to the next round.

### Two classic bugs
- **Off-by-one:** `range(5)` gives 0–4, not 1–5.
- **Infinite loop:** a `while` whose condition never becomes False. (In Colab press the ■ stop button.)
"""),
    demo('''# --- DEMO 1: if / elif / else (grading) ---------------------------------
score = 63                                     # the score to classify (change it and re-run!)
if not 0 <= score <= 100:                      # first, reject impossible scores
    print("Invalid score")                     # shown for e.g. -5 or 120
elif score >= 70:                              # 70 and above
    print("A")
elif score >= 60:                              # 60 to 69 (we only get here if score < 70)
    print("B")                                 # 63 lands here
elif score >= 50:                              # 50 to 59
    print("C")
elif score >= 45:                              # 45 to 49
    print("D")
else:                                          # anything below 45 that is still valid
    print("F")'''),
    demo('''# --- DEMO 2: for loop and range() ----------------------------------------
for i in range(5):                             # i takes the values 0, 1, 2, 3, 4
    print("round", i)                          # runs once per value of i
print(list(range(1, 6)))                       # list() lets us SEE the sequence 1..5 (6 is not included)
print(list(range(0, 10, 2)))                   # step of 2: 0, 2, 4, 6, 8
print(list(range(5, 0, -1)))                   # negative step counts down: 5, 4, 3, 2, 1'''),
    demo('''# --- DEMO 3: accumulator and counter ---------------------------------------
marks = [55, 72, 48, 90, 66]                   # a list of five marks (lists are explored fully in Week 4)
total = 0                                      # accumulator starts at zero
passed = 0                                     # counter starts at zero
for mark in marks:                             # take each mark in turn
    total += mark                              # total = total + mark: add this mark to the running total
    if mark >= 50:                             # is it a pass?
        passed += 1                            # yes: count it
print("Total:", total)                         # 331
print("Average:", total / len(marks))          # len() counts the items: 5
print("Passed:", passed)                       # 4'''),
    demo('''# --- DEMO 4: while loop with a sentinel ---------------------------------------
numbers = iter([4, 9, 2, -1, 7])               # iter simulates a user typing these values one by one
total = 0                                      # accumulator
value = next(numbers)                          # read the FIRST value before the loop
while value != -1:                             # -1 is the sentinel: keep going until we see it
    total += value                             # add the value
    value = next(numbers)                      # read the NEXT value (forgetting this = infinite loop!)
print("Sum before sentinel:", total)            # 15 (the 7 after -1 is never read)'''),
    demo('''# --- DEMO 5: break and continue -------------------------------------------------
for n in range(1, 11):                         # numbers 1 to 10
    if n % 2 == 0:                             # even number?
        continue                               # skip the rest of this round, go to the next n
    if n > 7:                                  # past 7?
        break                                  # leave the loop entirely
    print(n, end=" ")                          # print odd numbers 1 3 5 7 on one line (end=" " avoids a new line)
print()                                        # finish the line'''),
    demo('''# --- DEMO 6: nested loops (a number triangle) -------------------------------------
for row in range(1, 5):                        # outer loop: rows 1 to 4
    for col in range(1, row + 1):              # inner loop: runs completely for EACH row
        print(col, end=" ")                    # print 1..row on the same line
    print()                                    # new line after each row
# Output:
# 1
# 1 2
# 1 2 3
# 1 2 3 4'''),
    activity(
        "Trace the loop",
        "Complete the table by hand: what is `total` after each round? What is printed at the end?",
        '''total = 0                                   # start
for i in range(1, 5):                       # i = 1, 2, 3, 4
    total = total + i * i                   # add the square
    print(i, total)                         # show i and total
print("end", total)''',
        "Rounds: `1 1`, `2 5`, `3 14`, `4 30`, then `end 30`. This is the sum of squares 1² + 2² + 3² + 4². **Tip:** tracing with a table (round | i | total) is the fastest way to find logic errors."),
    activity(
        "Off-by-one",
        "How many times does each loop run? What is the last value printed?",
        '''for i in range(3):          # loop A
    print("A", i)
for i in range(1, 3):       # loop B
    print("B", i)
for i in range(3, 0, -1):   # loop C
    print("C", i)''',
        "A prints 0,1,2 (3 times); B prints 1,2 (2 times: stop 3 is excluded); C prints 3,2,1 (counting down, stop 0 excluded). **Rule:** `range(a, b)` runs `b - a` times."),
    md("""## 🛠️ Tasks
"""),
    task(1, "Grade calculator with validation",
         "Write `grade(score)` returning `\"A\"` (70+), `\"B\"` (60–69), `\"C\"` (50–59), `\"D\"` (45–49), `\"F\"` (below 45) and `\"Invalid\"` if the score is not between 0 and 100 inclusive. Test **boundaries**: 44, 45, 49, 50, 59, 60, 69, 70, 100, 101, -1.",
         '''def grade(score):
    # TODO: validate first, then use if / elif / else
    pass

for s in [44, 45, 70, 101]:
    print(s, grade(s))''',
         '''def grade(score):
    if score < 0 or score > 100:               # invalid FIRST, so bad scores never get a grade
        return "Invalid"
    elif score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    else:
        return "F"

for s in [44, 45, 70, 101]:                    # a few boundary tests
    print(s, grade(s))''',
         '''cases = {44: "F", 45: "D", 49: "D", 50: "C", 59: "C", 60: "B", 69: "B", 70: "A", 100: "A", 101: "Invalid", -1: "Invalid", 0: "F"}
wrong = {s: grade(s) for s, want in cases.items() if grade(s) != want}
check(not wrong, "all boundary cases correct", f"wrong results (score: yours): {wrong}")'''),
    task(2, "Score summary without Pandas",
         "Write `summary(scores)` that takes a list of numbers and returns a dictionary with `total`, `average`, `highest` and `lowest`. Use a **for loop** (do not use `sum`, `max`, `min`). If the list is empty return `None`.",
         '''def summary(scores):
    # TODO: loop through scores, track total, highest and lowest
    pass

print(summary([55, 72, 48, 90, 66]))''',
         '''def summary(scores):
    if len(scores) == 0:                       # nothing to summarise
        return None
    total = 0                                  # accumulator
    highest = scores[0]                        # start both extremes with the first score
    lowest = scores[0]
    for s in scores:                           # visit every score
        total += s                             # add to the total
        if s > highest:                        # new maximum found
            highest = s
        if s < lowest:                         # new minimum found
            lowest = s
    return {"total": total, "average": total / len(scores), "highest": highest, "lowest": lowest}

print(summary([55, 72, 48, 90, 66]))''',
         '''r = summary([55, 72, 48, 90, 66])
check(r == {"total": 331, "average": 66.2, "highest": 90, "lowest": 48}, "summary correct", "check total, average, highest, lowest")
check(summary([]) is None, "empty list returns None", "test len(scores) == 0 first")
check(summary([7])["lowest"] == 7, "single value works", "initialise highest/lowest with the first item")'''),
    task(3, "Multiplication table",
         "Write `times_table(n, up_to=12)` returning a **list of strings** such as `\"7 x 3 = 21\"` for 1 to `up_to`. Use a `for` loop and an f-string.",
         '''def times_table(n, up_to=12):
    lines = []
    # TODO: loop from 1 to up_to (inclusive!) and append each line
    return lines

for line in times_table(7, 3):
    print(line)''',
         '''def times_table(n, up_to=12):
    lines = []                                 # collect the lines here
    for i in range(1, up_to + 1):              # +1 because range excludes the stop value
        lines.append(f"{n} x {i} = {n * i}")   # build the text for this row
    return lines                               # give the list back

for line in times_table(7, 3):                 # print the three rows
    print(line)''',
         '''check(times_table(7, 3) == ["7 x 1 = 7", "7 x 2 = 14", "7 x 3 = 21"], "7 times table (3 rows)", "format must be '7 x 3 = 21'")
check(len(times_table(5)) == 12, "default is 12 rows", "up_to defaults to 12 and is inclusive")'''),
    task(4, "Count vowels",
         "Write `count_vowels(sentence)` returning how many vowels (a, e, i, o, u, either case) the sentence contains. Iterate over the characters.",
         '''def count_vowels(sentence):
    count = 0
    # TODO: loop over each character; count it if it is a vowel
    return count

print(count_vowels("Python is fun"))''',
         '''def count_vowels(sentence):
    count = 0                                  # counter
    for ch in sentence.lower():                # lower() so "A" and "a" are treated alike
        if ch in "aeiou":                      # membership test on a string of vowels
            count += 1                         # one more vowel
    return count

print(count_vowels("Python is fun"))           # 3''',
         '''check(count_vowels("Python is fun") == 3, "3 vowels", "count o, i, u")
check(count_vowels("RHYTHM") == 0, "no vowels", "y is not counted")
check(count_vowels("AEIOU aeiou") == 10, "upper and lower case", "use lower()")'''),
    task(5, "Number guessing game (fixed secret)",
         "Write `play(secret, guesses)` where `guesses` is a list of attempts. Loop through the guesses; return the **number of attempts** used to get the secret right, or `-1` if never guessed. Stop as soon as the secret is found (`break` or `return`).",
         '''def play(secret, guesses):
    # TODO: count attempts; stop when guess == secret
    pass

print(play(7, [3, 9, 7, 1]))''',
         '''def play(secret, guesses):
    attempts = 0                               # how many guesses used so far
    for guess in guesses:                      # try each guess in order
        attempts += 1                          # this guess counts as one attempt
        if guess == secret:                    # correct?
            return attempts                    # return stops the function (and the loop) at once
    return -1                                  # loop ended with no correct guess

print(play(7, [3, 9, 7, 1]))                   # 3''',
         '''check(play(7, [3, 9, 7, 1]) == 3, "found on attempt 3", "return the attempt count when guess == secret")
check(play(7, [1, 2]) == -1, "never guessed gives -1", "return -1 after the loop")
check(play(5, [5]) == 1, "found on attempt 1", "count the first guess too")'''),
    task(6, "Extension: right-angled pattern",
         "Write `triangle(n)` returning a list of `n` strings: `\"1\"`, `\"1 2\"`, `\"1 2 3\"` ... using **nested loops**. Explain in a comment how the outer and inner loop interact.",
         '''def triangle(n):
    rows = []
    # TODO: outer loop = rows; inner loop = numbers in a row
    return rows

for r in triangle(4):
    print(r)''',
         '''def triangle(n):
    rows = []                                  # will hold the finished rows
    for row in range(1, n + 1):                # OUTER loop: one pass per row
        numbers = []                           # numbers for THIS row
        for col in range(1, row + 1):          # INNER loop: runs fully for every outer pass, row times
            numbers.append(str(col))           # str() so we can join numbers as text
        rows.append(" ".join(numbers))         # join the pieces with spaces
    return rows

for r in triangle(4):                          # display
    print(r)''',
         '''check(triangle(3) == ["1", "1 2", "1 2 3"], "triangle(3)", "row k contains 1..k separated by spaces")
check(triangle(1) == ["1"], "triangle(1)", "one row only")
check(triangle(0) == [], "triangle(0) is empty", "range(1, 1) is empty")'''),
    quiz([
        ("What condition must eventually become false in a terminating `while` loop?", "The loop's own condition; something inside the loop must change the variables it tests."),
        ("What is an off-by-one error?", "Looping or indexing one time too many or too few, e.g. expecting `range(5)` to include 5."),
        ("What is the effect of `break`?", "It ends the loop immediately and continues after it."),
        ("When is a `for` loop better than a `while` loop?", "When the number of repetitions is known or you are going through every item of a collection."),
    ]),
    assignment(
        "**A.** Write `count_signs(values)` returning a tuple `(positives, negatives, zeros)`.\n\n**B.** Password attempts: write `login(correct, attempts)`. `attempts` is a list of tries. Return `\"Access granted\"` if one of the **first 3** matches, otherwise `\"Account locked\"`. Write your **pseudocode** first as comments.\n\n**C.** In the string `for_vs_while`, explain when a `for` loop is better than a `while` loop.",
        '''def count_signs(values):
    # TODO
    pass

def login(correct, attempts):
    # PSEUDOCODE (write your plan here as comments)
    # TODO
    pass

for_vs_while = ""   # TODO

print(count_signs([3, -1, 0, 8, -4]))
print(login("oou123", ["a", "oou123"]))''',
        '''def count_signs(values):
    positives = negatives = zeros = 0          # three counters, all start at zero
    for v in values:                           # inspect each value
        if v > 0:
            positives += 1
        elif v < 0:
            negatives += 1
        else:                                  # not > 0 and not < 0 means exactly 0
            zeros += 1
    return positives, negatives, zeros

def login(correct, attempts):
    # PSEUDOCODE:
    #   for each of the first 3 attempts
    #       if attempt equals the correct password: access granted
    #   if loop finishes with no match: account locked
    for attempt in attempts[:3]:               # [:3] keeps only the first three tries (slicing: Week 4)
        if attempt == correct:
            return "Access granted"
    return "Account locked"

for_vs_while = ("Use a for loop when you know how many times to repeat or you are visiting every item "
                "of a collection. Use a while loop when you repeat until a condition changes and "
                "you cannot know in advance how many rounds are needed.")

print(count_signs([3, -1, 0, 8, -4]))          # (2, 2, 1)
print(login("oou123", ["a", "oou123"]))        # Access granted''',
        '''check(count_signs([3, -1, 0, 8, -4]) == (2, 2, 1), "signs counted", "return (positives, negatives, zeros)")
check(login("pw", ["x", "y", "pw"]) == "Access granted", "third attempt allowed", "check the first 3 attempts")
check(login("pw", ["x", "y", "z", "pw"]) == "Account locked", "fourth attempt too late", "only the first 3 count")
check(len(for_vs_while.split()) >= 15, "explanation written", "write a full explanation")'''),
]


def build():
    return build_week(3, "selection_and_iteration", "Selection, Iteration and Practical Problem Solving",
                      OUTCOMES, ITEMS)
