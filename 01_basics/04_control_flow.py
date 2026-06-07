"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 1.4: Нөхцөл & Давталт (Control Flow)               ║
║  Python 102 — JavaScript програмистад зориулсан                 ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - if / elif / else нөхцөлийн бүтэц
   - for, while давталтууд
   - range(), enumerate(), zip()
   - match-case (Python 3.10+)
   - Walrus operator :=

💡 JS програмистад:
   Python-д {} хаалт, () хаалт байхгүй — ИНДЕНТ + : ашиглана.
   && || ! → and or not
   switch → match (Python 3.10+)
"""


# ============================================================
# 📌 ХЭСЭГ 1: if / elif / else
# ============================================================
print("═" * 50)
print("📌 IF / ELIF / ELSE")
print("═" * 50)

# --- Энгийн if ---
age = 20

# JS:  if (age >= 18) { console.log("Насанд хүрсэн"); }
# Py:
if age >= 18:
    print("Насанд хүрсэн")

# --- if-else ---
temperature = -15

# JS:  if (temp > 0) { ... } else { ... }
# Py:
if temperature > 0:
    print("Дулаан байна ☀️")
else:
    print("Хүйтэн байна 🥶")

# --- if-elif-else ---
# JS:  if () {} else if () {} else {}
# Py:  if: ... elif: ... else:     ← "else if" биш, "elif"!

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Оноо: {score}, Үнэлгээ: {grade}")  # B

# ⚠️ Анхаар:
#   1. Хаалт () шаардлагагүй (бичиж ч болно, гэхдээ Pythonic биш)
#   2. Блокийн эхэнд : (хоёр цэг) заавал байх ёстой
#   3. Блокийг ИНДЕНТ-ээр тодорхойлно (4 зай = 1 tab)


# --- Ternary operator (нэг мөрт нөхцөл) ---
# JS:  const status = age >= 18 ? "adult" : "minor"
# Py:
status = "насанд хүрсэн" if age >= 18 else "хүүхэд"
print(f"Статус: {status}")

# Ternary-г дотор нь бичиж ч болно:
print(f"Температур: {'дулаан' if temperature > 0 else 'хүйтэн'}")


# --- Logical operators ---
# JS:  && || !
# Py:  and or not

username = "admin"
password = "1234"

if username == "admin" and password == "1234":
    print("✅ Нэвтэрлээ!")

is_weekend = True
is_holiday = False

if is_weekend or is_holiday:
    print("🎉 Амрах өдөр!")

if not is_holiday:
    print("📅 Амралт биш")


# --- Short-circuit evaluation (JS-тэй адилхан) ---
# JS:  value = obj && obj.name
# Py:  Python-д ч бас and/or short-circuit

name = ""
display_name = name or "Зочин"         # name хоосон бол "Зочин"
print(f"Нэр: {display_name}")

# 💡 JS:  value = a ?? b  (nullish coalescing)
#    Python-д ?? байхгүй. Гэхдээ:
value = None
result = value if value is not None else "default"
print(f"Утга: {result}")


# --- Membership шалгалт: in ---
# JS:  arr.includes(x) эсвэл "key" in obj
# Py:  x in collection

fruits = ["алим", "жүрж", "банан"]
print("алим" in fruits)              # True
print("тарвас" not in fruits)        # True  ← not in — маш тохиромжтой!

text = "Hello Python World"
print("Python" in text)              # True — Текстэнд ч ажиллана!

person = {"name": "Болд", "age": 25}
print("name" in person)             # True — Dict-ийн key шалгана


# --- Chained comparison (Python-ий давуу тал!) ---
# JS:  if (x > 0 && x < 100) — 2 нөхцөл бичих хэрэгтэй
# Py:
x = 50
if 0 < x < 100:                     # Математик шиг бичнэ!
    print(f"{x} нь 0-100 хооронд")

if 1 <= x <= 100:
    print(f"{x} нь 1-100 хооронд (хүрээ оролцуулан)")


# ============================================================
# 📌 ХЭСЭГ 2: for давталт
# ============================================================
print("\n" + "═" * 50)
print("📌 FOR ДАВТАЛТ")
print("═" * 50)

"""
💡 Python-ий for давталт нь JS-ийн for...of-тай адилхан.
   JS-ийн for (let i=0; i<n; i++) хэлбэр Python-д БАЙХГҮЙ.
   Python-д range() ашиглана.
"""

# --- Жагсаалтыг давтах ---
# JS:  for (const fruit of fruits) { ... }
# Py:
fruits = ["алим", "жүрж", "банан", "тарвас"]
for fruit in fruits:
    print(f"  🍎 {fruit}")

# --- range() — Тоон давталт ---
# JS:  for (let i = 0; i < 5; i++)
# Py:
for i in range(5):                   # 0, 1, 2, 3, 4
    print(f"  i = {i}")

# range(start, stop, step):
for i in range(1, 10, 2):            # 1, 3, 5, 7, 9 — сондгой тоонууд
    print(f"  Сондгой: {i}")

for i in range(10, 0, -1):           # 10, 9, 8, ..., 1 — Урвуу
    print(f"  Countdown: {i}")

# 💡 range() нь жагсаалт биш, iterator (санах ойд хэмнэлттэй)
#    list(range(5)) гэж бичвэл жагсаалт болно: [0, 1, 2, 3, 4]


# --- enumerate() — Индекстэй давтах ---
# JS:  fruits.forEach((fruit, index) => ...)
# Py:
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# Эхлэх индексийг заах:
for num, fruit in enumerate(fruits, start=1):
    print(f"  {num}. {fruit}")


# --- zip() — Олон жагсаалтыг зэрэг давтах ---
names = ["Болд", "Дорж", "Сараа"]
ages = [25, 30, 22]
cities = ["УБ", "Дархан", "Эрдэнэт"]

for name, age, city in zip(names, ages, cities):
    print(f"  {name} ({age} нас) — {city}")

# 💡 JS-д ийм зүйлийг гараар хийх хэрэгтэй:
#    for (let i=0; i < names.length; i++) {
#        console.log(names[i], ages[i], cities[i]);
#    }


# --- Dict давтах ---
person = {"name": "Болд", "age": 25, "city": "УБ"}

# Зөвхөн key:
for key in person:
    print(f"  Key: {key}")

# Key + Value:
for key, value in person.items():
    print(f"  {key} = {value}")


# --- Текст давтах ---
for char in "Python":
    print(f"  '{char}'", end=" ")
print()  # Шинэ мөр


# --- Nested (давхар) for ---
for i in range(1, 4):
    for j in range(1, 4):
        print(f"  {i} × {j} = {i*j}", end="\t")
    print()  # Мөр шилжих


# ============================================================
# 📌 ХЭСЭГ 3: while давталт
# ============================================================
print("\n" + "═" * 50)
print("📌 WHILE ДАВТАЛТ")
print("═" * 50)

# JS-тэй бараг адилхан, зөвхөн () хаалт, {} хаалт байхгүй

count = 5
while count > 0:
    print(f"  ⏳ {count}...")
    count -= 1                       # ⚠️ Python-д count-- АЖИЛЛАХГҮЙ!
print("  🚀 Нисэв!")

# 💡 JS vs Python:
#    JS:  count++, count--    (increment/decrement)
#    Py:  count += 1, count -= 1  (++ -- байхгүй!)


# --- while True + break ---
# Хязгааргүй давталт + гарах нөхцөл

import random

print("\n--- Тоо таах тоглоом (демо) ---")
secret = random.randint(1, 10)
attempts = 0

while True:
    # Демо: Санамсаргүй тоо "таах"
    guess = random.randint(1, 10)
    attempts += 1

    if guess == secret:
        print(f"  🎉 Таалаа! {secret} — {attempts} оролдлого!")
        break                         # Давталтаас гарах

    if attempts > 20:
        print(f"  ❌ Хэтэрхий олон оролдлого. Хариу: {secret}")
        break


# ============================================================
# 📌 ХЭСЭГ 4: break, continue, pass, else
# ============================================================
print("\n" + "═" * 50)
print("📌 BREAK, CONTINUE, PASS, ELSE")
print("═" * 50)

# --- break — Давталтаас гарах ---
# JS-тэй адилхан
for i in range(10):
    if i == 5:
        print(f"  🛑 {i} дээр зогслоо")
        break
    print(f"  {i}", end=" ")
print()

# --- continue — Дараагийн давталт руу алгасах ---
# JS-тэй адилхан
print("Тэгш тоонууд: ", end="")
for i in range(10):
    if i % 2 != 0:
        continue                     # Сондгой тоонуудыг алгасах
    print(i, end=" ")
print()

# --- pass — Юу ч хийхгүй (placeholder) ---
# JS-д ийм зүйл байхгүй (хоосон {} бичдэг)
# Python-д хоосон блок бичиж болохгүй тул pass ашиглана

for i in range(5):
    if i == 3:
        pass                         # TODO: Дараа хийнэ
    # pass байхгүй бол SyntaxError гарна!

# Хоосон функц тодорхойлоход:
def todo_function():
    pass                             # Дараа хэрэгжүүлнэ

# Хоосон класс:
class EmptyClass:
    pass

# 💡 pass = "Юу ч хийхгүй" гэсэн утгатай.
#    Кодын бүтэц бичихдээ placeholder болгон ашиглана.


# --- for...else (Python-ий онцлог!) ---
"""
💡 JS-д ийм зүйл БАЙХГҮЙ!
   for...else: давталт break-ГҮЙ дууссан бол else блок ажиллана.
   break хийсэн бол else ажиллахгүй.
"""

# Жишээ: Анхны тоо (prime) шалгах
def is_prime(n):
    """n нь анхны тоо мөн эсэхийг шалгах"""
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            print(f"  {n} = {i} × {n // i} — Анхны тоо биш")
            break
    else:
        # for давталт break-гүй дууссан = хуваагч олдсонгүй
        print(f"  {n} — Анхны тоо ✅")
        return True

    return False

is_prime(7)    # 7 — Анхны тоо ✅
is_prime(12)   # 12 = 2 × 6 — Анхны тоо биш
is_prime(29)   # 29 — Анхны тоо ✅


# ============================================================
# 📌 ХЭСЭГ 5: match-case (Python 3.10+)
# ============================================================
print("\n" + "═" * 50)
print("📌 MATCH-CASE (Pattern Matching)")
print("═" * 50)

"""
💡 JS-ийн switch...case-тай АДИЛХАН, гэхдээ илүү хүчирхэг!
   Python 3.10+ дээр ажиллана.

   JS:  switch(value) { case "a": ...; break; }
   Py:  match value: case "a": ...

   ⚠️ break бичих шаардлагагүй! (fall-through байхгүй)
"""

# --- Энгийн match ---
def describe_http_status(status):
    match status:
        case 200:
            return "✅ OK"
        case 301:
            return "↪️ Redirect"
        case 404:
            return "❌ Not Found"
        case 500:
            return "💥 Server Error"
        case _:                       # _ = default (JS: default:)
            return f"❓ Unknown ({status})"

print(describe_http_status(200))   # ✅ OK
print(describe_http_status(404))   # ❌ Not Found
print(describe_http_status(418))   # ❓ Unknown (418)


# --- Pattern matching (struct шиг задлах) ---
def process_command(command):
    match command.split():
        case ["quit"]:
            print("  👋 Гарч байна...")
        case ["hello", name]:
            print(f"  👋 Сайн уу, {name}!")
        case ["add", *numbers]:
            total = sum(int(n) for n in numbers)
            print(f"  ➕ Нийлбэр: {total}")
        case ["move", direction, distance]:
            print(f"  🏃 {direction} чиглэлд {distance} алхам")
        case _:
            print(f"  ❓ '{command}' — Тодорхойгүй команд")

process_command("hello Болд")        # 👋 Сайн уу, Болд!
process_command("add 1 2 3 4 5")      # ➕ Нийлбэр: 15
process_command("move north 10")      # 🏃 north чиглэлд 10 алхам
process_command("quit")               # 👋 Гарч байна...

# --- Dict pattern matching ---
def process_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            print(f"  🖱️ Click: ({x}, {y})")
        case {"type": "keypress", "key": key}:
            print(f"  ⌨️ Key: {key}")
        case {"type": "scroll", "direction": d}:
            print(f"  🔄 Scroll: {d}")
        case _:
            print(f"  ❓ Unknown event")

process_event({"type": "click", "x": 100, "y": 200})
process_event({"type": "keypress", "key": "Enter"})


# ============================================================
# 📌 ХЭСЭГ 6: Walrus Operator := (Python 3.8+)
# ============================================================
print("\n" + "═" * 50)
print("📌 WALRUS OPERATOR :=")
print("═" * 50)

"""
💡 := нь "далайн морь" (walrus) оператор.
   Утга оноож, тэр утгыг нэг дор ашиглах боломжтой.
   JS-д ийм тусгай оператор байхгүй.
"""

# Хуучин арга (walrus-гүй):
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered = [x for x in data if x > 5]
n = len(filtered)
if n > 0:
    print(f"  {n} элемент олдсон (хуучин арга)")

# Шинэ арга (walrus-тай):
if (n := len([x for x in data if x > 5])) > 0:
    print(f"  {n} элемент олдсон (walrus)")

# while давталтад:
# import random  # (дээр import хийсэн)
print("\n  Walrus + while:")
while (num := random.randint(1, 10)) != 7:
    print(f"    {num} (7 биш)")
print(f"    {num} олдлоо! 🎯")

# List comprehension дотор:
# Тооцооллыг нэг л удаа хийж, шүүлт + утга хоёуланд ашиглах
import math
results = [(x, y) for x in range(10) if (y := math.sqrt(x)) == int(y)]
print(f"  Бүтэн квадратууд: {results}")  # [(0, 0.0), (1, 1.0), (4, 2.0), (9, 3.0)]


# ============================================================
# 📌 ХЭСЭГ 7: Бодит жишээ — Нэр хайгч (Mini Project)
# ============================================================
print("\n" + "═" * 50)
print("📌 ЖИШЭЭ: Оюутны дүнгийн систем")
print("═" * 50)

students = [
    {"name": "Болд", "scores": [85, 92, 78, 95]},
    {"name": "Дорж", "scores": [70, 65, 80, 72]},
    {"name": "Сараа", "scores": [95, 98, 92, 97]},
    {"name": "Түмэн", "scores": [50, 45, 60, 55]},
    {"name": "Оюука", "scores": [88, 82, 90, 85]},
]

print(f"\n  {'Нэр':<10} {'Дундаж':>8} {'Үнэлгээ':>8} {'Статус':>8}")
print("  " + "-" * 38)

for student in students:
    name = student["name"]
    scores = student["scores"]
    avg = sum(scores) / len(scores)

    # Үнэлгээ тодорхойлох
    if avg >= 90:
        grade = "A"
    elif avg >= 80:
        grade = "B"
    elif avg >= 70:
        grade = "C"
    elif avg >= 60:
        grade = "D"
    else:
        grade = "F"

    status = "✅ Тэнцсэн" if avg >= 60 else "❌ Тэнцээгүй"
    print(f"  {name:<10} {avg:>8.1f} {grade:>8} {status:>8}")

# Статистик:
all_avgs = [sum(s["scores"]) / len(s["scores"]) for s in students]
print(f"\n  📊 Ангийн дундаж: {sum(all_avgs) / len(all_avgs):.1f}")
print(f"  📈 Хамгийн өндөр: {max(all_avgs):.1f}")
print(f"  📉 Хамгийн бага: {min(all_avgs):.1f}")

# Тэнцсэн/тэнцээгүй тоо:
passed = sum(1 for avg in all_avgs if avg >= 60)
failed = len(all_avgs) - passed
print(f"  ✅ Тэнцсэн: {passed}, ❌ Тэнцээгүй: {failed}")


# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 1.4.1:
   FizzBuzz тоглоом:
   1-ээс 100 хүртэл тоонууд:
   - 3-д хуваагддаг бол "Fizz" хэвлэ
   - 5-д хуваагддаг бол "Buzz" хэвлэ
   - 3 ба 5-д хоёуланд хуваагддаг бол "FizzBuzz" хэвлэ
   - Бусад тохиолдолд тоогоо хэвлэ

✏️ Дасгал 1.4.2:
   Пирамид хэвлэ (n=5):
       *
      ***
     *****
    *******
   *********

✏️ Дасгал 1.4.3:
   match-case ашиглан тооцоолуур бич:
   "add 5 3"     → 8
   "sub 10 4"    → 6
   "mul 3 7"     → 21
   "div 15 3"    → 5.0
   "quit"        → Гарах

✏️ Дасгал 1.4.4:
   for...else ашиглан жагсаалтаас тодорхой утга хайх.
   Олдвол: "Олдлоо!" хэвлэх
   Олдохгүй бол: "Олдсонгүй" хэвлэх
"""

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("✅ Хичээл 1.4 амжилттай дууслаа!")
    print("👉 Дараагийн хичээл: 05_functions.py")
    print("=" * 50)
