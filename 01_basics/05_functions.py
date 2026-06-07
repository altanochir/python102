"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 1.5: Функц (Functions)                              ║
║  Python 102 — JavaScript програмистад зориулсан                 ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - def — функц тодорхойлох
   - *args, **kwargs — уян параметрүүд
   - Lambda — Нэргүй функц
   - Decorator — Python-ий хамгийн хүчтэй ойлголтуудын нэг!
   - Closure, Scope
   - Type hints — Функцийн гарын үсэг

💡 JS програмистад:
   function → def
   arrow function (=>) → lambda
   ...args → *args, **kwargs
"""


# ============================================================
# 📌 ХЭСЭГ 1: Функц тодорхойлох (def)
# ============================================================
print("═" * 50)
print("📌 ФУНКЦ ТОДОРХОЙЛОХ")
print("═" * 50)

# JS:  function greet(name) { return `Hello, ${name}!`; }
# Py:
def greet(name):
    """Мэндчилгээ хэвлэх функц."""
    return f"Hello, {name}!"

print(greet("Python"))       # Hello, Python!

# 💡 Ялгаа:
#    JS:  function name() {}   эсвэл  const name = () => {}
#    Py:  def name():
#         Python-д зөвхөн def ашиглана (function гэдэг түлхүүр үг байхгүй)


# --- Олон утга буцаах ---
# JS:  return { min: 1, max: 10 }  эсвэл  return [1, 10]
# Py:  return 1, 10  ← автоматаар tuple болно!

def min_max(numbers):
    """Хамгийн бага, их утгыг буцаах"""
    return min(numbers), max(numbers)

lo, hi = min_max([5, 2, 8, 1, 9])    # Tuple unpacking
print(f"Min: {lo}, Max: {hi}")


# --- Docstring (баримтжуулалт) ---
# JS:  /** JSDoc коммент */
# Py:  """Docstring"""   ← Функцийн эхний мөрөнд бичнэ

def calculate_bmi(weight_kg, height_m):
    """
    Биеийн жингийн индексийг (BMI) тооцоолох.

    Args:
        weight_kg: Жин (кг)
        height_m: Өндөр (метр)

    Returns:
        BMI утга (float)

    Example:
        >>> calculate_bmi(70, 1.75)
        22.857142857142858
    """
    return weight_kg / (height_m ** 2)

bmi = calculate_bmi(70, 1.75)
print(f"BMI: {bmi:.1f}")

# Docstring-ийг уншиж болно:
print(calculate_bmi.__doc__)          # JS-д ийм зүйл байхгүй
help(calculate_bmi)                   # Бүтэн тусламж


# ============================================================
# 📌 ХЭСЭГ 2: Параметрүүд (Parameters)
# ============================================================
print("\n" + "═" * 50)
print("📌 ПАРАМЕТРҮҮД")
print("═" * 50)

# --- Default параметр ---
# JS:  function greet(name = "World") { ... }
# Py:
def greet_v2(name="World", greeting="Сайн уу"):
    return f"{greeting}, {name}!"

print(greet_v2())                         # Сайн уу, World!
print(greet_v2("Болд"))                   # Сайн уу, Болд!
print(greet_v2("Болд", "Өглөөний мэнд"))  # Өглөөний мэнд, Болд!


# --- Keyword arguments (нэрээр дамжуулах) ---
# JS-д ийм зүйл Object-оор хийдэг: greet({ name: "Болд", greeting: "Hi" })
# Python-д шууд keyword ашиглана:

print(greet_v2(greeting="Hello", name="Python"))  # Дарааллыг сольж болно!

# 💡 Энэ нь Python-ий маш том давуу тал!
#    JS-д { name, greeting } гэж Object дамжуулах хэрэгтэй.


# --- Positional-only ба Keyword-only параметрүүд ---
# Python 3.8+ онцлог

def example(pos_only, /, normal, *, kw_only):
    """
    pos_only:  Зөвхөн байршлаар дамжуулна (/ -ийн өмнө)
    normal:    Аль ч хэлбэрээр
    kw_only:   Зөвхөн нэрээр дамжуулна (* -ийн дараа)
    """
    print(f"  {pos_only}, {normal}, {kw_only}")

example(1, 2, kw_only=3)              # ✅ Зөв
example(1, normal=2, kw_only=3)       # ✅ Зөв
# example(pos_only=1, normal=2, kw_only=3)  # ❌ TypeError!


# ⚠️ DEFAULT ПАРАМЕТРИЙН АЛДАА (Маш чухал!)
# Хэзээ ч mutable default утга ашиглаж БОЛОХГҮЙ!

# ❌ БУРУУ:
def bad_append(item, items=[]):
    items.append(item)
    return items

print(bad_append(1))           # [1] — зөв
print(bad_append(2))           # [1, 2] — 😱 Буруу! [2] байх ёстой!
print(bad_append(3))           # [1, 2, 3] — 😱😱

# ✅ ЗӨВ:
def good_append(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(good_append(1))           # [1] ✅
print(good_append(2))           # [2] ✅

# 💡 JS-д ийм асуудал байхгүй (default утга давталт бүрт шинээр үүснэ).
#    Python-д default утга ганцхан удаа (функц тодорхойлох үед) үүснэ!


# ============================================================
# 📌 ХЭСЭГ 3: *args, **kwargs
# ============================================================
print("\n" + "═" * 50)
print("📌 *ARGS, **KWARGS")
print("═" * 50)

"""
💡 JS:  function func(...args) {}     ← rest параметр
   Py:  def func(*args, **kwargs):    ← 2 төрөл!

   *args   = Нэрлээгүй аргументууд → tuple болно
   **kwargs = Нэрлэсэн аргументууд → dict болно
"""

# --- *args (tuple) ---
def sum_all(*numbers):
    """Бүх тоонуудын нийлбэр"""
    print(f"  args = {numbers}")       # tuple
    print(f"  type = {type(numbers)}")
    return sum(numbers)

print(f"  Нийлбэр: {sum_all(1, 2, 3, 4, 5)}")   # 15


# --- **kwargs (dict) ---
def print_info(**kwargs):
    """Нэрлэсэн бүх аргументуудыг хэвлэх"""
    print(f"  kwargs = {kwargs}")       # dict
    for key, value in kwargs.items():
        print(f"    {key}: {value}")

print_info(name="Болд", age=25, city="УБ")


# --- *args + **kwargs хослуулах ---
def super_func(*args, **kwargs):
    print(f"  args: {args}")
    print(f"  kwargs: {kwargs}")

super_func(1, 2, 3, name="Болд", age=25)
# args: (1, 2, 3)
# kwargs: {'name': 'Болд', 'age': 25}


# --- Unpacking (задлах) ---
# JS:  Math.max(...numbers)
# Py:
numbers = [1, 2, 3, 4, 5]
print(f"  Max: {max(*numbers)}")       # * ашиглан задлах

# Dict unpacking:
config = {"host": "localhost", "port": 8080}

def connect(host, port):
    print(f"  Connecting to {host}:{port}")

connect(**config)                      # ** ашиглан dict-ийг задлах
# JS:  connect({ ...config })


# ============================================================
# 📌 ХЭСЭГ 4: Lambda (Нэргүй функц)
# ============================================================
print("\n" + "═" * 50)
print("📌 LAMBDA — Нэргүй функц")
print("═" * 50)

"""
💡 JS:  (a, b) => a + b        ← Arrow function
   Py:  lambda a, b: a + b     ← Lambda

   ⚠️ Lambda нь зөвхөн НЭГ илэрхийлэл л агуулж чадна!
      Олон мөрт логик бичиж болохгүй (def ашиглана).
"""

# --- Энгийн lambda ---
# JS:  const add = (a, b) => a + b
# Py:
add = lambda a, b: a + b
print(f"  3 + 5 = {add(3, 5)}")

# --- Ихэвчлэн sorted(), map(), filter()-д ашиглана ---

# Нэрээр эрэмбэлэх:
students = [
    {"name": "Болд", "age": 25},
    {"name": "Сараа", "age": 22},
    {"name": "Дорж", "age": 30},
]

# JS:  students.sort((a, b) => a.age - b.age)
# Py:
by_age = sorted(students, key=lambda s: s["age"])
print("  Насаар эрэмбэлсэн:")
for s in by_age:
    print(f"    {s['name']}: {s['age']}")

# Нэрээр (урвуу):
by_name_desc = sorted(students, key=lambda s: s["name"], reverse=True)
print("  Нэрээр (урвуу):")
for s in by_name_desc:
    print(f"    {s['name']}")

# --- map() + lambda ---
# JS:  [1,2,3].map(x => x ** 2)
squares = list(map(lambda x: x ** 2, [1, 2, 3, 4, 5]))
print(f"  Квадратууд: {squares}")

# 💡 Гэхдээ list comprehension илүү Pythonic:
squares_v2 = [x ** 2 for x in [1, 2, 3, 4, 5]]
print(f"  Квадратууд (v2): {squares_v2}")

# --- filter() + lambda ---
# JS:  [1,2,3,4,5].filter(x => x % 2 === 0)
evens = list(filter(lambda x: x % 2 == 0, range(1, 11)))
print(f"  Тэгш тоо: {evens}")


# ============================================================
# 📌 ХЭСЭГ 5: Scope (Хүрээ) & Closure
# ============================================================
print("\n" + "═" * 50)
print("📌 SCOPE & CLOSURE")
print("═" * 50)

"""
💡 Python-ий scope дүрэм: LEGB
   L - Local     (Функцийн дотор)
   E - Enclosing (Дотоод функцийн гаднах функц)
   G - Global    (Модулийн түвшин)
   B - Built-in  (Python-ий суурь функцүүд)

JS-тэй харьцуулалт:
   JS:  block scope (let/const), function scope (var)
   Py:  function scope ONLY (блок scope байхгүй!)
"""

# ⚠️ Python-д блок scope БАЙХГҮЙ!
if True:
    block_var = "Би блокийн дотор үүссэн"

print(block_var)             # ✅ Ажиллана! (JS-д let ашигласан бол ReferenceError!)

for i in range(5):
    loop_var = i

print(f"loop_var = {loop_var}")  # 4 — for давталтын хувьсагч хүртэл хадгалагдана!


# --- Global хувьсагч ---
counter = 0

def increment():
    global counter              # global түлхүүр үг шаардлагатай!
    counter += 1

# ⚠️ global бичихгүй бол UnboundLocalError гарна!
increment()
increment()
print(f"  Counter: {counter}")   # 2


# --- Closure ---
# JS:  function outer() { let x = 10; return () => x; }
# Py:
def make_multiplier(factor):
    """Үржүүлэгч функц үүсгэх"""
    def multiply(number):
        return number * factor   # factor нь enclosing scope-оос
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(f"  double(5) = {double(5)}")   # 10
print(f"  triple(5) = {triple(5)}")   # 15

# --- nonlocal ---
def make_counter():
    count = 0

    def increment():
        nonlocal count           # Enclosing scope-ын хувьсагчийг өөрчлөх
        count += 1
        return count

    return increment

counter = make_counter()
print(f"  1: {counter()}")      # 1
print(f"  2: {counter()}")      # 2
print(f"  3: {counter()}")      # 3


# ============================================================
# 📌 ХЭСЭГ 6: Decorator — Python-ий "Супер хүч"! 🦸
# ============================================================
print("\n" + "═" * 50)
print("📌 DECORATOR — Функцийг өргөтгөх")
print("═" * 50)

"""
💡 Decorator = Функцийг "ороож", нэмэлт функциональ нэмнэ.

JS-д ийм pattern бий:
   const withLogging = (fn) => (...args) => {
       console.log("calling", fn.name);
       return fn(...args);
   }

Python-д @ синтакс ашиглана:
   @decorator
   def my_function():
       ...

Хаана ашиглагддаг вэ?
   - Flask/FastAPI: @app.route("/api/users")
   - Caching: @lru_cache
   - Logging, timing, authentication, validation
   - Property: @property
"""

import time
import functools

# --- Цаг хэмжигч decorator ---
def timer(func):
    """Функцийн ажиллах хугацааг хэмждэг decorator"""
    @functools.wraps(func)       # Эх функцийн нэр, docstring-ийг хадгалах
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"  ⏱️ {func.__name__}() — {end - start:.4f} секунд")
        return result
    return wrapper

@timer
def slow_function():
    """Удаан ажиллах функц"""
    total = sum(range(1_000_000))
    return total

result = slow_function()             # ⏱️ slow_function() — 0.0312 секунд
print(f"  Үр дүн: {result}")


# --- Логгер decorator ---
def logger(func):
    """Функцийн дуудалтыг бүртгэх"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(map(repr, args))
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"  📝 {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"  📤 {func.__name__} → {result!r}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 5)
# 📝 add(3, 5)
# 📤 add → 8


# --- Параметртэй decorator ---
def repeat(times):
    """Функцийг n удаа давтах decorator"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello(name):
    print(f"  👋 Hello, {name}!")

say_hello("Python")  # 3 удаа хэвлэнэ


# --- Олон decorator давхарлах ---
@timer
@logger
def multiply(a, b):
    return a * b

multiply(6, 7)
# 📝 multiply(6, 7)
# 📤 multiply → 42
# ⏱️ multiply() — 0.0001 секунд


# ============================================================
# 📌 ХЭСЭГ 7: First-class Functions
# ============================================================
print("\n" + "═" * 50)
print("📌 FIRST-CLASS FUNCTIONS")
print("═" * 50)

"""
💡 JS шиг Python-д ч функц нь "first-class citizen".
   Хувьсагчид оноож, параметр болгон дамжуулж, буцааж болно.
"""

# Функцийг хувьсагчид оноох:
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

# Функцийг сонгох:
def speak(text, style):
    return style(text)

print(speak("Hello Python", shout))    # HELLO PYTHON
print(speak("Hello Python", whisper))  # hello python

# Функцийг жагсаалтад хадгалах:
operations = [
    ("Том үсэг", str.upper),
    ("Жижиг үсэг", str.lower),
    ("Толгой", str.title),
    ("Урвуу", lambda s: s[::-1]),
]

text = "hello world"
for name, func in operations:
    print(f"  {name}: {func(text)}")


# ============================================================
# 📌 ХЭСЭГ 8: Type Hints — Функцийн гарын үсэг
# ============================================================
print("\n" + "═" * 50)
print("📌 TYPE HINTS")
print("═" * 50)

"""
💡 TypeScript-тай маш адилхан!
   TS:  function add(a: number, b: number): number
   Py:  def add(a: int, b: int) -> int:

   ⚠️ Type hints нь зөвхөн тайлбар! Python шалгахгүй (runtime-д).
   Гэхдээ IDE, mypy, pyright зэрэг tools шалгаж чадна.
"""

from typing import Optional, Union, Callable

# Энгийн type hints:
def add_typed(a: int, b: int) -> int:
    return a + b

# Optional (None байж болно):
def find_user(user_id: int) -> Optional[dict]:
    """Хэрэглэгч олох. Олдохгүй бол None."""
    users = {1: {"name": "Болд"}, 2: {"name": "Дорж"}}
    return users.get(user_id)

# Union (олон төрөл):
def process(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ синтакс:
# def process(value: int | str) -> str:

# Callback функц (Callable):
def apply_operation(
    x: int,
    y: int,
    operation: Callable[[int, int], int]     # (int, int) -> int
) -> int:
    return operation(x, y)

result = apply_operation(10, 3, lambda a, b: a + b)
print(f"  Result: {result}")

# List, Dict type hints:
def get_names(users: list[dict[str, str]]) -> list[str]:
    return [u["name"] for u in users]

# Complex return type:
def parse_config(path: str) -> dict[str, Union[str, int, bool]]:
    return {"debug": True, "port": 8080, "host": "localhost"}


# ============================================================
# 📌 ХЭСЭГ 9: Хэрэгтэй built-in функцүүд
# ============================================================
print("\n--- Хэрэгтэй built-in функцүүд ---")

# sorted() — Эрэмбэлэх (key параметртай)
words = ["banana", "apple", "cherry", "date"]
print(f"  Үсгийн: {sorted(words)}")
print(f"  Уртаар: {sorted(words, key=len)}")
print(f"  Сүүлийн: {sorted(words, key=lambda w: w[-1])}")

# functools.reduce() — Нэгтгэх
# JS:  [1,2,3,4,5].reduce((acc, x) => acc + x, 0)
from functools import reduce
total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5], 0)
print(f"  reduce: {total}")

# functools.lru_cache — Автоматаар кэшлэх (мемоизац)
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Фибоначчийн n-р гишүүн (кэштэй)"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"  fib(10) = {fibonacci(10)}")     # 55
print(f"  fib(30) = {fibonacci(30)}")     # 832040
print(f"  fib(50) = {fibonacci(50)}")     # 12586269025 — Маш хурдан!
print(f"  Cache info: {fibonacci.cache_info()}")


# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 1.5.1:
   Decorator бичих — @retry(max_attempts=3)
   Функц амжилтгүй болвол (exception) дахин оролдох.

✏️ Дасгал 1.5.2:
   Closure ашиглан counter үүсгэх:
   counter = make_counter(start=10, step=5)
   counter()  → 10
   counter()  → 15
   counter()  → 20

✏️ Дасгал 1.5.3:
   Type hints-тай функцүүд бичих:
   - calculate_area(shape: str, **dimensions: float) -> float
   - "circle" → π * r²
   - "rectangle" → width * height
   - "triangle" → 0.5 * base * height

✏️ Дасгал 1.5.4:
   @timer decorator ашиглан:
   - List comprehension vs map() vs for loop
   - 1,000,000 элемент дээр хурдыг харьцуулах
"""

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("✅ Хичээл 1.5 амжилттай дууслаа!")
    print("👉 Дараагийн хичээл: 06_oop.py")
    print("=" * 50)
