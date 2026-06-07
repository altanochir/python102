"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 1.3: Өгөгдлийн Бүтцүүд                              ║
║  Python 102 — JavaScript програмистад зориулсан                 ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - list, tuple, dict, set — Python-ий 4 гол өгөгдлийн бүтцийг эзэмших
   - List comprehension — Python-ий хамгийн хүчтэй боломж
   - Slicing — Маш чухал ойлголт

💡 JS програмист танд:
   JS-д Array, Object, Set, Map бий.
   Python-д list, dict, set, tuple бий.
   Ойлголт нь ижил, синтакс өөр!
"""


# ============================================================
# 📌 ХЭСЭГ 1: List (Жагсаалт) — JS Array-тай адилхан
# ============================================================
print("═" * 50)
print("📌 LIST — Жагсаалт")
print("═" * 50)

# Жагсаалт үүсгэх:
fruits = ["алим", "жүрж", "гүзээлзгэнэ", "тарвас"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14, None]   # Өөр өөр төрлүүд хольж болно (JS шиг)
empty = []                                # Хоосон жагсаалт

print(f"Жимс: {fruits}")
print(f"Урт: {len(fruits)}")             # JS: fruits.length → Python: len(fruits)


# --- Индексээр авах ---
print(fruits[0])             # "алим"       — Эхний элемент
print(fruits[-1])            # "тарвас"     — Сүүлийн элемент  ← Python-ий давуу тал!
print(fruits[-2])            # "гүзээлзгэнэ" — Сүүлээс 2 дахь

# 💡 JS: fruits[fruits.length - 1]  →  Python: fruits[-1]  (Маш тохиромжтой!)


# --- Slicing (Зүсэлт) ---
# Синтакс: list[start:end:step]
# start: Эхлэх индекс (оруулна)
# end: Төгсөх индекс (оруулахгүй!)
# step: Алхам

nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(nums[2:5])             # [2, 3, 4]     — Индекс 2-оос 4 хүртэл
print(nums[:3])              # [0, 1, 2]     — Эхнээс 3 элемент  ← JS: slice(0, 3)
print(nums[7:])              # [7, 8, 9]     — 7-оос сүүл хүртэл ← JS: slice(7)
print(nums[::2])             # [0, 2, 4, 6, 8] — Хоёр хоёроор алгасах
print(nums[::-1])            # [9, 8, ..., 0]  — Урвуу! ← JS: [...arr].reverse()
print(nums[1:8:2])           # [1, 3, 5, 7]  — 1-ээс 7 хүртэл, 2-оор алгасах

# Слайсаар утга өөрчлөх:
copy = nums[:]               # Бүтэн хуулбар ← JS: [...nums] эсвэл nums.slice()
copy[2:5] = [20, 30, 40]     # Индекс 2-4-ийг солих
print(f"Солисон: {copy}")


# --- List-ийн аргууд (Methods) ---
print("\n--- List methods ---")

fruits = ["алим", "жүрж"]

# Нэмэх:
fruits.append("банан")       # Төгсгөлд нэмэх         ← JS: push()
fruits.insert(1, "чавга")    # Тодорхой индекст нэмэх  ← JS: splice(1, 0, "чавга")
fruits.extend(["нэр", "аньс"])  # Олон элемент нэмэх   ← JS: push(...items)
print(f"Нэмсэн: {fruits}")

# Арилгах:
removed = fruits.pop()       # Сүүлийнхийг авч арилгах  ← JS: pop()
print(f"Арилгасан: {removed}")
fruits.pop(0)                # Индексээр арилгах        ← JS: shift() (эхнийх бол)
fruits.remove("жүрж")        # Утгаар арилгах           ← JS-д шууд арга байхгүй
print(f"Арилгасны дараа: {fruits}")

# Хайх:
idx = fruits.index("банан")  # Индексийг олох           ← JS: indexOf()
print(f"'банан' индекс: {idx}")
print(f"'банан' бий юу: {'банан' in fruits}")  # True   ← JS: includes()

# Эрэмбэлэх:
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()               # Өсөх дарааллаар          ← JS: sort((a,b) => a-b)
print(f"Эрэмбэлсэн: {numbers}")
numbers.sort(reverse=True)   # Буурах дарааллаар
print(f"Урвуу: {numbers}")

# ⚠️ JS vs Python ялгаа:
#    JS: [3,1,2].sort() → [1, 2, 3] (тоог текст шиг эрэмбэлнэ! Алдаатай!)
#    Python: [3,1,2].sort() → [1, 2, 3] (тоог зөв эрэмбэлнэ ✅)

# sorted() — Шинэ жагсаалт буцаана (эх жагсаалтыг өөрчлөхгүй):
original = [3, 1, 4, 1, 5]
new_sorted = sorted(original)
print(f"Эх: {original}")                # [3, 1, 4, 1, 5] — өөрчлөгдөөгүй
print(f"Эрэмбэлсэн хуулбар: {new_sorted}")  # [1, 1, 3, 4, 5]

# Бусад хэрэгтэй аргууд:
print(f"Нийлбэр: {sum(numbers)}")        # JS: numbers.reduce((a,b) => a+b, 0)
print(f"Хамгийн их: {max(numbers)}")     # JS: Math.max(...numbers)
print(f"Хамгийн бага: {min(numbers)}")   # JS: Math.min(...numbers)
print(f"Тоо ширхэг: {len(numbers)}")    # JS: numbers.length


# ============================================================
# 📌 ХЭСЭГ 2: List Comprehension — Python-ий "Супер хүч"!
# ============================================================
print("\n" + "═" * 50)
print("📌 LIST COMPREHENSION")
print("═" * 50)

"""
💡 Энэ нь Python-ий хамгийн гайхалтай боломжуудын нэг!
   JS-ийн map(), filter()-тай адилхан, гэхдээ илүү цэвэрхэн.

Синтакс:
   [илэрхийлэл  for  хувьсагч  in  iterable  if  нөхцөл]
"""

# --- map() equivalent ---
# JS:  [1,2,3,4,5].map(x => x * 2)
# Py:
doubled = [x * 2 for x in [1, 2, 3, 4, 5]]
print(f"Давхардуулсан: {doubled}")       # [2, 4, 6, 8, 10]

# --- filter() equivalent ---
# JS:  [1,2,3,4,5].filter(x => x > 2)
# Py:
filtered = [x for x in [1, 2, 3, 4, 5] if x > 2]
print(f"Шүүсэн: {filtered}")             # [3, 4, 5]

# --- map() + filter() хослуулах ---
# JS:  [1,2,3,4,5].filter(x => x % 2 === 0).map(x => x ** 2)
# Py:
result = [x ** 2 for x in range(1, 11) if x % 2 == 0]
print(f"Тэгш тооны квадрат: {result}")   # [4, 16, 36, 64, 100]

# --- Nested (давхар) comprehension ---
# JS:  arr1.flatMap(x => arr2.map(y => [x, y]))
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(f"Матриц: {matrix}")               # [[1,2,3], [2,4,6], [3,6,9]]

# Матрицыг хавтгайруулах (flatten):
# JS:  matrix.flat()
flat = [num for row in matrix for num in row]
print(f"Хавтгай: {flat}")                # [1, 2, 3, 2, 4, 6, 3, 6, 9]

# --- Текст боловсруулалт ---
words = ["hello", "world", "python"]
upper_words = [w.upper() for w in words]
print(f"Том үсгээр: {upper_words}")

# Үгийн урт 5-аас их:
long_words = [w for w in words if len(w) > 4]
print(f"Урт үгс: {long_words}")

# --- Нөхцөлт утга (ternary in comprehension) ---
# JS:  nums.map(x => x % 2 === 0 ? "тэгш" : "сондгой")
labels = ["тэгш" if x % 2 == 0 else "сондгой" for x in range(1, 6)]
print(f"Шошго: {labels}")                # ['сондгой', 'тэгш', 'сондгой', 'тэгш', 'сондгой']


# ============================================================
# 📌 ХЭСЭГ 3: Tuple (Багц) — Өөрчлөгдөхгүй жагсаалт
# ============================================================
print("\n" + "═" * 50)
print("📌 TUPLE — Өөрчлөгдөхгүй жагсаалт")
print("═" * 50)

"""
💡 JS-д tuple гэж байхгүй.
   Tuple = Зөвхөн уншигддаг (read-only) list.
   Үүсгэсний дараа нэмж, хасч, өөрчилж БОЛОХГҮЙ!

Яагаад хэрэгтэй вэ?
   1. dict-ийн key болж чадна (list болохгүй)
   2. Илүү хурдан (list-ээс)
   3. Өгөгдөл хамгаалалт — санамсаргүй өөрчлөлтөөс сэргийлнэ
   4. Функцээс олон утга буцаахад ашиглана
"""

# Tuple үүсгэх:
point = (3, 4)               # Хаалттай
colors = ("улаан", "ногоон", "цэнхэр")
single = (42,)               # ⚠️ Ганц элементтэй бол ЗААВАЛ таслал!
not_tuple = (42)             # Энэ нь зүгээр л 42 (тоо)!

print(f"Цэг: {point}")
print(f"Төрөл: {type(point)}")           # <class 'tuple'>
print(f"Ганц элемент: {single}, төрөл: {type(single)}")

# Tuple-ийн утгыг авах (list шиг):
print(f"X: {point[0]}, Y: {point[1]}")
print(f"Эхний өнгө: {colors[0]}")

# ⚠️ Tuple-ийг ӨӨРЧЛӨЖ БОЛОХГҮЙ:
try:
    colors[0] = "шар"
except TypeError as e:
    print(f"⚠️ Алдаа: {e}")

# Tuple unpacking (задлах):
x, y = point                 # JS: const [x, y] = point (destructuring)
print(f"x={x}, y={y}")

# Функцээс олон утга буцаахад:
def get_min_max(numbers):
    """Хамгийн бага ба их утгыг буцаах"""
    return min(numbers), max(numbers)    # tuple буцаана

lo, hi = get_min_max([5, 2, 8, 1, 9])
print(f"Мин: {lo}, Макс: {hi}")

# * (star) ашиглан задлах:
first, *rest = [1, 2, 3, 4, 5]          # JS: const [first, ...rest] = arr
print(f"Эхний: {first}, Үлдсэн: {rest}")  # 1, [2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
print(f"Эхний: {first}, Дунд: {middle}, Сүүлийн: {last}")  # 1, [2,3,4], 5

# Named tuple (нэртэй tuple — struct шиг):
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"Point: x={p.x}, y={p.y}")       # Нэрээр хандаж болно!


# ============================================================
# 📌 ХЭСЭГ 4: Dictionary (Толь бичиг) — JS Object/Map
# ============================================================
print("\n" + "═" * 50)
print("📌 DICT — Толь бичиг")
print("═" * 50)

"""
💡 JS-тэй харьцуулалт:
   JS Object {} ↔ Python dict {}
   Бараг адилхан ажиллана!

   Ялгаа:
   - JS: { name: "John" }     ← key-г хашилтгүй бичиж болно
   - Py: { "name": "John" }   ← key ЗААВАЛ хашилттай (str бол)
"""

# Dict үүсгэх:
person = {
    "name": "Болд",
    "age": 25,
    "city": "Улаанбаатар",
    "skills": ["Python", "JavaScript"],
    "is_student": False
}

print(f"Хүн: {person}")

# Утга авах:
print(person["name"])         # "Болд"    ← JS: person.name эсвэл person["name"]
# print(person["phone"])      # ⚠️ KeyError! (JS-д undefined буцаана)

# .get() — Аюулгүй арга (KeyError гарахгүй):
print(person.get("phone"))            # None     ← JS: person.phone → undefined
print(person.get("phone", "N/A"))     # "N/A"    ← default утга

# 💡 JS vs Python:
#    JS:  person.name ?? "default"     (nullish coalescing)
#    Py:  person.get("name", "default")


# --- Dict-д нэмэх, өөрчлөх ---
person["email"] = "bold@email.mn"     # Шинэ key нэмэх / одоо байгааг өөрчлөх
person["age"] = 26                    # Утга өөрчлөх
print(f"Шинэчилсэн: {person}")

# Олон key нэг дор шинэчлэх:
person.update({
    "phone": "99001122",
    "age": 27
})
# JS:  Object.assign(person, { phone: "99001122", age: 27 })
# Py:  person.update({ "phone": "99001122", "age": 27 })

# --- Dict-ээс арилгах ---
del person["is_student"]             # Key арилгах  ← JS: delete person.is_student
removed_val = person.pop("email")    # Авч арилгах (утгыг нь буцаана)
print(f"Арилгасан email: {removed_val}")


# --- Dict шалгалт ---
print("name" in person)              # True  — key бий юу?  ← JS: "name" in person
print("phone" in person)             # True

# ⚠️ JS vs Python ялгаа:
#    JS:  "name" in person → prototype chain-ыг ч шалгана
#    Python: "name" in person → зөвхөн шууд key-г шалгана


# --- Dict-ийг давтах (iterate) ---
print("\n--- Dict давтах ---")

# Keys:
for key in person:                    # JS: for (let key in person)
    print(f"  Key: {key}")

# Values:
for value in person.values():         # JS: Object.values(person).forEach(...)
    print(f"  Value: {value}")

# Key-Value хос:
for key, value in person.items():     # JS: Object.entries(person).forEach(([k,v]) => ...)
    print(f"  {key}: {value}")

# 💡 JS-тэй харьцуулалт:
#    JS:  Object.keys(obj)     →  Py: dict.keys()
#    JS:  Object.values(obj)   →  Py: dict.values()
#    JS:  Object.entries(obj)  →  Py: dict.items()


# --- Dict Comprehension ---
# JS:  Object.fromEntries(arr.map(x => [x, x*x]))
squares = {x: x**2 for x in range(1, 6)}
print(f"Квадратууд: {squares}")       # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Шүүлттэй:
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(f"Тэгш квадрат: {even_squares}")

# Dict-ийг нийлүүлэх (merge):
# JS:  { ...dict1, ...dict2 }
# Py:  { **dict1, **dict2 }    (Python 3.5+)
# Py:  dict1 | dict2            (Python 3.9+)

defaults = {"theme": "dark", "lang": "en", "font_size": 14}
user_prefs = {"lang": "mn", "font_size": 16}

# Арга 1: ** (spread)
settings = {**defaults, **user_prefs}
print(f"Тохиргоо: {settings}")

# Арга 2: | оператор (Python 3.9+)
settings2 = defaults | user_prefs
print(f"Тохиргоо2: {settings2}")


# ============================================================
# 📌 ХЭСЭГ 5: Set (Олонлог) — Давтагдахгүй цуглуулга
# ============================================================
print("\n" + "═" * 50)
print("📌 SET — Олонлог")
print("═" * 50)

"""
💡 JS-ийн Set-тэй бараг адилхан.
   Ялгаа: Python-ий Set нь математикийн олонлогийн бүх үйлдлийг дэмждэг!
"""

# Set үүсгэх:
fruits = {"алим", "жүрж", "банан", "алим"}  # "алим" давтагдсан
print(f"Set: {fruits}")                      # Давтагдсан "алим" арилсан

# ⚠️ Хоосон set: {} биш set() !!!
empty_set = set()             # {} нь хоосон dict!
empty_dict = {}               # Энэ нь dict

# List-ээс set үүсгэх (давтагдсаныг арилгах):
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = set(numbers)
print(f"Давтагдахгүй: {unique}")           # {1, 2, 3, 4}

# --- Set-ийн аргууд ---
colors = {"улаан", "ногоон", "цэнхэр"}
colors.add("шар")             # Нэмэх       ← JS: set.add()
colors.discard("ногоон")      # Арилгах     ← JS: set.delete()
print(f"in: {'улаан' in colors}")  # True   ← JS: set.has()
print(f"Урт: {len(colors)}")                # JS: set.size

# --- Олонлогийн үйлдлүүд (Математик!) ---
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(f"A ∪ B (нэгдэл): {a | b}")           # {1,2,3,4,5,6,7,8}  ← union
print(f"A ∩ B (огтлолцол): {a & b}")         # {4, 5}             ← intersection
print(f"A - B (ялгавар): {a - b}")           # {1, 2, 3}          ← difference
print(f"A △ B (тэгш хэм ялгавар): {a ^ b}") # {1,2,3,6,7,8}      ← symmetric_difference

# Set comprehension:
even_set = {x for x in range(20) if x % 2 == 0}
print(f"Тэгш тоонууд: {even_set}")

# 💡 Set нь хайлтад маш хурдан! (O(1) — list нь O(n))
big_list = list(range(1_000_000))
big_set = set(range(1_000_000))
# 999_999 in big_list  → Удаан (бүгдийг шалгана)
# 999_999 in big_set   → Маш хурдан (hash lookup)


# ============================================================
# 📌 ХЭСЭГ 6: Бүтцүүдийг хооронд нь хөрвүүлэх
# ============================================================
print("\n--- Хөрвүүлэлт ---")

# list ↔ tuple ↔ set
my_list = [1, 2, 2, 3, 3, 3]
my_tuple = tuple(my_list)     # list → tuple
my_set = set(my_list)         # list → set (давтагдсан арилна)
back_to_list = list(my_set)   # set → list

print(f"List: {my_list}")
print(f"Tuple: {my_tuple}")
print(f"Set: {my_set}")
print(f"Буцаасан List: {back_to_list}")

# dict-ийн keys, values-ийг list болгох:
person = {"name": "Болд", "age": 25}
keys = list(person.keys())
values = list(person.values())
items = list(person.items())  # [(key, value), ...] — tuple-ийн list
print(f"Keys: {keys}")
print(f"Values: {values}")
print(f"Items: {items}")


# ============================================================
# 📌 ХЭСЭГ 7: Гүн хуулбар vs Гүехэн хуулбар (Deep vs Shallow copy)
# ============================================================
print("\n--- Copy ---")

"""
💡 JS-тэй адил асуудал! Object/Array нь reference-ээр дамждаг.
"""

# ⚠️ Гүехэн хуулбар (shallow copy):
original = [1, 2, [3, 4]]
shallow = original[:]         # JS: [...original]
shallow[0] = 99
shallow[2][0] = 99            # ⚠️ Дотоод list-ийг ч өөрчилнө!

print(f"Original: {original}")  # [1, 2, [99, 4]] ← 😱 original ч өөрчлөгдсөн!
print(f"Shallow: {shallow}")    # [99, 2, [99, 4]]

# ✅ Гүн хуулбар (deep copy):
import copy
original = [1, 2, [3, 4]]
deep = copy.deepcopy(original)
deep[2][0] = 99

print(f"Original: {original}")  # [1, 2, [3, 4]] ← Өөрчлөгдөөгүй ✅
print(f"Deep: {deep}")          # [1, 2, [99, 4]]

# JS:  JSON.parse(JSON.stringify(obj)) — Хуучин арга
#      structuredClone(obj) — Шинэ арга
# Py:  copy.deepcopy(obj)


# ============================================================
# 📌 ХЭСЭГ 8: Хэрэгтэй built-in функцүүд
# ============================================================
print("\n--- Built-in функцүүд ---")

# enumerate() — Индекстэй давтах
# JS:  arr.forEach((item, index) => ...)
fruits = ["алим", "жүрж", "банан"]
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# Эхлэх индексийг өөрчлөх:
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}. {fruit}")

# zip() — Олон жагсаалтыг зэрэгцүүлж давтах
names = ["Болд", "Дорж", "Сараа"]
ages = [25, 30, 22]
cities = ["УБ", "Дархан", "Эрдэнэт"]

for name, age, city in zip(names, ages, cities):
    print(f"  {name}, {age} настай, {city}")

# zip() + dict():
name_age = dict(zip(names, ages))
print(f"  Dict: {name_age}")              # {"Болд": 25, "Дорж": 30, "Сараа": 22}

# any() & all() — JS: some() & every()
numbers = [2, 4, 6, 8, 10]
print(f"Бүгд тэгш үү? {all(x % 2 == 0 for x in numbers)}")   # True  ← JS: every()
print(f"Нэг нь ч 5 үү? {any(x == 5 for x in numbers)}")       # False ← JS: some()

# map() & filter() — Функц хэлбэр (list comprehension илүү түгээмэл)
# JS:  [1,2,3].map(x => x*2)
doubled = list(map(lambda x: x * 2, [1, 2, 3]))
print(f"map: {doubled}")

# JS:  [1,2,3,4,5].filter(x => x > 2)
big = list(filter(lambda x: x > 2, [1, 2, 3, 4, 5]))
print(f"filter: {big}")

# 💡 Python-д map/filter-ийн оронд list comprehension ашиглахыг зөвлөнө.
#    Илүү уншихад хялбар!


# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 1.3.1:
   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] жагсаалтаас:
   a) Тэгш тоонуудыг шүүж авах (list comprehension)
   b) Тоо бүрийн кубыг (x³) тооцоолох
   c) 3-д хуваагддаг тоонуудын нийлбэр олох

✏️ Дасгал 1.3.2:
   Хэрэглэгчдийн мэдээллийг dict-ээр хадгалж, хэвлэ:
   users = [
       {"name": "Болд", "age": 25, "active": True},
       {"name": "Дорж", "age": 30, "active": False},
       {"name": "Сараа", "age": 22, "active": True},
   ]
   a) Идэвхтэй хэрэглэгчдийн нэрийг хэвлэ
   b) Дундаж насыг тооцоол
   c) Хамгийн залуу хэрэглэгчийг ол

✏️ Дасгал 1.3.3:
   Хоёр текстийн нийтлэг тэмдэгтүүдийг ол (set ашиглах):
   text1 = "hello world"
   text2 = "world peace"
   Нийтлэг тэмдэгтүүд: ?

✏️ Дасгал 1.3.4:
   Доорх матрицыг транспоз хий (мөр ↔ багана):
   matrix = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
   Үр дүн: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
   💡 Hint: zip(*matrix) ашиглаарай
"""

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("✅ Хичээл 1.3 амжилттай дууслаа!")
    print("👉 Дараагийн хичээл: 04_control_flow.py")
    print("=" * 50)
