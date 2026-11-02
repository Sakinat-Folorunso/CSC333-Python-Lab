from lib import md, demo, activity, task, quiz, assignment, build_week

OUTCOMES = [
    "Define classes and create objects (instances) with `__init__`, attributes and methods.",
    "Explain `self` and distinguish **instance attributes** from **class attributes**.",
    "Apply **encapsulation**: protect an object's data with validation, `_private` names and `@property`.",
    "Give objects readable text with `__str__` and `__repr__`.",
    "Recognise **inheritance** and **polymorphism** in a short preview.",
]

ITEMS = [
    md("""## 1. Why object-oriented programming (OOP)?
Until now data (a dictionary) and behaviour (functions) lived apart. In **OOP** we bundle them: a **class** is a *blueprint*; an **object** is one *thing built from the blueprint*.

| Term | Meaning | Example |
|---|---|---|
| **class** | blueprint / template | `Student` |
| **object / instance** | one concrete thing | `amina = Student("Amina", "DS")` |
| **attribute** | data stored in the object | `amina.name` |
| **method** | function belonging to the class | `amina.add_score(80)` |
| **constructor** | `__init__`: runs automatically when an object is created | sets the starting state |
| **`self`** | the object the method is working on | `self.name` |

### Instance vs class attributes
- **Instance attribute** (`self.name`): each object has its own copy.
- **Class attribute** (written in the class body): *shared* by all objects (`institution = "OOU"`).

### Encapsulation = keep the data valid
Do not let outside code put an object into a nonsense state (negative balance, score of 500). Provide **methods** that check the rules, mark internal data with a leading underscore (`_balance`: a polite “keep out” sign) and expose safe, read-only views with `@property`.

### Special methods (a.k.a. “dunder” methods)
`__init__` (create) · `__str__` (friendly text for `print`) · `__repr__` (developer text) · `__len__` · `__eq__`. Python calls them for you.

### Inheritance preview
A **child class** can reuse and extend a **parent class**: `class Lecturer(Person)`. Different child classes can answer the *same method name* differently: that is **polymorphism**.
"""),
    demo('''# --- DEMO 1: a first class ----------------------------------------------------
class Student:                                         # class names use CapitalizedWords
    institution = "OOU"                                # CLASS attribute: shared by every Student

    def __init__(self, name, programme, scores=None):  # constructor: runs when Student(...) is called
        self.name = name                               # INSTANCE attribute: this object's own name
        self.programme = programme                     # instance attribute
        self.scores = scores if scores is not None else []   # new empty list per object (never use [] as a default!)

    def add_score(self, score):                        # a method: always has self first
        if not 0 <= score <= 100:                      # validation lives next to the data it protects
            raise ValueError("Score must be between 0 and 100")   # raise = stop with a clear error
        self.scores.append(score)                      # store the valid score

    def average(self):                                 # another method
        if not self.scores:                            # an empty list counts as False
            return 0.0                                 # avoid dividing by zero
        return sum(self.scores) / len(self.scores)     # total divided by count

amina = Student("Amina", "Data Science")               # create an OBJECT (this calls __init__)
tola = Student("Tola", "Computer Science")             # a second, independent object
amina.add_score(78)                                    # call a method with dot notation
amina.add_score(84)
tola.add_score(60)
print(amina.name, amina.average())                     # Amina 81.0
print(tola.name, tola.average())                       # Tola 60.0  <- separate state
print(amina.institution, tola.institution)            # OOU OOU    <- shared class attribute
print(amina.scores is tola.scores)                     # False: each object owns its own list'''),
    demo('''# --- DEMO 2: validation in action (catching the error) -------------------------------
try:                                                   # try the risky line
    amina.add_score(150)                               # invalid: the method will raise ValueError
except ValueError as error:                            # catch it and keep the program alive
    print("Rejected:", error)                          # Rejected: Score must be between 0 and 100
print(amina.scores)                                    # [78, 84]: the invalid score was NOT stored'''),
    demo('''# --- DEMO 3: encapsulation with a property ------------------------------------------------
class Wallet:
    def __init__(self, owner, balance=0):
        self.owner = owner                             # public attribute
        self._balance = balance                        # leading underscore: "internal, use methods instead"

    @property                                          # lets us READ w.balance like an attribute
    def balance(self):                                 # ... but there is no setter, so it is read-only
        return self._balance

    def deposit(self, amount):
        if amount <= 0:                                # rule: deposits must be positive
            raise ValueError("Deposit must be positive")
        self._balance += amount                        # only the class itself changes the balance

w = Wallet("Ada", 1000)                                # open with N1000
w.deposit(500)                                         # N1500
print(w.balance)                                       # 1500 (reading works)
try:
    w.balance = 99999                                  # trying to cheat by assigning directly
except AttributeError as error:                        # properties without setters refuse assignment
    print("Blocked:", error)                           # Blocked: ... has no setter'''),
    demo('''# --- DEMO 4: __str__ and __repr__ ------------------------------------------------------------
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):                                 # used by print() and str()
        return f"{self.title} by {self.author}"

    def __repr__(self):                                # used when inspecting the object / in lists
        return f"Book({self.title!r}, {self.author!r}, {self.pages})"   # !r shows the quotes

b = Book("Things Fall Apart", "Chinua Achebe", 209)
print(b)                                               # Things Fall Apart by Chinua Achebe
print([b])                                             # [Book('Things Fall Apart', 'Chinua Achebe', 209)]
print(repr(b))                                         # same developer text'''),
    demo('''# --- DEMO 5: inheritance and polymorphism (preview) -----------------------------------------
class Person:                                          # PARENT class
    def __init__(self, name):
        self.name = name
    def role(self):                                    # a method children may override
        return "member of OOU"

class Lecturer(Person):                                # CHILD class: (Person) means "inherits from Person"
    def role(self):                                    # OVERRIDE: same name, new behaviour
        return "teaches courses"

class Student2(Person):                                # another child
    def role(self):
        return "attends courses"

people = [Person("Ngozi"), Lecturer("Dr Bello"), Student2("Chika")]   # one list, three kinds of object
for p in people:                                       # POLYMORPHISM: same call, each object answers its own way
    print(p.name, "->", p.role())                      # Ngozi -> member of OOU, etc.
print(isinstance(people[1], Person))                   # True: a Lecturer IS a Person'''),
    activity(
        "Shared or separate?",
        "Predict the three printed lines. Which attribute is shared and which is not?",
        '''class Counter:
    total = 0                      # class attribute (shared)
    def __init__(self):
        self.mine = 0              # instance attribute (separate)
    def hit(self):
        self.mine += 1             # changes only THIS object
        Counter.total += 1         # changes the SHARED value

a = Counter()
b = Counter()
a.hit(); a.hit(); b.hit()
print(a.mine, b.mine, Counter.total)''',
        "`2 1 3`. `mine` belongs to each object (a hit twice, b once); `total` is stored once on the class and counts all three hits."),
    activity(
        "What does self refer to?",
        "Which object's name is printed on each line?",
        '''class Greeter:
    def __init__(self, name):
        self.name = name
    def hello(self):
        return f"Hello from {self.name}"

g1 = Greeter("Ada")
g2 = Greeter("Bola")
print(g1.hello())
print(g2.hello())
print(Greeter.hello(g2))      # calling through the class: we pass the object ourselves''',
        "`Hello from Ada`, `Hello from Bola`, `Hello from Bola`. `self` is simply \"the object in front of the dot\". Writing `g1.hello()` is shorthand for `Greeter.hello(g1)`."),
    md("""## 🛠️ Tasks
Write each class in the cell. A good habit: draw the **class diagram** first.

```
+----------------------+
|      Student         |
+----------------------+
| name, programme      |  <- attributes
| scores               |
+----------------------+
| add_score(score)     |  <- methods
| average()            |
+----------------------+
```
"""),
    task(1, "Extend the Student class",
         "Complete `Student` (given partly). Add: `highest()` (max score, or `None` if no scores), `has_passed()` (`True` if average ≥ 50) and `__str__` returning `\"<name> (<programme>): avg <average with 1 decimal>\"`.",
         '''class Student:
    def __init__(self, name, programme):
        self.name = name
        self.programme = programme
        self.scores = []

    def add_score(self, score):
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        self.scores.append(score)

    def average(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

    def highest(self):
        # TODO
        pass

    def has_passed(self):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass

s = Student("Amina", "Data Science")
s.add_score(70); s.add_score(90)
print(s.average())
# print(s)    # TODO: remove the leading # once __str__ is written''',
         '''class Student:
    def __init__(self, name, programme):
        self.name = name                                   # store the name
        self.programme = programme                         # store the programme
        self.scores = []                                   # a fresh list for this student

    def add_score(self, score):
        if not 0 <= score <= 100:                          # reject impossible scores
            raise ValueError("Score must be between 0 and 100")
        self.scores.append(score)

    def average(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0.0   # safe average

    def highest(self):
        if not self.scores:                                # nothing recorded yet
            return None
        return max(self.scores)                            # the largest score

    def has_passed(self):
        return self.average() >= 50                        # a Boolean expression is returned directly

    def __str__(self):
        return f"{self.name} ({self.programme}): avg {self.average():.1f}"   # 1 decimal place

s = Student("Amina", "Data Science")
s.add_score(70); s.add_score(90)
print(s)                                                   # Amina (Data Science): avg 80.0''',
         '''a = Student("Amina", "Data Science"); a.add_score(70); a.add_score(90)
b = Student("Tola", "Computer Science")
check(a.highest() == 90 and b.highest() is None, "highest()", "max(self.scores) or None when empty")
check(a.has_passed() is True and b.has_passed() is False, "has_passed()", "average() >= 50")
check(str(a) == "Amina (Data Science): avg 80.0", "__str__", "f'{name} ({programme}): avg {avg:.1f}'")
try:
    a.add_score(101); ok = False
except ValueError:
    ok = True
check(ok and a.scores == [70, 90], "validation still works", "raise ValueError for scores outside 0-100")'''),
    task(2, "InventoryItem",
         "Create `InventoryItem(code, description, quantity, unit_price)` with methods `total_value()` (quantity × unit price), `restock(n)` (add `n`; `n` must be positive else `ValueError`) and `sell(n)` (remove `n`; raise `ValueError` if `n` is not positive or exceeds stock).",
         '''class InventoryItem:
    def __init__(self, code, description, quantity, unit_price):
        # TODO: store the four attributes
        pass

    def total_value(self):
        # TODO
        pass

    def restock(self, n):
        # TODO
        pass

    def sell(self, n):
        # TODO
        pass

item = InventoryItem("A1", "Notebook", 10, 250)
print(item.total_value())''',
         '''class InventoryItem:
    def __init__(self, code, description, quantity, unit_price):
        self.code = code                                   # identifier
        self.description = description                     # what it is
        self.quantity = quantity                           # how many in stock
        self.unit_price = unit_price                       # price of one

    def total_value(self):
        return self.quantity * self.unit_price             # value of the whole stock line

    def restock(self, n):
        if n <= 0:                                         # nonsense amount
            raise ValueError("Restock amount must be positive")
        self.quantity += n

    def sell(self, n):
        if n <= 0:
            raise ValueError("Sale amount must be positive")
        if n > self.quantity:                              # cannot sell what we do not have
            raise ValueError("Not enough stock")
        self.quantity -= n

item = InventoryItem("A1", "Notebook", 10, 250)
print(item.total_value())                                  # 2500''',
         '''def raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False

it = InventoryItem("A1", "Notebook", 10, 250)
check(it.total_value() == 2500, "total_value", "quantity * unit_price")
it.restock(5); it.sell(3)
check(it.quantity == 12, "restock and sell change quantity", "restock adds, sell subtracts")
check(raises(it.sell, 100) and raises(it.sell, 0) and raises(it.restock, -1), "invalid amounts raise ValueError", "validate before changing quantity")
check(it.quantity == 12, "quantity unchanged after failed operations", "validate FIRST, then change state")'''),
    task(3, "BankAccount (fictional data only)",
         "Create `BankAccount(owner, balance=0)`. Keep the balance in `_balance` and expose it with a **read-only property** `balance`. `deposit(amount)` and `withdraw(amount)` raise `ValueError` for non-positive amounts; `withdraw` also raises when the amount exceeds the balance.",
         '''class BankAccount:
    def __init__(self, owner, balance=0):
        # TODO
        pass

    @property
    def balance(self):
        # TODO
        pass

    def deposit(self, amount):
        # TODO
        pass

    def withdraw(self, amount):
        # TODO
        pass

acct = BankAccount("Ada", 1000)
acct.deposit(500)
print(acct.balance)''',
         '''class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner                                 # account holder (fictional!)
        self._balance = balance                            # "private" by convention

    @property
    def balance(self):
        return self._balance                               # read-only view

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:                         # no overdraft
            raise ValueError("Insufficient funds")
        self._balance -= amount

acct = BankAccount("Ada", 1000)
acct.deposit(500)
print(acct.balance)                                        # 1500''',
         '''def raises(fn, *args, exc=ValueError):
    try:
        fn(*args)
    except exc:
        return True
    return False

acct = BankAccount("Ada", 1000)
acct.deposit(500); acct.withdraw(200)
check(acct.balance == 1300, "deposit and withdraw", "balance = 1000 + 500 - 200")
check(raises(acct.withdraw, 5000) and raises(acct.deposit, -5) and raises(acct.withdraw, 0), "invalid operations raise ValueError", "check amount > 0 and amount <= balance")
def try_set():
    acct.balance = 1
check(raises(try_set, exc=AttributeError), "balance is read-only", "define @property balance without a setter")
check(acct.balance == 1300, "balance unchanged after failures", "validate before modifying")'''),
    task(4, "Course enrolment",
         "Create `Course(code, title, capacity)` with `enrol(student_name)` (returns `True` when added; `False` if the student is already enrolled **or** the course is full), `enrolment_count()` and `is_full()`.",
         '''class Course:
    def __init__(self, code, title, capacity):
        # TODO
        pass

    def enrol(self, student_name):
        # TODO
        pass

    def enrolment_count(self):
        # TODO
        pass

    def is_full(self):
        # TODO
        pass

c = Course("CSC333", "Programming III Lab", 2)
print(c.enrol("Ada"))''',
         '''class Course:
    def __init__(self, code, title, capacity):
        self.code = code
        self.title = title
        self.capacity = capacity                           # maximum number of students
        self.students = []                                 # names of enrolled students

    def enrol(self, student_name):
        if self.is_full() or student_name in self.students:   # two reasons to refuse
            return False
        self.students.append(student_name)
        return True

    def enrolment_count(self):
        return len(self.students)

    def is_full(self):
        return len(self.students) >= self.capacity

c = Course("CSC333", "Programming III Lab", 2)
print(c.enrol("Ada"))                                      # True''',
         '''c = Course("CSC333", "Programming III Lab", 2)
check(c.enrol("Ada") is True and c.enrol("Ada") is False, "no duplicate enrolment", "refuse names already in the list")
check(c.enrol("Bola") is True and c.is_full() is True, "fills up", "is_full: count >= capacity")
check(c.enrol("Chi") is False and c.enrolment_count() == 2, "full course refuses", "check is_full() before adding")
d = Course("X", "Y", 5)
check(d.enrolment_count() == 0, "each course has its own list", "create self.students inside __init__")'''),
    task(5, "Extension: validated property with a setter",
         "Create `Product(name, quantity)` where `quantity` is a **property with a setter**. The setter raises `ValueError` if the value is negative; the constructor must use the same rule.",
         '''class Product:
    def __init__(self, name, quantity):
        self.name = name
        # TODO: use the property (self.quantity = quantity) so validation applies
        pass

    @property
    def quantity(self):
        # TODO
        pass

    @quantity.setter
    def quantity(self, value):
        # TODO
        pass

p = Product("Pen", 5)
print(p.quantity)''',
         '''class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity                           # goes through the SETTER, so it is validated too

    @property
    def quantity(self):
        return self._quantity                              # read the hidden value

    @quantity.setter
    def quantity(self, value):                             # runs on every `p.quantity = ...`
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value

p = Product("Pen", 5)
print(p.quantity)                                          # 5''',
         '''def raises(fn):
    try:
        fn()
    except ValueError:
        return True
    return False

p = Product("Pen", 5)
p.quantity = 9
check(p.quantity == 9, "setter stores valid values", "assign self._quantity = value")
def bad_set():
    p.quantity = -1
check(raises(bad_set), "setter rejects negatives", "raise ValueError when value < 0")
check(raises(lambda: Product("Bad", -3)), "constructor validates too", "use self.quantity = quantity in __init__")
check(p.quantity == 9, "value unchanged after rejection", "do not assign before validating")'''),
    quiz([
        ("What does `self` refer to?", "The particular object the method is being called on."),
        ("When is `__init__` executed?", "Automatically, every time a new object of the class is created."),
        ("What is the difference between a class attribute and an instance attribute?", "A class attribute is one value shared by all objects; an instance attribute (`self.x`) belongs to a single object."),
        ("Why should validation belong inside the class?", "Because the object then protects its own data: every way of changing it passes through the same rules."),
    ]),
    assignment(
        "**A. ICT service request.** Create `ServiceRequest(request_id, description)` with attributes `status` (starts as `\"open\"`), a method `close()` that sets the status to `\"closed\"`, and `__str__` returning `\"#<id> <description> [<status>]\"`.\n\n**B.** Make two objects, close only one, and store `(str(r1), str(r2))` in `two_states`.\n\n**C.** In `oop_terms` (a dictionary) define in your own words: `class`, `object`, `attribute`, `method`, `encapsulation`.",
        '''class ServiceRequest:
    # TODO
    pass

# TODO: create r1 and r2, close only r1
two_states = None

oop_terms = {
    "class": "",
    "object": "",
    "attribute": "",
    "method": "",
    "encapsulation": "",
}
print(two_states)''',
        '''class ServiceRequest:
    def __init__(self, request_id, description):
        self.request_id = request_id                       # unique number of the ticket
        self.description = description                     # what is wrong
        self.status = "open"                               # every new request starts open

    def close(self):
        self.status = "closed"                             # change this object's state

    def __str__(self):
        return f"#{self.request_id} {self.description} [{self.status}]"

r1 = ServiceRequest(1, "Projector not working")            # two separate objects
r2 = ServiceRequest(2, "Wi-Fi down in Lab 2")
r1.close()                                                 # only r1 changes
two_states = (str(r1), str(r2))

oop_terms = {
    "class": "A blueprint that describes the attributes and methods its objects will have.",
    "object": "One concrete instance created from a class, with its own data.",
    "attribute": "A variable stored inside an object that describes its state.",
    "method": "A function defined in a class that works on the object it is called on.",
    "encapsulation": "Keeping data and the rules that protect it together, so outside code cannot make the object invalid.",
}
print(two_states)                                          # ('#1 Projector not working [closed]', '#2 Wi-Fi down in Lab 2 [open]')''',
        '''check(two_states == ("#1 Projector not working [closed]", "#2 Wi-Fi down in Lab 2 [open]"), "two objects, two states", "close only r1; build the text with __str__")
check(all(isinstance(v, str) and len(v.split()) >= 4 for v in oop_terms.values()) and len(oop_terms) == 5, "all five terms defined", "write a short sentence for each term")'''),
]


def build():
    return build_week(7, "object_oriented_programming", "Object-Oriented Programming: Classes, Objects and Encapsulation",
                      OUTCOMES, ITEMS)
