from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Create and manipulate **dictionaries** and **sets**, including safe lookup with `get()`.",
    "Represent structured records using dictionaries and lists of dictionaries.",
    "Use set operations (union, intersection, difference) to compare groups.",
    "Explain **stack (LIFO)** and **queue (FIFO)** behaviour and implement both with a list and `collections.deque`.",
    "Choose the right structure (list, tuple, set, dictionary) for a given problem.",
]

ITEMS = [
    md("""## 1. Dictionaries: look things up by *name*, not by position
A **dictionary** (`dict`) stores **key → value** pairs. It is the data structure behind phone books, settings and almost every record you will meet.

```python
student = {"name": "Tola", "programme": "Computer Science", "level": 300}
student["name"]            # "Tola"      (look up by key)
student["cgpa"] = 4.1      # add or update a pair
```
- Keys must be **unique** and **immutable** (strings, numbers, tuples).
- Lookup by key is **very fast**, no matter how many items.
- `d["missing"]` raises `KeyError`; `d.get("missing")` returns `None` (or a default you choose) instead.
- Useful methods: `keys()` `values()` `items()` `get()` `update()` `pop()`.

## 2. Sets: unique items and maths-style comparison
A **set** is an unordered collection **without duplicates**: `{"CSC", "ICT"}`.
- `set(list)` is the quickest way to remove duplicates (order is lost).
- Operations: `a | b` union · `a & b` intersection · `a - b` difference · `a ^ b` symmetric difference.
- Membership test (`x in my_set`) is very fast.
- Empty set: `set()` (because `{}` is an empty *dictionary*!).

## 3. Abstract data structures: stack and queue
They are defined by **behaviour**, not by Python syntax.

| Structure | Rule | Real-life picture | Core operations |
|---|---|---|---|
| **Stack** | **L**ast **I**n, **F**irst **O**ut (LIFO) | a pile of plates; browser *Back* button; *Undo* | `push`, `pop`, `peek` |
| **Queue** | **F**irst **I**n, **F**irst **O**ut (FIFO) | a line at the bank; print jobs; support tickets | `enqueue`, `dequeue` |

- A list works well as a stack (`append` / `pop`).
- For queues use `collections.deque`: removing from the **front** of a list is slow, but `deque.popleft()` is fast.
- **Underflow** = trying to remove from an empty stack/queue. Always handle it.

## 4. Choosing the right structure
| Need | Use |
|---|---|
| ordered, changeable collection | `list` |
| fixed record that must not change | `tuple` |
| uniqueness / fast membership / set maths | `set` |
| look up by a label (key) | `dict` |
| undo / back / depth-first | stack |
| fairness / first come first served | queue |
"""),
    demo('''# --- DEMO 1: a dictionary record ---------------------------------------------
student = {                                        # curly braces with key: value pairs
    "name": "Tola",                                # key "name"  -> value "Tola"
    "programme": "Computer Science",               # key "programme"
    "scores": [72, 81, 77],                        # a value may itself be a list
}
average = sum(student["scores"]) / len(student["scores"])   # read the list by key, then compute the average
student["average"] = round(average, 2)             # adding a NEW key just by assigning to it
student["programme"] = "Data Science"              # assigning to an EXISTING key replaces its value
print(student["name"])                             # Tola
print(student.get("average"))                      # 76.67
print(student.get("cgpa"))                         # None: get() does not crash on a missing key
print(student.get("cgpa", "not recorded"))         # a default value to use when the key is missing
print("name" in student)                           # membership checks KEYS: True'''),
    demo('''# --- DEMO 2: looping through a dictionary ---------------------------------------
prices = {"rice": 1200, "beans": 900, "garri": 500}    # item -> price in naira
for item in prices:                                    # looping over a dict gives the KEYS
    print(item)                                        # rice, beans, garri
for item, price in prices.items():                     # items() gives (key, value) pairs; we unpack each pair
    print(f"{item:<6} N{price:,}")                     # aligned, with thousands separator
print(list(prices.keys()))                             # ['rice', 'beans', 'garri']
print(sum(prices.values()))                            # 2600: add up all the values
prices.update({"yam": 1500, "rice": 1300})             # update(): add yam, change rice
print(prices.pop("beans"))                             # pop() removes a key and RETURNS its value: 900
print(prices)                                          # {'rice': 1300, 'garri': 500, 'yam': 1500}'''),
    demo('''# --- DEMO 3: list of dictionaries (a mini table) ------------------------------------
students = [                                           # each dictionary is one row of the "table"
    {"name": "Amina", "programme": "CS", "score": 78},
    {"name": "Tola", "programme": "DS", "score": 91},
    {"name": "Chika", "programme": "CS", "score": 67},
]
for s in students:                                     # visit each row
    print(s["name"], s["score"])                       # read two columns of the row
cs_scores = [s["score"] for s in students if s["programme"] == "CS"]   # filter rows, collect one column
print(cs_scores)                                       # [78, 67]
by_programme = {}                                      # build a dictionary of programme -> list of names
for s in students:                                     # go through each student
    by_programme.setdefault(s["programme"], []).append(s["name"])   # setdefault: create the list if absent, then append
print(by_programme)                                    # {'CS': ['Amina', 'Chika'], 'DS': ['Tola']}'''),
    demo('''# --- DEMO 4: sets ------------------------------------------------------------------------
group_a = {"CSC", "ICT", "DTS"}                        # courses taken by group A
group_b = {"DTS", "SEN", "CSC"}                        # courses taken by group B
print(group_a & group_b)                               # intersection (in BOTH): {'CSC', 'DTS'}
print(group_a | group_b)                               # union (in EITHER): all four courses
print(group_a - group_b)                               # difference (only in A): {'ICT'}
print(group_a ^ group_b)                               # symmetric difference (in exactly one): {'ICT', 'SEN'}
emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]  # a list with a duplicate
print(len(emails), len(set(emails)))                   # 4 3 : converting to a set removed the duplicate
print("b@x.com" in set(emails))                        # fast membership test: True'''),
    demo('''# --- DEMO 5: a stack (LIFO) with a list ---------------------------------------------------
stack = []                                             # an empty stack
stack.append("task A")                                 # PUSH: put on top
stack.append("task B")                                 # push another
stack.append("task C")                                 # and another: stack is A, B, C (C on top)
print(stack[-1])                                       # PEEK: look at the top without removing: task C
print(stack.pop())                                     # POP: remove and return the TOP: task C
print(stack.pop())                                     # task B (last in, first out)
print(stack)                                           # ['task A']
print(len(stack) == 0)                                 # is the stack empty? False'''),
    demo('''# --- DEMO 6: a queue (FIFO) with deque -----------------------------------------------------
from collections import deque                          # deque = "double-ended queue", fast at both ends
queue = deque()                                        # an empty queue
queue.append("ticket 1")                               # ENQUEUE: join the BACK of the line
queue.append("ticket 2")
queue.append("ticket 3")
print(queue.popleft())                                 # DEQUEUE: serve the FRONT: ticket 1 (first in, first out)
print(queue)                                           # deque(['ticket 2', 'ticket 3'])
print(queue[0])                                        # look at the front without removing: ticket 2
print(len(queue))                                      # how many are waiting: 2'''),
    activity(
        "LIFO or FIFO?",
        "The same four items are added in the order **A, B, C, D**. Then two items are removed. Write down what remains for a stack and for a queue.",
        '''from collections import deque
stack = []
queue = deque()
for item in ["A", "B", "C", "D"]:      # add four items to each
    stack.append(item)
    queue.append(item)
stack.pop(); stack.pop()               # remove two from the stack
queue.popleft(); queue.popleft()       # remove two from the queue
print("stack:", stack)
print("queue:", list(queue))''',
        "Stack keeps `['A', 'B']` (D and C, the *latest*, were removed). Queue keeps `['C', 'D']` (A and B, the *earliest*, were removed). Same input, opposite policy."),
    activity(
        "Why did my set shrink?",
        "Predict the output. Is the order guaranteed? What happens to `{}`?",
        '''nums = [3, 1, 3, 2, 1, 3]
print(set(nums))
print(len(nums), len(set(nums)))
print(type({}), type(set()))
print({1, 2} | {2, 3})''',
        "`{1, 2, 3}`, `6 3`, `<class 'dict'> <class 'set'>`, `{1, 2, 3}`. Sets drop duplicates and have no promised order. `{}` is an empty **dict**; use `set()` for an empty set."),
    md("""## 🛠️ Tasks
In these tasks the stack and queue are passed to *functions*. (In Week 7 you will wrap them in classes.)
"""),
    task(1, "Student record with average",
         "Write `make_record(name, programme, scores)` returning a dictionary with keys `name`, `programme`, `scores` and `average` (rounded to 2 dp).",
         '''def make_record(name, programme, scores):
    # TODO: build and return the dictionary
    pass

print(make_record("Tola", "Data Science", [72, 81, 77]))''',
         '''def make_record(name, programme, scores):
    record = {"name": name, "programme": programme, "scores": scores}   # the basic fields
    record["average"] = round(sum(scores) / len(scores), 2)             # add the computed field
    return record

print(make_record("Tola", "Data Science", [72, 81, 77]))''',
         '''r = make_record("Tola", "Data Science", [72, 81, 77])
check(r["average"] == 76.67, "average is 76.67", "round(sum / len, 2)")
check(set(r) == {"name", "programme", "scores", "average"}, "all four keys", "keys: name, programme, scores, average")'''),
    task(2, "Contact book",
         "Write functions on a dictionary `book` (name → phone): `add_contact(book, name, phone)`, `find_contact(book, name)` (return the phone or `\"Not found\"`), `update_contact(book, name, phone)` (return `True` if the contact existed), `delete_contact(book, name)` (return `True` if deleted).",
         '''def add_contact(book, name, phone):
    # TODO
    pass

def find_contact(book, name):
    # TODO: use get() with a default
    pass

def update_contact(book, name, phone):
    # TODO
    pass

def delete_contact(book, name):
    # TODO
    pass

book = {}
add_contact(book, "Ada", "0801")
print(find_contact(book, "Ada"))''',
         '''def add_contact(book, name, phone):
    book[name] = phone                         # create the pair (or overwrite)

def find_contact(book, name):
    return book.get(name, "Not found")         # get() with a default never crashes

def update_contact(book, name, phone):
    if name in book:                           # only update an existing contact
        book[name] = phone
        return True
    return False

def delete_contact(book, name):
    if name in book:
        del book[name]                         # del removes the key and its value
        return True
    return False

book = {}
add_contact(book, "Ada", "0801")
print(find_contact(book, "Ada"))               # 0801''',
         '''b = {}
add_contact(b, "Ada", "0801"); add_contact(b, "Bola", "0802")
check(find_contact(b, "Ada") == "0801" and find_contact(b, "Zed") == "Not found", "find_contact", "use book.get(name, 'Not found')")
check(update_contact(b, "Ada", "0999") is True and b["Ada"] == "0999" and update_contact(b, "Zed", "1") is False, "update_contact", "update only if the name exists")
check(delete_contact(b, "Bola") is True and "Bola" not in b and delete_contact(b, "Bola") is False, "delete_contact", "delete only if present, return True/False")'''),
    task(3, "Compare course registrations with sets",
         "Write `compare_groups(a, b)` taking two lists of course codes and returning a dictionary with sorted lists: `common`, `only_a`, `only_b` and `all`.",
         '''def compare_groups(a, b):
    # TODO: convert to sets, then use & - |
    pass

print(compare_groups(["CSC", "ICT", "DTS"], ["DTS", "SEN", "CSC"]))''',
         '''def compare_groups(a, b):
    sa, sb = set(a), set(b)                    # sets remove duplicates and allow set maths
    return {
        "common": sorted(sa & sb),             # in both groups
        "only_a": sorted(sa - sb),             # only in a
        "only_b": sorted(sb - sa),             # only in b
        "all": sorted(sa | sb),                # everything
    }

print(compare_groups(["CSC", "ICT", "DTS"], ["DTS", "SEN", "CSC"]))''',
         '''r = compare_groups(["CSC", "ICT", "DTS"], ["DTS", "SEN", "CSC"])
check(r["common"] == ["CSC", "DTS"], "common", "intersection a & b")
check(r["only_a"] == ["ICT"] and r["only_b"] == ["SEN"], "only_a / only_b", "differences a - b and b - a")
check(r["all"] == ["CSC", "DTS", "ICT", "SEN"], "all", "union a | b")'''),
    task(4, "Undo stack",
         "Write `push(stack, item)`, `pop(stack)` and `peek(stack)`. `pop` and `peek` on an empty stack must return the text `\"Stack is empty\"` (**underflow handling**, the extension challenge).",
         '''def push(stack, item):
    # TODO
    pass

def pop(stack):
    # TODO
    pass

def peek(stack):
    # TODO
    pass

history = []
push(history, "page1")
push(history, "page2")
print(pop(history))''',
         '''def push(stack, item):
    stack.append(item)                          # put on TOP (end of the list)

def pop(stack):
    if len(stack) == 0:                         # underflow: nothing to remove
        return "Stack is empty"
    return stack.pop()                          # remove and return the top

def peek(stack):
    if len(stack) == 0:
        return "Stack is empty"
    return stack[-1]                            # look at the top without removing

history = []
push(history, "page1")
push(history, "page2")
print(pop(history))                             # page2''',
         '''h = []
check(pop(h) == "Stack is empty" and peek(h) == "Stack is empty", "underflow handled", "test len(stack) == 0 first")
push(h, "a"); push(h, "b")
check(peek(h) == "b" and pop(h) == "b" and pop(h) == "a", "LIFO order", "the LAST item pushed leaves first")'''),
    task(5, "ICT support queue",
         "Write `enqueue(q, ticket)`, `dequeue(q)` and `size(q)` for a `deque`. `dequeue` on an empty queue returns `\"Queue is empty\"`.",
         '''from collections import deque

def enqueue(q, ticket):
    # TODO
    pass

def dequeue(q):
    # TODO
    pass

def size(q):
    # TODO
    pass

support = deque()
enqueue(support, "printer jammed")
print(size(support))''',
         '''from collections import deque

def enqueue(q, ticket):
    q.append(ticket)                            # join at the BACK

def dequeue(q):
    if len(q) == 0:                             # underflow
        return "Queue is empty"
    return q.popleft()                          # serve the FRONT

def size(q):
    return len(q)

support = deque()
enqueue(support, "printer jammed")
print(size(support))                            # 1''',
         '''q = deque()
check(dequeue(q) == "Queue is empty", "underflow handled", "check len(q) == 0")
enqueue(q, "t1"); enqueue(q, "t2"); enqueue(q, "t3")
check(dequeue(q) == "t1" and dequeue(q) == "t2" and size(q) == 1, "FIFO order", "the FIRST ticket in leaves first (popleft)")'''),
    quiz([
        ("What is the difference between a set and a list?", "A list is ordered and allows duplicates; a set has unique items, no promised order and very fast membership tests."),
        ("Explain LIFO and FIFO.", "LIFO (stack): the last item added is the first removed. FIFO (queue): the first item added is the first removed."),
        ("What problem does `dict.get()` help prevent?", "A `KeyError` when a key might be missing; it returns `None` or a default instead."),
        ("Why is `{}` not an empty set?", "`{}` creates an empty dictionary; use `set()` for an empty set."),
    ]),
    assignment(
        "**A.** Write `build_inventory(items)` where `items` is a list of `(code, name, quantity)` tuples; return a dictionary keyed by `code` whose values are dictionaries `{\"name\": ..., \"quantity\": ...}`.\n\n**B.** Write `serve_all(requests)` taking a list of request texts; add them to a `deque`, then serve them in order and return the list of served requests (demonstrating FIFO).\n\n**C.** In `set_vs_dict` explain why a set is useful for duplicate removal and a dictionary for lookup.",
        '''from collections import deque

def build_inventory(items):
    # TODO
    pass

def serve_all(requests):
    # TODO
    pass

set_vs_dict = ""   # TODO

print(build_inventory([("A1", "pen", 10), ("B2", "book", 4)]))
print(serve_all(["r1", "r2", "r3"]))''',
        '''from collections import deque

def build_inventory(items):
    inventory = {}                                       # code -> details
    for code, name, quantity in items:                   # unpack each tuple directly in the loop header
        inventory[code] = {"name": name, "quantity": quantity}
    return inventory

def serve_all(requests):
    q = deque(requests)                                  # deque can be built from a list
    served = []
    while len(q) > 0:                                    # until the queue is empty
        served.append(q.popleft())                       # serve the front request
    return served

set_vs_dict = ("A set stores only unique items, so converting a list to a set removes duplicates quickly. "
               "A dictionary maps a key to a value, so you can look up a record directly by its key "
               "instead of searching through every item.")

print(build_inventory([("A1", "pen", 10), ("B2", "book", 4)]))
print(serve_all(["r1", "r2", "r3"]))                     # ['r1', 'r2', 'r3'] (FIFO)''',
        '''inv = build_inventory([("A1", "pen", 10), ("B2", "book", 4)])
check(inv == {"A1": {"name": "pen", "quantity": 10}, "B2": {"name": "book", "quantity": 4}}, "inventory built", "key = code, value = dict with name and quantity")
check(serve_all(["r1", "r2", "r3"]) == ["r1", "r2", "r3"], "served in arrival order", "use popleft()")
check(len(set_vs_dict.split()) >= 15, "explanation written", "write 2 to 3 sentences")'''),
]


def build():
    return build_week(5, "dictionaries_sets_stacks_queues", "Built-in Collections II: Dictionaries, Sets and Introductory Abstract Structures",
                      OUTCOMES, ITEMS)
