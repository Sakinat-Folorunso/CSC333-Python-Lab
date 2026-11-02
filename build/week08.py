from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Implement **linear** and **binary search** and state the precondition of each.",
    "Implement **bubble sort** and **insertion sort** and test them on edge cases.",
    "Build a **singly linked list** from `Node` objects and explain how it differs from a Python list.",
    "Describe time complexity (`O(1)`, `O(log n)`, `O(n)`, `O(n²)`) and relate it to counted steps.",
    "Time algorithms fairly (repeated runs, mean ± standard deviation) and explain why timings vary.",
]

ITEMS = [
    md("""## 1. From *using* collections to *reasoning* about them
Two programs may give the same answer yet differ enormously in how **much work** they do as the data grows. **Algorithm analysis** lets us compare them without running them.

### Counting steps and Big-O
We describe growth with **Big-O notation**, ignoring constants and small terms.

| Class | Name | Meaning when the input size n doubles | Example |
|---|---|---|---|
| `O(1)` | constant | same work | `list[0]`, `dict[key]` |
| `O(log n)` | logarithmic | one more step | binary search |
| `O(n)` | linear | work doubles | linear search, `sum(list)` |
| `O(n log n)` | linearithmic | a bit more than double | good sorting (`sorted`) |
| `O(n²)` | quadratic | work **quadruples** | bubble / insertion sort |

### Searching
| Algorithm | Precondition | Idea | Worst case |
|---|---|---|---|
| **Linear search** | none | look at items one by one | `O(n)` |
| **Binary search** | list must be **sorted** | compare with the middle; discard half | `O(log n)` |

### Sorting (instructional algorithms)
- **Bubble sort:** repeatedly compare neighbours and swap if out of order; largest values “bubble” to the end.
- **Insertion sort:** keep a sorted left part; take the next item and *insert* it in the right place (like sorting playing cards in your hand).
- Both are `O(n²)` in the worst case. In real programs use `sorted()` / `list.sort()` (`O(n log n)`).

### Linked list
A **linked list** is a chain of **nodes**. Each node stores a `value` and a reference `next` to the following node; the list remembers the **head**.

```
head → [10 | •]→[20 | •]→[30 | None]
```
| Operation | Python `list` | Linked list |
|---|---|---|
| Access item `i` | `O(1)` | `O(n)` (must walk) |
| Insert/delete at the front | `O(n)` | `O(1)` |
| Memory | contiguous | scattered nodes + pointers |

### Always test the edge cases
**empty list · one element · duplicates · already sorted · reverse sorted · item not present.**
"""),
    demo('''# --- DEMO 1: linear search that also counts comparisons ---------------------
def linear_search(items, target):
    comparisons = 0                                  # how many items we looked at
    for index, value in enumerate(items):            # enumerate gives (position, value) pairs
        comparisons += 1                             # we are about to compare one item
        if value == target:                          # found it?
            return index, comparisons                # position and effort
    return -1, comparisons                           # looked at everything, not found

values = [12, 18, 25, 31, 44, 57]
print(linear_search(values, 31))                     # (3, 4): found at index 3 after 4 comparisons
print(linear_search(values, 99))                     # (-1, 6): not found after 6 comparisons'''),
    demo('''# --- DEMO 2: binary search (list MUST be sorted) -----------------------------
def binary_search(items, target):
    low, high = 0, len(items) - 1                    # the search window is the whole list
    comparisons = 0
    while low <= high:                               # while the window is not empty
        mid = (low + high) // 2                      # middle index (floor division)
        comparisons += 1
        if items[mid] == target:                     # lucky: the middle is the target
            return mid, comparisons
        if items[mid] < target:                      # target is bigger: discard the LEFT half
            low = mid + 1
        else:                                        # target is smaller: discard the RIGHT half
            high = mid - 1
    return -1, comparisons                           # window became empty

values = [12, 18, 25, 31, 44, 57]
print(binary_search(values, 31))                     # (3, 1): found with a single comparison
print(binary_search(values, 57))                     # (5, 3)
print(binary_search(list(range(1, 1001)), 1000))     # about 10 comparisons for 1000 items, not 1000!'''),
    demo('''# --- DEMO 3: bubble sort ---------------------------------------------------------
def bubble_sort(items):
    data = list(items)                               # work on a COPY so the caller's list is not changed
    n = len(data)
    for end in range(n - 1, 0, -1):                  # the unsorted part shrinks: end = n-1 ... 1
        swapped = False                              # did this pass change anything?
        for i in range(end):                         # compare neighbours up to `end`
            if data[i] > data[i + 1]:                # out of order?
                data[i], data[i + 1] = data[i + 1], data[i]   # swap in one line (tuple unpacking)
                swapped = True
        if not swapped:                              # a pass with no swaps means the list is sorted: stop early
            break
    return data

print(bubble_sort([5, 2, 9, 1, 5, 6]))               # [1, 2, 5, 5, 6, 9]
print(bubble_sort([]), bubble_sort([7]))             # [] [7]  edge cases'''),
    demo('''# --- DEMO 4: insertion sort ---------------------------------------------------------
def insertion_sort(items):
    data = list(items)                               # copy
    for i in range(1, len(data)):                    # data[0:i] is already sorted
        key = data[i]                                # the next card to place
        j = i - 1                                    # start looking at the item just before it
        while j >= 0 and data[j] > key:              # shift bigger items one place to the right
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key                            # drop the card into the gap
    return data

print(insertion_sort([5, 2, 9, 1, 5, 6]))            # [1, 2, 5, 5, 6, 9]
print(insertion_sort([3, 2, 1]) == sorted([3, 2, 1]))# True: compare with the built-in'''),
    demo('''# --- DEMO 5: a singly linked list --------------------------------------------------------
class Node:
    def __init__(self, value):
        self.value = value                           # the data stored in this node
        self.next = None                             # reference to the next node (None = end of the chain)

class LinkedList:
    def __init__(self):
        self.head = None                             # empty list: no first node yet

    def append(self, value):
        new_node = Node(value)                       # build the node
        if self.head is None:                        # list was empty
            self.head = new_node                     # the new node becomes the head
            return
        current = self.head                          # otherwise walk to the LAST node
        while current.next is not None:              # stop when there is no next node
            current = current.next
        current.next = new_node                      # link the new node at the end

    def to_list(self):
        items = []
        current = self.head                          # start at the head
        while current is not None:                   # visit every node
            items.append(current.value)
            current = current.next                   # move along the chain
        return items

ll = LinkedList()
for v in [10, 20, 30]:                               # add three values
    ll.append(v)
print(ll.to_list())                                  # [10, 20, 30]'''),
    demo('''# --- DEMO 6: timing algorithms fairly ----------------------------------------------------------
import random                                        # for reproducible test data
import statistics                                    # mean and standard deviation
import time                                          # perf_counter: a high-resolution stopwatch

random.seed(42)                                      # same "random" data every run
data = [random.randint(0, 10_000) for _ in range(800)]   # 800 random integers

def time_it(fn, data, repeats=5):
    times = []
    for _ in range(repeats):                         # repeat: one timing is unreliable
        start = time.perf_counter()                  # stopwatch on
        fn(data)                                     # run the algorithm
        times.append(time.perf_counter() - start)    # stopwatch off; store the elapsed seconds
    return statistics.mean(times), statistics.stdev(times)   # report mean and spread

for name, fn in [("bubble", bubble_sort), ("insertion", insertion_sort), ("built-in sorted", sorted)]:
    mean, sd = time_it(fn, data)
    print(f"{name:<16} mean {mean*1000:8.3f} ms  (sd {sd*1000:.3f} ms)")
# Timings depend on hardware, input and implementation: use them to see TRENDS, not exact values.'''),
    activity(
        "Count the comparisons",
        "For the sorted list `[2, 4, 6, 8, 10, 12, 14]`, how many comparisons does linear search need for 14? What about binary search? Predict, then run.",
        '''items = [2, 4, 6, 8, 10, 12, 14]
print("linear :", linear_search(items, 14))
print("binary :", binary_search(items, 14))
print("binary for 8:", binary_search(items, 8))''',
        "Linear: 7 comparisons (it must check every item). Binary: 3 (middle 8, then 12, then 14). For 8 binary needs only 1 (it is the middle). Binary search's advantage grows with the size of the list."),
    activity(
        "Why must binary search have a sorted list?",
        "Run binary search on an **unsorted** list and compare with linear search. Explain the wrong answer.",
        '''messy = [31, 7, 25, 3, 44, 12]
print("linear:", linear_search(messy, 3))
print("binary:", binary_search(messy, 3))''',
        "Linear finds 3 at index 3. Binary returns `-1` (not found) because it compares with the middle value (25) and wrongly discards the half that actually contains 3. Binary search relies on the order to know which half to discard."),
    md("""## 🛠️ Tasks
The demos above are available in your notebook session; in each task you will **write your own version**.
"""),
    task(1, "Search with comparison counts",
         "Write `linear_search_count(items, target)` and `binary_search_count(items, target)`. Each returns `(index, comparisons)`; use `-1` when absent. Binary search assumes a sorted list.",
         '''def linear_search_count(items, target):
    # TODO
    pass

def binary_search_count(items, target):
    # TODO
    pass

data = list(range(1, 101))
print(linear_search_count(data, 100))
print(binary_search_count(data, 100))''',
         '''def linear_search_count(items, target):
    comparisons = 0
    for i, value in enumerate(items):                  # look at items one by one
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons                             # absent

def binary_search_count(items, target):
    low, high, comparisons = 0, len(items) - 1, 0
    while low <= high:                                 # window not empty
        mid = (low + high) // 2
        comparisons += 1
        if items[mid] == target:
            return mid, comparisons
        if items[mid] < target:
            low = mid + 1                              # discard left half
        else:
            high = mid - 1                             # discard right half
    return -1, comparisons

data = list(range(1, 101))
print(linear_search_count(data, 100))                  # (99, 100)
print(binary_search_count(data, 100))                  # (99, 7)''',
         '''data = list(range(1, 101))
check(linear_search_count(data, 100) == (99, 100), "linear: found last item after 100 comparisons", "count every comparison, return (index, comparisons)")
i, c = binary_search_count(data, 100)
check(i == 99 and c <= 7, "binary: found with at most 7 comparisons", "halve the window each time")
check(linear_search_count(data, 500)[0] == -1 and binary_search_count(data, 500)[0] == -1, "absent item gives -1", "return -1 after the loop")
check(binary_search_count([], 1) == (-1, 0) and linear_search_count([], 1) == (-1, 0), "empty list handled", "no comparisons on an empty list")'''),
    task(2, "Bubble sort",
         "Write `bubble_sort(items)` returning a **new sorted list** and leaving the input unchanged. Include the early-exit optimisation (stop if a pass makes no swap).",
         '''def bubble_sort(items):
    # TODO
    pass

print(bubble_sort([5, 2, 9, 1, 5, 6]))''',
         '''def bubble_sort(items):
    data = list(items)                                 # copy: never mutate the caller's list
    for end in range(len(data) - 1, 0, -1):            # shrinking unsorted region
        swapped = False
        for i in range(end):
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                swapped = True
        if not swapped:                                # already sorted: stop early
            break
    return data

print(bubble_sort([5, 2, 9, 1, 5, 6]))''',
         '''cases = [[], [7], [2, 1], [1, 2, 3], [3, 2, 1], [5, 2, 9, 1, 5, 6], [4, 4, 4]]
wrong = [c for c in cases if bubble_sort(c) != sorted(c)]
check(not wrong, "all edge cases sorted (empty, one, duplicates, sorted, reversed)", f"wrong on: {wrong}")
original = [3, 1, 2]
bubble_sort(original)
check(original == [3, 1, 2], "input list is not modified", "start with data = list(items)")'''),
    task(3, "Insertion sort and duplicates",
         "Write `insertion_sort(items)` (new list). Then write `matches_builtin(items)` returning `True` when your sort gives exactly the same result as `sorted(items)`; use it on lists with **duplicates**.",
         '''def insertion_sort(items):
    # TODO
    pass

def matches_builtin(items):
    # TODO
    pass

print(matches_builtin([3, 1, 3, 2, 1]))''',
         '''def insertion_sort(items):
    data = list(items)
    for i in range(1, len(data)):                      # left part data[:i] is sorted
        key = data[i]                                  # card to insert
        j = i - 1
        while j >= 0 and data[j] > key:                # shift larger cards right
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key                              # place the card
    return data

def matches_builtin(items):
    return insertion_sort(items) == sorted(items)      # compare with Python's trusted result

print(matches_builtin([3, 1, 3, 2, 1]))                # True''',
         '''import random
rng = random.Random(42)                                 # reproducible test data (seed 42)
trials = [[rng.randint(0, 5) for _ in range(rng.randint(0, 12))] for _ in range(100)]   # many duplicates
check(all(matches_builtin(t) for t in trials), "100 random lists with duplicates match sorted()", "make sure shifting uses data[j] > key")
check(insertion_sort([]) == [] and insertion_sort([1]) == [1], "empty and single", "range(1, 0) is empty, which is fine")'''),
    task(4, "Singly linked list",
         "Complete `LinkedList`: `append(value)`, `to_list()`, `find(value)` (True/False), `delete(value)` (remove the **first** match; return `True` if removed else `False`) and `__len__`. `Node` is given.",
         '''class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        # TODO
        pass

    def to_list(self):
        # TODO
        pass

    def find(self, value):
        # TODO
        pass

    def delete(self, value):
        # TODO (hint: handle the head separately, then keep track of `previous`)
        pass

    def __len__(self):
        # TODO
        pass

ll = LinkedList()
ll.append(1); ll.append(2)
print(ll.to_list())''',
         '''class Node:
    def __init__(self, value):
        self.value = value                             # stored data
        self.next = None                               # link to the next node

class LinkedList:
    def __init__(self):
        self.head = None                               # empty list

    def append(self, value):
        node = Node(value)
        if self.head is None:                          # empty: new node is the head
            self.head = node
            return
        current = self.head
        while current.next is not None:                # walk to the last node
            current = current.next
        current.next = node                            # attach at the end

    def to_list(self):
        out, current = [], self.head
        while current is not None:                     # visit every node
            out.append(current.value)
            current = current.next
        return out

    def find(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def delete(self, value):
        if self.head is None:                          # nothing to delete
            return False
        if self.head.value == value:                   # deleting the head: move head forward
            self.head = self.head.next
            return True
        previous, current = self.head, self.head.next  # keep a pointer to the node BEFORE current
        while current is not None:
            if current.value == value:
                previous.next = current.next           # skip over the node: unlink it
                return True
            previous, current = current, current.next
        return False

    def __len__(self):
        return len(self.to_list())                     # simple (O(n)) but correct

ll = LinkedList()
ll.append(1); ll.append(2)
print(ll.to_list())                                    # [1, 2]''',
         '''ll = LinkedList()
check(ll.to_list() == [] and len(ll) == 0 and ll.delete(1) is False, "empty list behaves", "head is None means empty")
for v in [10, 20, 30, 20]:
    ll.append(v)
check(ll.to_list() == [10, 20, 30, 20] and len(ll) == 4, "append and length", "walk to the end and link a new Node")
check(ll.find(30) is True and ll.find(99) is False, "find", "walk the chain comparing values")
check(ll.delete(20) is True and ll.to_list() == [10, 30, 20], "delete first match in the middle", "previous.next = current.next")
check(ll.delete(10) is True and ll.to_list() == [30, 20], "delete the head", "head = head.next")
check(ll.delete(20) is True and ll.to_list() == [30] and ll.delete(99) is False, "delete the tail / missing", "return False when not found")'''),
    task(5, "Algorithm summary table",
         "Complete the dictionary `summary`. For each algorithm give `precondition`, `complexity` (exactly one of `\"O(1)\"`, `\"O(log n)\"`, `\"O(n)\"`, `\"O(n^2)\"` for its **worst case**) and a short `use_case` text.",
         '''summary = {
    "linear search":  {"precondition": "", "complexity": "", "use_case": ""},
    "binary search":  {"precondition": "", "complexity": "", "use_case": ""},
    "bubble sort":    {"precondition": "", "complexity": "", "use_case": ""},
    "insertion sort": {"precondition": "", "complexity": "", "use_case": ""},
}
print(summary["binary search"])''',
         '''summary = {
    "linear search":  {"precondition": "none", "complexity": "O(n)",
                       "use_case": "small or unsorted data, e.g. find a name in a short list"},
    "binary search":  {"precondition": "list must be sorted", "complexity": "O(log n)",
                       "use_case": "fast lookup in a large sorted list, e.g. a sorted student register"},
    "bubble sort":    {"precondition": "none", "complexity": "O(n^2)",
                       "use_case": "teaching, or tiny lists; real programs use sorted()"},
    "insertion sort": {"precondition": "none", "complexity": "O(n^2)",
                       "use_case": "small or nearly sorted lists, or adding items to a sorted list one by one"},
}
print(summary["binary search"])''',
         '''allowed = {"O(1)", "O(log n)", "O(n)", "O(n^2)"}
check(all(v["complexity"] in allowed for v in summary.values()), "complexities use the allowed labels", "use exactly O(n), O(log n) or O(n^2)")
check(summary["linear search"]["complexity"] == "O(n)" and summary["binary search"]["complexity"] == "O(log n)", "search complexities", "linear O(n), binary O(log n)")
check(summary["bubble sort"]["complexity"] == "O(n^2)" and summary["insertion sort"]["complexity"] == "O(n^2)", "sorting complexities", "both simple sorts are O(n^2)")
check("sorted" in summary["binary search"]["precondition"], "binary search needs a sorted list", "state the precondition")
check(all(len(v["use_case"]) > 8 for v in summary.values()), "use cases written", "fill every use_case")'''),
    task(6, "Extension: fair timing",
         "Write `time_function(fn, data, repeats=5)` returning `(mean_seconds, std_seconds)` using `time.perf_counter()` and `statistics`. Run your `bubble_sort` and `sorted` on 500 random numbers (seed 42) and write one comment about *why exact numbers differ between computers*.",
         '''import random, statistics, time

def time_function(fn, data, repeats=5):
    # TODO: time `fn(data)` `repeats` times and return (mean, standard deviation)
    pass

random.seed(42)
sample = [random.randint(0, 1000) for _ in range(500)]
print(time_function(sorted, sample))

# Why do timings differ between computers? (write your answer as a comment)''',
         '''import random, statistics, time

def time_function(fn, data, repeats=5):
    times = []                                         # elapsed seconds for each repeat
    for _ in range(repeats):
        start = time.perf_counter()                    # start the stopwatch
        fn(data)                                       # run the function being measured
        times.append(time.perf_counter() - start)      # elapsed = now - start
    return statistics.mean(times), statistics.stdev(times)

random.seed(42)                                        # reproducible data
sample = [random.randint(0, 1000) for _ in range(500)]
print(time_function(sorted, sample))
print(time_function(bubble_sort, sample))

# Timings differ between computers because of processor speed, other programs running,
# Python version and memory/caching: compare algorithms on the SAME machine and look at trends.''',
         '''m, s = time_function(sorted, sample)
check(isinstance(m, float) and m > 0 and isinstance(s, float) and s >= 0, "returns (mean, std) as positive floats", "use statistics.mean and statistics.stdev on the list of times")
mb, _ = time_function(bubble_sort, sample)
check(mb > m, "bubble sort is slower than sorted() on 500 items", "bubble sort is O(n^2); sorted() is O(n log n)")'''),
    quiz([
        ("What is the precondition for binary search?", "The list must already be sorted."),
        ("What does `O(n)` describe?", "Work that grows in direct proportion to the input size n (double the data, double the steps)."),
        ("Why test empty and one-element inputs?", "They are common edge cases where loops may not run or indexes may fail; correct code must handle them."),
        ("Why is a linked list slower than a Python list for `items[500]`?", "It has no index: to reach node 500 you must follow 500 links from the head, so access is O(n)."),
    ]),
    assignment(
        "**A.** In `why_sorted`, explain in 2 to 3 sentences why binary search cannot be applied directly to an unsorted list.\n\n**B.** In `use_cases`, give a *practical* use case for each of: `stack`, `queue`, `linked_list`, `dictionary`.\n\n**C.** Write `verify_sort(sort_fn, trials=50)`: using `random.Random(42)` generate `trials` random lists (length 0 to 15, values 0 to 9 so duplicates are common) and return `True` only if `sort_fn(list)` equals `sorted(list)` for every one.",
        '''import random

why_sorted = ""        # TODO

use_cases = {
    "stack": "",
    "queue": "",
    "linked_list": "",
    "dictionary": "",
}

def verify_sort(sort_fn, trials=50):
    # TODO
    pass

print(verify_sort(insertion_sort))''',
        '''import random

why_sorted = ("Binary search compares the target with the middle item and then throws away one half. "
              "That only works if the order tells us which half can contain the target. "
              "In an unsorted list the discarded half may contain the item, so the search can miss it.")

use_cases = {
    "stack": "The Undo button in an editor, or the Back button in a browser (last action is reversed first).",
    "queue": "A print queue or helpdesk tickets served first-come, first-served.",
    "linked_list": "A playlist or text-editor buffer where items are inserted and removed often in the middle.",
    "dictionary": "A phone book or a student register looked up by matric number.",
}

def verify_sort(sort_fn, trials=50):
    rng = random.Random(42)                                       # reproducible generator
    for _ in range(trials):
        data = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]   # random length, many duplicates
        if sort_fn(data) != sorted(data):                         # compare with the built-in
            return False                                          # one failure is enough
    return True

print(verify_sort(insertion_sort))                                # True''',
        '''check(len(why_sorted.split()) >= 20, "explanation written", "write 2 to 3 sentences")
check(set(use_cases) == {"stack", "queue", "linked_list", "dictionary"} and all(len(v.split()) >= 4 for v in use_cases.values()), "four use cases", "one practical example each")
check(verify_sort(insertion_sort) is True and verify_sort(bubble_sort) is True, "your sorts pass verify_sort", "compare sort_fn(data) with sorted(data) for every trial")
check(verify_sort(lambda x: x) is False, "verify_sort detects a wrong sort", "return False as soon as a result differs")'''),
]


def build():
    return build_week(8, "data_structures_and_algorithms", "Data Structures and Algorithms: Linked Structures, Searching and Sorting",
                      OUTCOMES, ITEMS)
