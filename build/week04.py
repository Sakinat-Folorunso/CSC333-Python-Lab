from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Manipulate strings using indexing, slicing and common methods.",
    "Create, read, update and traverse **lists**, including nested lists.",
    "Explain **mutability** and the difference between aliasing and copying.",
    "Use **tuples** and tuple unpacking, and explain when a tuple is the right choice.",
    "Process small collections of records (scores, inventory, sentences) without Pandas.",
]

ITEMS = [
    md("""## 1. From single values to collections
So far each variable held **one** value. Real data comes in groups: all the scores in a class, all the items in a shop. A **sequence** stores many values in order and lets you reach each one by its **position (index)**.

| Type | Mutable? | Written | Typical use |
|---|---|---|---|
| `str` | ❌ no | `"hello"` | text |
| `list` | ✅ yes | `[1, 2, 3]` | a collection you will change |
| `tuple` | ❌ no | `(6.5, 3.2)` | a fixed record, e.g. a coordinate |

### Indexing and slicing
- Counting starts at **0**. `items[0]` is the first, `items[-1]` is the **last**.
- Slice `items[start:stop]` includes `start`, excludes `stop`. `items[:3]` first three; `items[2:]` from index 2; `items[::-1]` reversed.

```
 index:    0    1    2    3
 value:   "A"  "B"  "C"  "D"
 negative: -4   -3   -2   -1
```

### Mutable vs immutable
- **Mutable** = can be changed *in place* (lists).
- **Immutable** = cannot (strings, tuples). Operations return a **new** value.
- Danger: `b = a` for lists makes **both names point to the same list** (*aliasing*). Use `b = a.copy()` for an independent copy.

### Essential string methods
`strip()` `lower()` `upper()` `title()` `split()` `join()` `replace()` `find()` `startswith()` `count()`.

### Essential list methods
`append(x)` add at end · `extend(more)` add many · `insert(i, x)` · `remove(x)` · `pop()` / `pop(i)` · `sort()` · `reverse()` · plus functions `len`, `sum`, `min`, `max`, `sorted`.
"""),
    demo('''# --- DEMO 1: strings: indexing, slicing, methods ---------------------------
word = "Programming"                         # a string of 11 characters
print(word[0])                               # first character: P
print(word[-1])                              # last character: g
print(word[0:7])                             # characters 0..6: Program
print(word[3:])                              # from index 3 to the end: gramming
print(word[::-1])                            # reversed: gnimmargorP
print(len(word))                             # number of characters: 11
print(word.upper(), word.lower())            # all capitals / all small letters
print(word.count("m"))                       # how many times "m" appears: 2
print(word.replace("m", "M"))                # returns a NEW string: PrograMMing (original unchanged)
# word[0] = "p"                              # ERROR if uncommented: strings are immutable'''),
    demo('''# --- DEMO 2: cleaning and splitting text ------------------------------------
raw_name = "   ada LOVELACE   "              # messy text with extra spaces and odd capitals
clean_name = raw_name.strip().title()        # strip() removes edge spaces; title() capitalises each word
print(clean_name)                            # Ada Lovelace
csv_line = "Amina, 78 ,Data Science"         # one comma-separated record
parts = csv_line.split(",")                  # split() cuts the text at every comma and returns a LIST
print(parts)                                 # ['Amina', ' 78 ', 'Data Science']
parts = [p.strip() for p in parts]           # list comprehension: strip the spaces off each piece
print(parts)                                 # ['Amina', '78', 'Data Science']
print(" | ".join(parts))                     # join() glues the list back together with " | " between items'''),
    demo('''# --- DEMO 3: lists: create, read, change ----------------------------------------
scores = [68, 75, 82]                        # a list of three integers
scores.append(91)                            # add 91 at the END: [68, 75, 82, 91]
scores[0] = 70                               # replace the first item (lists are mutable): [70, 75, 82, 91]
scores.insert(1, 60)                         # put 60 at index 1, shifting others right: [70, 60, 75, 82, 91]
removed = scores.pop()                       # remove and RETURN the last item (91)
scores.remove(60)                            # delete the first item equal to 60
print(scores, "removed:", removed)           # [70, 75, 82] removed: 91
print(len(scores), sum(scores), min(scores), max(scores))    # count, total, smallest, largest
print(sum(scores) / len(scores))             # average
print(sorted(scores, reverse=True))          # a NEW list, largest first (original unchanged)
print(75 in scores)                          # membership test: True'''),
    demo('''# --- DEMO 4: aliasing versus copying ---------------------------------------------
first = [1, 2, 3]                            # an original list
alias = first                                # NOT a copy: a second NAME for the same list
real_copy = first.copy()                     # a genuinely separate list
first.append(99)                             # change the original
print("first    :", first)                   # [1, 2, 3, 99]
print("alias    :", alias)                   # [1, 2, 3, 99]  <- changed too!
print("real_copy:", real_copy)               # [1, 2, 3]       <- unaffected
print(first is alias, first is real_copy)    # "is" asks: same object? True False'''),
    demo('''# --- DEMO 5: nested lists (rows and columns) -----------------------------------------
marks = [                                    # a list of lists: each inner list is one student's two scores
    [70, 80],                                # student 0
    [55, 65],                                # student 1
    [90, 85],                                # student 2
]
print(marks[1])                              # the whole second row: [55, 65]
print(marks[1][0])                           # row 1, column 0: 55
for row in marks:                            # visit each student's row
    print(sum(row) / len(row))               # that student's average: 75.0, 60.0, 87.5
column_0 = [row[0] for row in marks]         # comprehension: first score of every student
print(column_0)                              # [70, 55, 90]'''),
    demo('''# --- DEMO 6: tuples and unpacking --------------------------------------------------
location = (6.5, 3.2)                        # a tuple: fixed latitude/longitude pair
latitude, longitude = location               # unpacking: first value to latitude, second to longitude
print(latitude, longitude)                   # 6.5 3.2
student = ("Tola", "Computer Science", 300)  # a fixed record: name, programme, level
name, programme, level = student             # unpack all three at once
print(f"{name} - {programme} - {level}")     # Tola - Computer Science - 300
# location[0] = 7.0                          # ERROR if uncommented: tuples are immutable
print(min(10, 3, 7), (1, 2) + (3,))          # tuples can be joined: (1, 2, 3)'''),
    activity(
        "Slicing detective",
        "Predict each line. Remember: **start included, stop excluded**, and negative indexes count from the end.",
        '''s = "COMPUTER"
print(s[2:5])      # slice A
print(s[:3])       # slice B
print(s[-3:])      # slice C
print(s[::2])      # slice D (every second character)
print(s[5:2])      # slice E (start after stop)''',
        "A `MPU`, B `COM`, C `TER`, D `CMUE` (indexes 0,2,4,6), E empty string (nothing, because start is after stop; slicing never raises an error)."),
    activity(
        "Who changed my list?",
        "Predict `a`, `b` and `c` after the changes, then explain why.",
        '''a = [1, 2, 3]
b = a
c = a[:]            # slicing the whole list makes a copy
b.append(4)
c.append(5)
print(a, b, c)''',
        "`[1, 2, 3, 4] [1, 2, 3, 4] [1, 2, 3, 5]`. `b` is an alias of `a`, so they are the same list; `c` is a copy (`a[:]`), so it changes independently. This is the #1 beginner list bug."),
    md("""## 🛠️ Tasks
"""),
    task(1, "Score list processor",
         "Write `class_stats(scores)` returning a tuple `(average, highest, lowest)`. Use `sum`, `max`, `min`, `len`. Round the average to 2 decimal places.",
         '''def class_stats(scores):
    # TODO
    pass

print(class_stats([68, 75, 82, 91]))''',
         '''def class_stats(scores):
    average = round(sum(scores) / len(scores), 2)   # total divided by count, rounded
    return average, max(scores), min(scores)        # three values -> a tuple

print(class_stats([68, 75, 82, 91]))                # (79.0, 91, 68)''',
         '''check(class_stats([68, 75, 82, 91]) == (79.0, 91, 68), "stats correct", "return (average, highest, lowest)")
check(class_stats([10, 20, 25]) == (18.33, 25, 10), "rounding to 2 dp", "use round(..., 2)")'''),
    task(2, "Inventory list manager",
         "Write four functions on a list of item names: `add_item(items, name)` (append if not already present), `remove_item(items, name)` (remove if present), `find_item(items, name)` (return its index or -1), `update_item(items, old, new)` (replace; return `True` if done, else `False`). All modify the list **in place**.",
         '''def add_item(items, name):
    # TODO
    pass

def remove_item(items, name):
    # TODO
    pass

def find_item(items, name):
    # TODO
    pass

def update_item(items, old, new):
    # TODO
    pass

stock = ["rice", "beans"]
add_item(stock, "garri")
print(stock)''',
         '''def add_item(items, name):
    if name not in items:                       # avoid duplicates
        items.append(name)                      # add at the end

def remove_item(items, name):
    if name in items:                           # only remove what exists (remove() raises an error otherwise)
        items.remove(name)

def find_item(items, name):
    if name in items:
        return items.index(name)                # index() gives the position of the first match
    return -1                                   # not found

def update_item(items, old, new):
    i = find_item(items, old)                   # reuse our own function
    if i == -1:
        return False                            # nothing to update
    items[i] = new                              # lists are mutable: replace in place
    return True

stock = ["rice", "beans"]
add_item(stock, "garri")                        # stock: rice, beans, garri
print(stock)''',
         '''s = ["rice", "beans"]
add_item(s, "garri"); add_item(s, "garri")
check(s == ["rice", "beans", "garri"], "add_item without duplicates", "only append when the name is not in the list")
remove_item(s, "beans"); remove_item(s, "yam")
check(s == ["rice", "garri"], "remove_item (and missing item is safe)", "check `name in items` before removing")
check(find_item(s, "garri") == 1 and find_item(s, "yam") == -1, "find_item", "return index or -1")
check(update_item(s, "rice", "ofada") is True and s[0] == "ofada" and update_item(s, "zzz", "q") is False, "update_item", "replace at the found index; return True/False")'''),
    task(3, "Sentence analyser",
         "Write `analyse(sentence)` returning a dictionary: `words` (word count), `longest` (the longest word; first one if tied) and `sorted_words` (words in alphabetical order, lower-case). Hint: `split()`.",
         '''def analyse(sentence):
    # TODO
    pass

print(analyse("Python is fun to learn"))''',
         '''def analyse(sentence):
    words = sentence.split()                           # cut the text at spaces -> list of words
    longest = words[0]                                 # assume the first word is longest ...
    for w in words:                                    # ... then look for a longer one
        if len(w) > len(longest):                      # strictly longer keeps the FIRST of equal lengths
            longest = w
    return {"words": len(words),
            "longest": longest,
            "sorted_words": sorted(w.lower() for w in words)}   # sorted() returns a new alphabetical list

print(analyse("Python is fun to learn"))''',
         '''r = analyse("Python is fun to learn")
check(r["words"] == 5, "5 words", "len(sentence.split())")
check(r["longest"] == "Python", "longest word is Python", "compare lengths; keep the first when tied")
check(r["sorted_words"] == ["fun", "is", "learn", "python", "to"], "alphabetical order", "sorted() of lower-case words")'''),
    task(4, "3 x 3 matrix row totals",
         "Write `row_totals(matrix)` returning a list with the sum of each row, and `column_totals(matrix)` returning the sum of each column. The matrix is a list of lists.",
         '''def row_totals(matrix):
    # TODO
    pass

def column_totals(matrix):
    # TODO (hint: for each column index, add row[col] across all rows)
    pass

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(row_totals(m), column_totals(m))''',
         '''def row_totals(matrix):
    return [sum(row) for row in matrix]                 # one sum per inner list

def column_totals(matrix):
    totals = []
    for col in range(len(matrix[0])):                   # for each column position
        total = 0
        for row in matrix:                              # go down the rows
            total += row[col]                           # add that column's value
        totals.append(total)
    return totals

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(row_totals(m), column_totals(m))                  # [6, 15, 24] [12, 15, 18]''',
         '''m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
check(row_totals(m) == [6, 15, 24], "row totals", "sum each inner list")
check(column_totals(m) == [12, 15, 18], "column totals", "add row[col] down every row")'''),
    task(5, "Extension: prove aliasing",
         "Write `demo_alias()` that: creates `first = [1, 2, 3]`, sets `second = first`, appends 4 to `first`, and returns `(first, second)`. Then write `demo_copy()` that does the same but with `second = first.copy()` and returns `(first, second)`.",
         '''def demo_alias():
    # TODO
    pass

def demo_copy():
    # TODO
    pass

print(demo_alias())
print(demo_copy())''',
         '''def demo_alias():
    first = [1, 2, 3]                       # original
    second = first                          # alias: same list, two names
    first.append(4)                         # change via one name ...
    return first, second                    # ... both show the change

def demo_copy():
    first = [1, 2, 3]
    second = first.copy()                   # independent copy
    first.append(4)                         # only `first` changes
    return first, second

print(demo_alias())                         # ([1, 2, 3, 4], [1, 2, 3, 4])
print(demo_copy())                          # ([1, 2, 3, 4], [1, 2, 3])''',
         '''check(demo_alias() == ([1, 2, 3, 4], [1, 2, 3, 4]), "alias shows the change in both", "second = first")
check(demo_copy() == ([1, 2, 3, 4], [1, 2, 3]), "copy is independent", "second = first.copy()")'''),
    quiz([
        ("Are strings mutable in Python?", "No. String methods return a new string; the original is unchanged."),
        ("What is the difference between `append()` and `extend()`?", "`append(x)` adds `x` as ONE item; `extend(items)` adds each item of an iterable separately."),
        ("What is a nested list?", "A list whose items are themselves lists, useful for rows and columns."),
        ("Give one practical reason to use a tuple.", "Its values cannot be changed accidentally, so it suits fixed records such as coordinates; tuples can also be dictionary keys."),
    ]),
    assignment(
        "**A.** Write `unique_in_order(names)` returning a new list with duplicates removed **preserving the original order** (do not use `set`, Pandas or `dict.fromkeys`).\n\n**B.** Write `student_averages(records)` where `records` is a list like `[[\"Amina\", 70, 80], [\"Tola\", 60, 50]]`; return a list of `(name, average)` tuples.\n\n**C.** In `mutability_note` explain *mutability* in your own words and give one reason to use a tuple.",
        '''def unique_in_order(names):
    # TODO
    pass

def student_averages(records):
    # TODO
    pass

mutability_note = ""   # TODO

print(unique_in_order(["Ada", "Bola", "Ada", "Chi", "Bola"]))
print(student_averages([["Amina", 70, 80], ["Tola", 60, 50]]))''',
        '''def unique_in_order(names):
    result = []                                  # new list we will build
    for n in names:                              # go through the original in order
        if n not in result:                      # skip names we already kept
            result.append(n)
    return result

def student_averages(records):
    out = []
    for rec in records:                          # e.g. ["Amina", 70, 80]
        name = rec[0]                            # first item is the name
        marks = rec[1:]                          # the rest are marks (a slice)
        out.append((name, sum(marks) / len(marks)))   # a (name, average) tuple
    return out

mutability_note = ("Mutability means an object can be changed in place after it is created. Lists are mutable; "
                   "strings and tuples are not. A tuple is useful for fixed data, such as a coordinate, "
                   "because it cannot be changed by mistake.")

print(unique_in_order(["Ada", "Bola", "Ada", "Chi", "Bola"]))   # ['Ada', 'Bola', 'Chi']
print(student_averages([["Amina", 70, 80], ["Tola", 60, 50]]))  # [('Amina', 75.0), ('Tola', 55.0)]''',
        '''check(unique_in_order(["Ada", "Bola", "Ada", "Chi", "Bola"]) == ["Ada", "Bola", "Chi"], "duplicates removed, order kept", "append only if not already in the result list")
check(student_averages([["Amina", 70, 80], ["Tola", 60, 50]]) == [("Amina", 75.0), ("Tola", 55.0)], "averages correct", "use rec[0] and rec[1:]")
check(len(mutability_note.split()) >= 15, "explanation written", "write 2 to 3 sentences")'''),
]


def build():
    return build_week(4, "strings_lists_tuples", "Strings and Built-in Collections I: Lists and Tuples",
                      OUTCOMES, ITEMS)
