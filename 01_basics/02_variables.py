"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 1.2: Хувьсагч & Өгөгдлийн Төрлүүд                  ║
║  Python 102 — JavaScript програмистад зориулсан                 ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - Python-ий өгөгдлийн төрлүүдийг бүрэн ойлгох
   - Type hints (TypeScript шиг) ашиглах
   - JS-ээс ялгаатай зүйлсийг тодруулах
"""


# ============================================================
# 📌 ХЭСЭГ 1: Тоон төрлүүд (Numbers)
# ============================================================

# --- int (бүхэл тоо) ---
# JS-д Number нэг л төрөл байдаг.
# Python-д int, float, complex гэж ялгаатай.

age = 25                    # int
big_number = 1_000_000      # Уншихад хялбар бичих арга (JS-д ч бас ажиллана)
binary = 0b1010             # 2-тын тоо = 10
octal = 0o17                # 8-тын тоо = 15
hexadecimal = 0xFF          # 16-тын тоо = 255

# 💡 Python-ий int хязгааргүй том байж болно! (JS-ийн BigInt шиг)
huge = 10 ** 100            # Googol — 1-ийн ард 100 тэг
print(f"Googol = {huge}")   # JS-д энэ нь Infinity болох байсан!


# --- float (бутархай тоо) ---
pi = 3.14159
temperature = -40.0
scientific = 1.5e10         # 1.5 × 10^10 = 15,000,000,000

# ⚠️ Float-ийн нарийвчлал (JS-тэй адил асуудалтай!)
print(0.1 + 0.2)            # 0.30000000000000004 — JS-тэй яг адилхан!

# Шийдэл: decimal модуль ашиглах (мөнгө тооцоолоход хэрэгтэй)
from decimal import Decimal
price = Decimal("0.1") + Decimal("0.2")
print(f"Нарийвчлалтай: {price}")  # 0.3 ✅

# Тоон дугуйлах:
print(round(3.14159, 2))    # 3.14


# --- complex (комплекс тоо) ---
# JS-д байхгүй, Python-д бий (AI/ML математикд хэрэглэгдэнэ)
z = 3 + 4j
print(f"Бодит хэсэг: {z.real}, Хуурмаг хэсэг: {z.imag}")


# --- Арифметик үйлдлүүд ---
print("--- Арифметик үйлдлүүд ---")

a, b = 17, 5               # Олон хувьсагч нэг мөрөнд (JS-д ч ажиллана)

print(f"{a} + {b} = {a + b}")       # Нэмэх: 22
print(f"{a} - {b} = {a - b}")       # Хасах: 12
print(f"{a} * {b} = {a * b}")       # Үржих: 85
print(f"{a} / {b} = {a / b}")       # Хуваах: 3.4  (ҮРГЭЛЖ float буцаана!)
print(f"{a} // {b} = {a // b}")     # Бүхэл хуваах: 3  ← JS-д Math.floor(a/b)
print(f"{a} % {b} = {a % b}")       # Үлдэгдэл: 2
print(f"{a} ** {b} = {a ** b}")     # Зэрэг: 1419857  ← JS-д Math.pow(a,b) эсвэл a**b

# 💡 JS vs Python ялгаа:
#    JS:  17 / 5 = 3.4     Python: 17 / 5 = 3.4     (адилхан)
#    JS:  бүхэл хуваалт байхгүй  Python: 17 // 5 = 3
#    JS:  Math.pow(2, 10)  Python: 2 ** 10


# ============================================================
# 📌 ХЭСЭГ 2: Текст (Strings)
# ============================================================
print("\n--- Текст (Strings) ---")

# Текст зарлах — Ганц '', давхар "" хоёулаа ажиллана
name = 'Python'
greeting = "Сайн байна уу"

# 💡 JS-тэй адилхан: ганц ба давхар хашилт ялгаагүй

# --- f-string (Формат текст) ---
# JS:  `Hello ${name}`        (backtick)
# Py:  f"Hello {name}"        (f prefix)

age = 30
message = f"{name} хэл {age} жилийн настай"
print(message)

# f-string дотор илэрхийлэл бичиж болно:
print(f"2 + 3 = {2 + 3}")
print(f"Том үсгээр: {name.upper()}")
print(f"Pi = {3.14159:.2f}")         # 2 оронтой бутархай: 3.14
print(f"{'Болд':>20}")               # Баруун тийш 20 тэмдэгтэд зэрэгцүүлэх
print(f"{'Болд':<20}|")              # Зүүн тийш
print(f"{'Болд':^20}|")              # Голд
print(f"{1000000:,}")                # 1,000,000 — мянгатын тусгаарлагч

# --- Хуучин формат аргууд ---
# .format() арга
print("Сайн уу, {}! Та {} настай.".format(name, age))
# % оператор (хуучин арга, мэдэхэд болно)
print("Сайн уу, %s! Та %d настай." % (name, age))


# --- Олон мөрт текст ---
# JS:  `олон мөрт
#       текст`               (backtick)
# Py:  """олон мөрт
#       текст"""             (triple quotes)

poem = """
Хаврын салхи
    Нүдийг нэмэргэн
        Нам гүм болно
"""
print(poem)


# --- Текстийн аргууд (String methods) ---
text = "  Hello, Python World!  "

print(text.strip())          # Хоёр талын зайг арилгах  ← JS: trim()
print(text.lstrip())         # Зүүн талын зайг арилгах  ← JS: trimStart()
print(text.rstrip())         # Баруун талын зайг арилгах ← JS: trimEnd()
print(text.lower())          # бүгд жижгээр            ← JS: toLowerCase()
print(text.upper())          # БҮГД ТОМООР             ← JS: toUpperCase()
print(text.title())          # Үг Бүрийн Эхний Үсэг Том
print(text.replace("Python", "JS"))  # Солих          ← JS: replace()
print(text.split(","))       # Хуваах                  ← JS: split()
print(text.find("Python"))   # Индекс олох (7)         ← JS: indexOf()
print(text.count("l"))       # Тоолох (2)
print(text.startswith("  H"))# True                    ← JS: startsWith()
print(text.endswith("!  "))  # True                    ← JS: endsWith()

# Текст нэгтгэх (join)
# JS:  ["a", "b", "c"].join("-")
# Py:  "-".join(["a", "b", "c"])    ← Анхаар! Дуудагдах дараалал өөр!
words = ["Python", "бол", "гоё"]
print(" ".join(words))       # "Python бол гоё"

# Текст давтах
print("Ha" * 3)              # "HaHaHa"    ← JS-д ийм зүйл байхгүй ("Ha".repeat(3) бий)

# Текст индексээр авах (slicing)
s = "Hello Python"
print(s[0])                  # "H"         ← JS: s[0]
print(s[-1])                 # "n"         ← JS: s[s.length-1]  (Python-д -1 ажиллана!)
print(s[0:5])                # "Hello"     ← JS: s.slice(0, 5)
print(s[6:])                 # "Python"    ← JS: s.slice(6)
print(s[::-1])               # "nohtyP olleH"  ← Урвуу! JS-д ийм шууд арга байхгүй


# --- Raw string ---
# Тусгай тэмдэгтүүдийг тоохгүй (regex бичихэд хэрэгтэй)
path = r"C:\Users\new\test"  # \n шинэ мөр гэж тайлбарлахгүй
print(path)                  # C:\Users\new\test


# ============================================================
# 📌 ХЭСЭГ 3: Boolean (Үнэн/Худал)
# ============================================================
print("\n--- Boolean ---")

# ⚠️ ЧУХАЛ: Python-д True/False ТОМ ҮСГЭЭР бичнэ!
# JS:  true / false (жижгээр)
# Py:  True / False (Эхний үсэг том!)

is_active = True
is_deleted = False

# Logical operators:
# JS:  && || !
# Py:  and or not      ← Англи үгээр!

print(True and False)        # False    ← JS: true && false
print(True or False)         # True     ← JS: true || false
print(not True)              # False    ← JS: !true

# Харьцуулалт:
print(5 > 3)                 # True
print(5 == 5)                # True     ← JS: === ашиглах хэрэгтэй, Python-д == яг адилхан
print(5 != 3)                # True
print(1 < 2 < 3)             # True     ← Chained comparison! JS-д ажиллахгүй!
print(1 < 2 and 2 < 3)       # Дээрхтэй адилхан утгатай

# 💡 Python-д === (strict equality) гэж байхгүй.
#    == нь аль хэдийн strict (төрөл шалгадаг):
print(1 == "1")              # False    ← JS-д 1 == "1" нь true! Python-д False.
print(1 == 1.0)              # True     ← Тоонууд хоорондоо харьцуулагдана


# --- Truthy / Falsy утгууд ---
# JS-тэй бараг адилхан ойлголт

# Python дээр Falsy утгууд:
#   False, None, 0, 0.0, "", [], {}, set(), (), frozenset()

# Python дээр Truthy: Дээрхээс бусад бүх зүйл

# ⚠️ JS-тэй ялгаа:
#   JS:  "" → falsy,  [] → truthy,  {} → truthy
#   Py:  "" → falsy,  [] → falsy!,  {} → falsy!  ← Хоосон list, dict falsy!

print(bool(""))              # False
print(bool("hello"))         # True
print(bool(0))               # False
print(bool(42))              # True
print(bool([]))              # False    ← JS-д [] нь truthy!
print(bool([1, 2]))          # True
print(bool({}))              # False    ← JS-д {} нь truthy!
print(bool(None))            # False    ← JS-д null нь falsy


# ============================================================
# 📌 ХЭСЭГ 4: None (Хоосон утга)
# ============================================================
print("\n--- None ---")

# JS:  null, undefined (2 өөр зүйл!)
# Py:  None (зөвхөн 1)

result = None

# None шалгах: is оператор ашиглана (== биш!)
if result is None:
    print("Утга байхгүй")

if result is not None:
    print("Утга бий")

# 💡 'is' vs '==' ялгаа:
#    is  → нэг объект мөн эсэхийг шалгана (identity)
#    ==  → утга нь тэнцүү эсэхийг шалгана (equality)
#    None шалгахдаа ҮРГЭЛЖ 'is' ашиглана!

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)                # True  — утга нь адилхан
print(a is b)                # False — өөр өөр объект
print(a is c)                # True  — нэг объект


# ============================================================
# 📌 ХЭСЭГ 5: Type Hints (TypeScript шиг)
# ============================================================
print("\n--- Type Hints ---")

"""
💡 JS/TypeScript-тэй харьцуулалт:
   TS:  let name: string = "Python"
   Py:  name: str = "Python"

   TS:  function add(a: number, b: number): number
   Py:  def add(a: int, b: int) -> int:

Type hints нь Python-д ЗААВАЛ биш (optional)!
Гэхдээ ашиглахыг зөвлөе — код илүү ойлгомжтой болно.
IDE-ийн автоматаар нөхөлт (autocomplete) ч сайжирна.
"""

# Энгийн type hints:
name: str = "Python"
age: int = 30
height: float = 1.75
is_student: bool = False
nothing: None = None

# Цогц type hints (typing модулиас):
from typing import Optional, Union

# Optional = утга байж болно эсвэл None байж болно
middle_name: Optional[str] = None      # str | None

# Union = олон төрлийн аль нэг
value: Union[int, str] = 42            # int эсвэл str

# Python 3.10+ дээр илүү энгийн бичиглэл:
# middle_name: str | None = None
# value: int | str = 42


# --- type() ба isinstance() ---
print(type(42))              # <class 'int'>
print(type("hello"))         # <class 'str'>
print(type(True))            # <class 'bool'>
print(type(None))            # <class 'NoneType'>
print(type([1, 2]))          # <class 'list'>

# isinstance() — илүү уян шалгалт (удамшилтай ажиллана)
print(isinstance(42, int))           # True
print(isinstance(42, (int, float)))  # True — аль нэг нь
print(isinstance(True, int))         # True! ← bool нь int-ийн дэд класс!


# ============================================================
# 📌 ХЭСЭГ 6: Төрөл хөрвүүлэлт (Type Conversion)
# ============================================================
print("\n--- Төрөл хөрвүүлэлт ---")

# JS:  Number("42"), String(42), Boolean(1)
# Py:  int("42"),    str(42),    bool(1)

# Текстийг тоо руу:
num = int("42")              # 42
num_float = float("3.14")   # 3.14

# Тоог текст руу:
text = str(42)               # "42"
text2 = str(3.14)            # "3.14"

# Boolean руу:
print(bool(1))               # True
print(bool(0))               # False
print(bool(""))              # False
print(bool("0"))             # True    ← ⚠️ JS-д bool("0") ч True!

# ⚠️ Чухал ялгаа — Python нь хатуу хөрвүүлэлт шаарддаг:
# JS:  "5" + 3 = "53"  (текст нэгтгэл)
# Py:  "5" + 3 → TypeError!  (Алдаа!)
# Зөв: "5" + str(3) эсвэл int("5") + 3

try:
    result = "5" + 3
except TypeError as e:
    print(f"⚠️ Алдаа: {e}")
    print(f"Зөв арга: {'5'} + str(3) = {'5' + str(3)}")
    print(f"Зөв арга: int('5') + 3 = {int('5') + 3}")


# ============================================================
# 📌 ХЭСЭГ 7: Хувьсагчийн нэрийн дүрэм
# ============================================================
"""
Python-ий нэрийн convention (PEP 8):

   JS:               Python:
   camelCase          snake_case          ← Хувьсагч, функцэд
   PascalCase         PascalCase          ← Классд (адилхан)
   UPPER_SNAKE        UPPER_SNAKE_CASE    ← Тогтмол утгад (адилхан)
   _private           _private            ← Хувийн (адилхан)
   __dunder__         __dunder__          ← Тусгай аргууд (Python-д л бий)

Жишээ:
   JS:  let userName = "John"
   Py:  user_name = "John"

   JS:  const MAX_RETRY = 3
   Py:  MAX_RETRY = 3

   JS:  class UserProfile {}
   Py:  class UserProfile:

💡 Python нь snake_case ашигладаг (JS-ийн camelCase-ээс ялгаатай).
   Энэ нь PEP 8 стандартын нэг хэсэг.
"""

# Зөв нэрийн жишээнүүд:
user_name = "Болд"           # snake_case — хувьсагч
MAX_CONNECTIONS = 100        # UPPER_SNAKE — тогтмол
_internal_value = 42         # _ эхлэл — хувийн (private)

# Буруу нэрийн жишээнүүд (ажиллах ч гэсэн, convention-ий дагуу буруу):
# userName = "John"          # camelCase — Python-д хэрэглэхгүй
# UserName = "John"          # PascalCase — зөвхөн класст


# ============================================================
# 📌 ХЭСЭГ 8: Олон хувьсагч нэг дор
# ============================================================

# Нэг мөрөнд олон хувьсагч (Tuple unpacking):
x, y, z = 1, 2, 3           # JS: const [x, y, z] = [1, 2, 3]  (destructuring)
print(f"x={x}, y={y}, z={z}")

# Хувьсагчийн утгыг солих (swap):
a = 10
b = 20
a, b = b, a                 # JS-д: [a, b] = [b, a] эсвэл temp хувьсагч хэрэгтэй
print(f"a={a}, b={b}")      # a=20, b=10

# Нэг утга олон хувьсагчид:
x = y = z = 0               # Бүгдийг 0-ээр эхлүүлэх


# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 1.2.1:
   Дараах хувьсагчуудын төрлийг (type) тодорхойл:
   a = 42
   b = 3.14
   c = "hello"
   d = True
   e = None
   f = [1, 2, 3]
   Тус бүрийн type()-ийг хэвлэ.

✏️ Дасгал 1.2.2:
   Хэрэглэгчээс 2 тоо авч (input), нэмэх, хасах, үржих, хуваах
   үр дүнг хэвлэ. Дугуйлалтыг 2 оронтой бутархайгаар хийх.

✏️ Дасгал 1.2.3:
   Нэр, нас, хот гэсэн мэдээллийг f-string ашиглан
   дараах хэлбэрээр хэвлэ:
   ╔═══════════════════════╗
   ║ Нэр:  Болд            ║
   ║ Нас:  25              ║
   ║ Хот:  Улаанбаатар     ║
   ╚═══════════════════════╝

✏️ Дасгал 1.2.4:
   "Hello, World!" текстийг:
   - Бүгд томоор хэвлэ
   - Бүгд жижгээр хэвлэ
   - Урвуугаар хэвлэ
   - Үг тус бүрийг массивт хуваа
   - "World" гэдэг үгийг "Python"-оор сол
"""

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("✅ Хичээл 1.2 амжилттай дууслаа!")
    print("👉 Дараагийн хичээл: 03_data_structures.py")
    print("=" * 50)
