"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 1.6: Класс & OOP (Object-Oriented Programming)     ║
║  Python 102 — JavaScript програмистад зориулсан                 ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - class тодорхойлох, __init__, self
   - Удамшил (Inheritance)
   - @property, @staticmethod, @classmethod
   - Dunder (magic) methods
   - Dataclass (Python 3.7+)
   - Abstract Base Class

💡 JS програмистад:
   JS class ↔ Python class — Маш адилхан!
   constructor() → __init__()
   this → self
   # private → _ private (convention)
"""


# ============================================================
# 📌 ХЭСЭГ 1: Класс тодорхойлох
# ============================================================
print("═" * 50)
print("📌 КЛАСС ТОДОРХОЙЛОХ")
print("═" * 50)

# --- JS хувилбар ---
# class Dog {
#     constructor(name, breed) {
#         this.name = name;
#         this.breed = breed;
#     }
#     bark() {
#         return `${this.name} says Woof!`;
#     }
# }

# --- Python хувилбар ---
class Dog:
    """Нохой класс"""

    # Class variable (бүх instance-д нийтлэг)
    species = "Canis familiaris"

    def __init__(self, name: str, breed: str, age: int = 0):
        """
        Constructor — JS-ийн constructor()-тай адилхан.

        Args:
            name: Нохойн нэр
            breed: Үүлдэр
            age: Нас
        """
        # Instance variables:
        self.name = name             # JS: this.name = name
        self.breed = breed           # JS: this.breed = breed
        self.age = age
        self._tricks = []            # _ = private (convention)

    def bark(self) -> str:
        """Хуцах"""
        return f"{self.name} says Woof! 🐕"

    def learn_trick(self, trick: str) -> None:
        """Шинэ зүйл сурах"""
        self._tricks.append(trick)

    def show_tricks(self) -> str:
        """Сурсан зүйлсээ харуулах"""
        if not self._tricks:
            return f"{self.name} юу ч мэдэхгүй 😅"
        return f"{self.name} мэднэ: {', '.join(self._tricks)}"

    def __str__(self) -> str:
        """Текст хэлбэр (print дуудахад)"""
        return f"🐕 {self.name} ({self.breed}, {self.age} нас)"

    def __repr__(self) -> str:
        """Debug хэлбэр"""
        return f"Dog(name='{self.name}', breed='{self.breed}', age={self.age})"


# Объект үүсгэх:
rex = Dog("Rex", "German Shepherd", 3)
buddy = Dog("Buddy", "Golden Retriever", 5)

print(rex.bark())                     # Rex says Woof! 🐕
print(buddy)                          # 🐕 Buddy (Golden Retriever, 5 нас)

rex.learn_trick("Суу")
rex.learn_trick("Гар өг")
print(rex.show_tricks())              # Rex мэднэ: Суу, Гар өг

# Class variable:
print(f"Зүйл: {Dog.species}")        # Canis familiaris
print(f"Зүйл: {rex.species}")        # Адилхан — instance-ээр ч хандаж болно


# 💡 JS vs Python ялгаа:
#    JS:  this.name         →  Py: self.name
#    JS:  автоматаар this    →  Py: self-ийг ЗААВАЛ бичнэ! (1-р параметр)
#    JS:  #private           →  Py: _private (convention), __name_mangling


# ============================================================
# 📌 ХЭСЭГ 2: Удамшил (Inheritance)
# ============================================================
print("\n" + "═" * 50)
print("📌 УДАМШИЛ (INHERITANCE)")
print("═" * 50)

# JS:  class Puppy extends Dog { ... }
# Py:  class Puppy(Dog):

class Animal:
    """Амьтны суурь класс"""

    def __init__(self, name: str, sound: str):
        self.name = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name}: {self.sound}!"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"


class Cat(Animal):
    """Муур класс — Animal-аас удамшина"""

    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name, "Мяу")  # JS: super(name, "Мяу")
        self.indoor = indoor

    def purr(self) -> str:
        return f"{self.name} хуурхинж байна... 😺"


class Parrot(Animal):
    """Тоть шувуу"""

    def __init__(self, name: str, vocabulary: list[str] = None):
        super().__init__(name, "Squawk")
        self.vocabulary = vocabulary or []

    def speak(self) -> str:
        """Method override — Эцэг классын аргыг дарж бичих"""
        if self.vocabulary:
            import random
            word = random.choice(self.vocabulary)
            return f"🦜 {self.name}: '{word}'"
        return super().speak()         # Эцэг классын аргыг дуудах


cat = Cat("Мишээл")
parrot = Parrot("Полли", ["Сайн уу!", "Крекер өгөөч!", "Python гоё!"])

print(cat.speak())                    # Мишээл: Мяу!
print(cat.purr())                     # Мишээл хуурхинж байна...
print(parrot.speak())                 # 🦜 Полли: 'Python гоё!'

# isinstance шалгалт:
print(f"\ncat нь Animal мөн үү? {isinstance(cat, Animal)}")     # True
print(f"cat нь Cat мөн үү? {isinstance(cat, Cat)}")             # True
print(f"cat нь Parrot мөн үү? {isinstance(cat, Parrot)}")       # False

# issubclass шалгалт:
print(f"Cat нь Animal-ийн дэд класс мөн үү? {issubclass(Cat, Animal)}")  # True


# --- Multiple Inheritance (Олон удамшил) ---
# JS-д олон удамшил байхгүй! Python-д бий.

class Flyable:
    """Нисэж чаддаг"""
    def fly(self) -> str:
        return f"{self.name} нисэж байна! 🦅"

class Swimmable:
    """Сэлж чаддаг"""
    def swim(self) -> str:
        return f"{self.name} сэлж байна! 🏊"

class Duck(Animal, Flyable, Swimmable):
    """Нугас — нисэж ч, сэлж ч чадна!"""
    def __init__(self, name: str):
        super().__init__(name, "Quack")

donald = Duck("Дональд")
print(f"\n{donald.speak()}")           # Дональд: Quack!
print(donald.fly())                    # Дональд нисэж байна! 🦅
print(donald.swim())                   # Дональд сэлж байна! 🏊

# MRO (Method Resolution Order) — Аргыг хайх дараалал:
print(f"\nDuck MRO: {[c.__name__ for c in Duck.__mro__]}")
# ['Duck', 'Animal', 'Flyable', 'Swimmable', 'object']


# ============================================================
# 📌 ХЭСЭГ 3: @property, @staticmethod, @classmethod
# ============================================================
print("\n" + "═" * 50)
print("📌 PROPERTY, STATIC, CLASSMETHOD")
print("═" * 50)

class Circle:
    """Тойрог класс — @property жишээ"""

    import math

    def __init__(self, radius: float):
        self._radius = radius          # _ = private

    # --- @property — Getter ---
    # JS:  get radius() { return this._radius; }
    @property
    def radius(self) -> float:
        """Радиус авах"""
        return self._radius

    # --- @property.setter — Setter ---
    # JS:  set radius(value) { this._radius = value; }
    @radius.setter
    def radius(self, value: float):
        """Радиус тохируулах (шалгалттай)"""
        if value < 0:
            raise ValueError("Радиус сөрөг байж болохгүй!")
        self._radius = value

    # --- Тооцоологдсон property ---
    @property
    def area(self) -> float:
        """Талбай"""
        return self.math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        """Тойргийн урт"""
        return 2 * self.math.pi * self._radius

    # --- @staticmethod — Обьекттой холбоогүй арга ---
    # JS:  static method() { ... }
    @staticmethod
    def from_diameter(diameter: float) -> "Circle":
        """Диаметрээс тойрог үүсгэх"""
        return Circle(diameter / 2)

    # --- @classmethod — Класстай холбоотой арга ---
    @classmethod
    def unit_circle(cls) -> "Circle":
        """Нэгж тойрог (r=1) үүсгэх"""
        return cls(1.0)               # cls = Circle класс өөрөө

    def __str__(self) -> str:
        return f"⭕ Circle(r={self._radius:.2f}, area={self.area:.2f})"


circle = Circle(5)
print(f"Радиус: {circle.radius}")             # 5
print(f"Талбай: {circle.area:.2f}")            # 78.54
print(f"Тойрог: {circle.circumference:.2f}")   # 31.42
print(circle)                                   # ⭕ Circle(r=5.00, area=78.54)

# Property setter:
circle.radius = 10                             # Setter дуудагдана
print(f"Шинэ радиус: {circle.radius}")

try:
    circle.radius = -5                         # ValueError!
except ValueError as e:
    print(f"⚠️ {e}")

# Static method:
c2 = Circle.from_diameter(20)                  # Диаметр = 20 → радиус = 10
print(f"from_diameter: {c2}")

# Class method:
unit = Circle.unit_circle()
print(f"unit_circle: {unit}")


# ============================================================
# 📌 ХЭСЭГ 4: Dunder (Magic) Methods
# ============================================================
print("\n" + "═" * 50)
print("📌 DUNDER (MAGIC) METHODS")
print("═" * 50)

"""
💡 Dunder = Double UNDERscore = __method__
   Python-ий "magic methods" — оператор, built-in функцтэй ажиллах.

   JS-д ийм зүйл байхгүй (Symbol ашиглана, жишээ: Symbol.iterator).
"""

class Vector:
    """2D вектор — Dunder methods жишээ"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # --- Текст хэлбэр ---
    def __str__(self) -> str:
        """print() дуудахад"""
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Debug, REPL-д"""
        return f"Vector({self.x}, {self.y})"

    # --- Арифметик оператор ---
    def __add__(self, other: "Vector") -> "Vector":
        """v1 + v2"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        """v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        """v * 3"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """3 * v (урвуу)"""
        return self.__mul__(scalar)

    # --- Харьцуулалт ---
    def __eq__(self, other: "Vector") -> bool:
        """v1 == v2"""
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: "Vector") -> bool:
        """v1 < v2 (уртаар)"""
        return self.magnitude < other.magnitude

    # --- Бусад ---
    def __abs__(self) -> float:
        """abs(v) — Уртыг тооцоолох"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __len__(self) -> int:
        """len(v) — Хэмжээс"""
        return 2

    def __bool__(self) -> bool:
        """bool(v) — Тэг вектор биш юу?"""
        return self.x != 0 or self.y != 0

    def __getitem__(self, index: int) -> float:
        """v[0], v[1] — Индексээр авах"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Index {index} out of range")

    def __iter__(self):
        """for x in v: — Давтагдаж болох"""
        yield self.x
        yield self.y

    @property
    def magnitude(self) -> float:
        """Векторын урт"""
        return abs(self)


# Хэрэглэх:
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")                     # (3, 4)
print(f"v2 = {v2}")                     # (1, 2)
print(f"v1 + v2 = {v1 + v2}")           # (4, 6)
print(f"v1 - v2 = {v1 - v2}")           # (2, 2)
print(f"v1 * 3 = {v1 * 3}")             # (9, 12)
print(f"3 * v1 = {3 * v1}")             # (9, 12)
print(f"|v1| = {abs(v1)}")              # 5.0
print(f"v1 == v2: {v1 == v2}")          # False
print(f"v1[0] = {v1[0]}")               # 3
print(f"v1 < v2: {v1 < v2}")            # False

# Unpack:
x, y = v1
print(f"Unpack: x={x}, y={y}")


# ============================================================
# 📌 ХЭСЭГ 5: Dataclass (Python 3.7+) 🌟
# ============================================================
print("\n" + "═" * 50)
print("📌 DATACLASS — Автомат класс")
print("═" * 50)

"""
💡 Dataclass = Автоматаар __init__, __repr__, __eq__ үүсгэнэ.
   Маш их boilerplate код хэмнэнэ!

   JS-тэй харьцуулалт:
   TS:  interface User { name: string; age: number; }
   Py:  @dataclass class User: name: str; age: int
"""

from dataclasses import dataclass, field
from typing import Optional

# --- Энгийн dataclass ---
@dataclass
class User:
    name: str
    email: str
    age: int
    active: bool = True              # Default утга

# Автоматаар __init__ үүссэн:
user = User("Болд", "bold@email.mn", 25)
print(user)                           # User(name='Болд', email='bold@email.mn', age=25, active=True)

# Автоматаар __eq__ үүссэн:
user2 = User("Болд", "bold@email.mn", 25)
print(f"user == user2: {user == user2}")  # True


# --- Илүү нарийн dataclass ---
@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    tags: list[str] = field(default_factory=list)  # ⚠️ Mutable default!
    _id: int = field(init=False, repr=False)       # __init__-д оруулахгүй

    def __post_init__(self):
        """__init__-ийн дараа дуудагдана"""
        import random
        self._id = random.randint(1000, 9999)

    @property
    def total_value(self) -> float:
        """Нийт үнэ"""
        return self.price * self.quantity


laptop = Product("MacBook", 2500.0, 5, ["tech", "apple"])
print(laptop)
print(f"Нийт үнэ: ${laptop.total_value:,.2f}")


# --- Frozen dataclass (өөрчлөгдөхгүй) ---
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
print(f"Point: {p}")

try:
    p.x = 10                          # ❌ FrozenInstanceError!
except Exception as e:
    print(f"⚠️ {type(e).__name__}: {e}")

# frozen=True бол dict key болж чадна (hashable):
points = {Point(0, 0): "origin", Point(1, 1): "diagonal"}
print(f"Origin: {points[Point(0, 0)]}")


# --- Dataclass-ийн ордероор эрэмбэлэх ---
@dataclass(order=True)
class Student:
    """Оноогоор эрэмбэлэгддэг оюутан"""
    # sort_index нь эрэмбэлэхэд ашиглагдана
    sort_index: float = field(init=False, repr=False)
    name: str = ""
    gpa: float = 0.0

    def __post_init__(self):
        self.sort_index = self.gpa     # GPA-аар эрэмбэлэх

students = [
    Student("Болд", 3.5),
    Student("Сараа", 3.9),
    Student("Дорж", 3.2),
]

for s in sorted(students, reverse=True):
    print(f"  {s.name}: GPA {s.gpa}")


# ============================================================
# 📌 ХЭСЭГ 6: Abstract Base Class (Хийсвэр класс)
# ============================================================
print("\n" + "═" * 50)
print("📌 ABSTRACT CLASS")
print("═" * 50)

"""
💡 TypeScript-ийн interface-тай адилхан!
   Хийсвэр класс = Хэрэгжүүлэх ёстой аргуудыг тодорхойлно.
"""

from abc import ABC, abstractmethod

class Shape(ABC):
    """Дүрс — Хийсвэр класс (interface шиг)"""

    @abstractmethod
    def area(self) -> float:
        """Талбай тооцоолох (ЗААВАЛ хэрэгжүүлэх!)"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Периметр тооцоолох"""
        pass

    def describe(self) -> str:
        """Тодорхойлолт (хэрэгжүүлсэн — дарж бичиж ч болно)"""
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


# ❌ Shape()-ийг шууд үүсгэж БОЛОХГҮЙ:
try:
    s = Shape()
except TypeError as e:
    print(f"⚠️ {e}")


import math

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class CircleShape(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


# Polymorphism (Олон хэлбэрт байдал):
shapes: list[Shape] = [
    Rectangle(5, 3),
    CircleShape(4),
    Rectangle(10, 2),
    CircleShape(7),
]

print("\n  Бүх дүрсүүд:")
for shape in shapes:
    print(f"    {shape.describe()}")

# Хамгийн их талбайтай дүрс:
largest = max(shapes, key=lambda s: s.area())
print(f"\n  Хамгийн том: {largest.describe()}")


# ============================================================
# 📌 ХЭСЭГ 7: Enum (Тоологч)
# ============================================================
print("\n" + "═" * 50)
print("📌 ENUM")
print("═" * 50)

from enum import Enum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"

# Хэрэглэх:
print(f"Color: {Color.RED}")              # Color.RED
print(f"Value: {Color.RED.value}")         # 1
print(f"Name: {Color.RED.name}")           # RED

status = Status.ACTIVE
print(f"Status: {status}")                 # Status.ACTIVE
print(f"Value: {status.value}")            # active

# Match-case-тай:
def handle_status(status: Status):
    match status:
        case Status.PENDING:
            print("  ⏳ Хүлээж байна...")
        case Status.ACTIVE:
            print("  ✅ Идэвхтэй!")
        case Status.DELETED:
            print("  🗑️ Устгагдсан!")
        case _:
            print("  ❓ Тодорхойгүй")

handle_status(Status.ACTIVE)


# ============================================================
# 📌 ХЭСЭГ 8: Бодит жишээ — Дансны систем
# ============================================================
print("\n" + "═" * 50)
print("📌 ЖИШЭЭ: Банкны данс")
print("═" * 50)

@dataclass
class Transaction:
    """Гүйлгээ"""
    type: str              # "deposit" эсвэл "withdrawal"
    amount: float
    description: str = ""

    def __str__(self) -> str:
        sign = "+" if self.type == "deposit" else "-"
        return f"  {sign}₮{self.amount:>12,.0f}  {self.description}"


class BankAccount:
    """Банкны данс"""

    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self._balance = balance
        self._transactions: list[Transaction] = []

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float, description: str = "Орлого") -> None:
        if amount <= 0:
            raise ValueError("Дүн 0-ээс их байх ёстой")
        self._balance += amount
        self._transactions.append(Transaction("deposit", amount, description))

    def withdraw(self, amount: float, description: str = "Зарлага") -> None:
        if amount <= 0:
            raise ValueError("Дүн 0-ээс их байх ёстой")
        if amount > self._balance:
            raise ValueError(f"Үлдэгдэл хүрэлцэхгүй! (₮{self._balance:,.0f})")
        self._balance -= amount
        self._transactions.append(Transaction("withdrawal", amount, description))

    def statement(self) -> None:
        """Дансны хуулга хэвлэх"""
        print(f"\n  {'=' * 45}")
        print(f"  📊 Дансны хуулга — {self.owner}")
        print(f"  {'=' * 45}")
        for t in self._transactions:
            print(t)
        print(f"  {'-' * 45}")
        print(f"  💰 Үлдэгдэл: ₮{self._balance:>12,.0f}")
        print(f"  {'=' * 45}")

    def __str__(self) -> str:
        return f"🏦 {self.owner}: ₮{self._balance:,.0f}"


# Ашиглах:
account = BankAccount("Болд", 1_000_000)
account.deposit(500_000, "Цалин")
account.deposit(200_000, "Бонус")
account.withdraw(150_000, "Түрээс")
account.withdraw(50_000, "Хоол")
account.statement()

# Алдаа шалгалт:
try:
    account.withdraw(10_000_000, "Tesla авах")
except ValueError as e:
    print(f"\n  ⚠️ {e}")


# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 1.6.1:
   TodoList класс бичих:
   - add(task: str) — Даалгавар нэмэх
   - complete(index: int) — Дуусгах
   - remove(index: int) — Арилгах
   - show() — Жагсаалт хэвлэх
   - __len__() — Тоог авах
   - __str__() — Хэвлэх

✏️ Дасгал 1.6.2:
   Dataclass ашиглан Library системийг бүтээх:
   - Book(title, author, year, isbn)
   - Library — номнуудыг хадгалах
   - Хайх, нэмэх, арилгах, жагсаах

✏️ Дасгал 1.6.3:
   Shape хийсвэр классыг өргөтгөх:
   - Triangle(a, b, c) нэмэх
   - Hexagon(side) нэмэх
   - Бүх дүрсийг талбайгаар эрэмбэлэх

✏️ Дасгал 1.6.4:
   Ажилчдын цалингийн систем:
   - Employee (суурь класс)
   - FullTime(Employee) — Сарын цалин
   - PartTime(Employee) — Цагийн цалин
   - Manager(FullTime) — Цалин + бонус
   - Нийт цалингийн зардлыг тооцоол
"""

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("✅ Хичээл 1.6 амжилттай дууслаа!")
    print("🎉 1-Р ҮЕ ШАТ ДУУСЛАА!")
    print("👉 Дараагийн үе шат: 02_intermediate/")
    print("=" * 50)
