"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 2.3: Pythonic Код — Илүү хурдан, илүү цэгцтэй код бичих ║
║  Tech With Tim-ийн зөвлөмж: Tutorial hell-ээс гарах 5 алхам      ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. List, Dict & Set Comprehensions (Хамгийн хэрэгтэй бичиглэл)
   2. Generators & Generator Expressions (Санах ойн хэмнэлт)
   3. Context Managers (with оператор, нөөцийг цэвэрлэх)
   4. Advanced Dictionary & Set Operations (Профессионал ажиллагаа)

💡 JavaScript (Node.js) туршлагатай танд зориулсан харьцуулалтууд орсон.
"""

import sys
import time
import os
from collections import defaultdict
from contextlib import contextmanager

# ============================================================
# 📌 ХЭСЭГ 1: List, Dict & Set Comprehensions
# ============================================================
"""
💡 JavaScript-д бид `.map()` болон `.filter()` ашиглаж массивыг өөрчилдөг:
   JS:  const doubles = numbers.map(x => x * 2).filter(x => x > 10);
   
Python-д үүнийг "List Comprehension" ашиглаж маш хялбар бичдэг.
Энэ нь кодыг богино, уншихад хялбар болгохоос гадна C хэл дээр бичигдсэн тул энгийн loop-ээс хурдан ажилладаг!
"""

def example_1_comprehensions():
    print("\n=== 1. Comprehensions (Жагсаалт үүсгэх товчлол) ===")
    
    # --- Жишээ 1: Энгийн List Comprehension ---
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Уламжлалт арга:
    traditional_doubles = []
    for x in numbers:
        if x > 5:
            traditional_doubles.append(x * 2)
            
    # Pythonic арга (Comprehension):
    # Загвар: [expression for item in iterable if condition]
    pythonic_doubles = [x * 2 for x in numbers if x > 5]
    
    print(f"Эхний жагсаалт: {numbers}")
    print(f"Уламжлалт аргаар (>5-ыг 2-оор үржүүлсэн): {traditional_doubles}")
    print(f"Pythonic аргаар (>5-ыг 2-оор үржүүлсэн): {pythonic_doubles}")
    
    # --- Жишээ 2: Dictionary Comprehension ---
    # JS: const keyValues = items.reduce((acc, curr) => ({...acc, [curr.id]: curr}), {})
    users = [("alice", 25), ("bob", 30), ("charlie", 35)]
    
    # Нэр ба насаар dictionary үүсгэх
    user_dict = {name.title(): age for name, age in users}
    print(f"\nDictionary Comprehension: {user_dict}")
    
    # Нөхцөл шалгах
    adult_dict = {name: age for name, age in user_dict.items() if age >= 30}
    print(f"Зөвхөн 30-аас дээш насныхан: {adult_dict}")

    # --- Жишээ 3: Set Comprehension ---
    # Давхардаагүй өгөгдөл үүсгэх
    words = ["apple", "banana", "apple", "cherry", "banana"]
    unique_lengths = {len(word) for word in words}
    print(f"\nҮгийн уртуудын Set (давхардалгүй): {unique_lengths}")


# ============================================================
# 📌 ХЭСЭГ 2: Generators & Generator Expressions
# ============================================================
"""
Машин сургалт (ML/AI) болон том өгөгдөл (Big Data)-д санах ой (RAM) маш чухал.
List Comprehension нь үр дүнгээ шууд RAM дээр хадгалдаг бол
Generator нь зөвхөн дуудсан үед нь ("lazy evaluation") өгөгдлийг нэг нэгээр нь боловсруулдаг.

💡 JS: Generator functions (function*) болон `yield` түлхүүр үгтэй яг ижил.
"""

def example_2_generators():
    print("\n=== 2. Generators & Memory Efficiency ===")
    
    # Санах ойн хэмжээ харьцуулах жишээ
    # 1 сая тооны квадрат
    limit = 1000000
    
    # 1. List (Бүх тоог санах ойд шууд үүсгэнэ)
    start_time = time.time()
    num_list = [x ** 2 for x in range(limit)]
    list_memory = sys.getsizeof(num_list) / (1024 * 1024) # MB болгох
    list_time = time.time() - start_time
    
    # 2. Generator Expression (Бүх өгөгдлийг үүсгэхгүй, хэрэгцээт үед нь үүсгэнэ)
    # List comprehension-оос ялгаа нь хаалтанд бичнэ ()
    start_time = time.time()
    num_generator = (x ** 2 for x in range(limit))
    generator_memory = sys.getsizeof(num_generator) / 1024 # KB болгох
    generator_time = time.time() - start_time
    
    print(f"1. List Comprehension [x**2 for x in range({limit})]:")
    print(f"   - Санах ой: {list_memory:.4f} MB")
    print(f"   - Үүсгэх хугацаа: {list_time:.4f} секунд")
    
    print(f"2. Generator Expression (x**2 for x in range({limit})):")
    print(f"   - Санах ой: {generator_memory:.4f} KB (Маш бага! 🤩)")
    print(f"   - Үүсгэх хугацаа: {generator_time:.4f} секунд (Шууд ажиллана!)")
    
    # Өгөгдлийг уншихдаа `next()` эсвэл `for loop` ашиглана:
    print("\nGenerator-оос эхний 3 үр дүнг авах:")
    print(f"Эхнийх: {next(num_generator)}")
    print(f"Дараагийнх: {next(num_generator)}")
    print(f"Гурав дахь: {next(num_generator)}")
    
    # Custom Generator функц (yield түлхүүр үг)
    def my_fibonacci(n):
        """Фибоначчийн цуваа үүсгэгч generator"""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
            
    print("\nFibonacci generator ажиллуулах (эхний 6):")
    fib = my_fibonacci(6)
    for num in fib:
        print(f"-> {num}")


# ============================================================
# 📌 ХЭСЭГ 3: Context Managers (with оператор)
# ============================================================
"""
Програм бичихэд файл нээх, сүлжээний холболт, өгөгдлийн сангийн холболтыг нээгээд
буцааж хаахгүй орхивол нөөцийн алдагдал гардаг.
`with` оператор нь ямар ч нөхцөлд (алдаа гарсан ч гэсэн) нөөцийг найдвартай хааж цэвэрлэдэг.

💡 JS: `try { ... } finally { connection.close() }` гэсэн урт бичиглэлийг хялбарчилсан хувилбар.
"""

# Custom Context Manager үүсгэх 1-р арга: Class ашиглах
class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
        
    def __enter__(self):
        print(f"  [__enter__] Файлыг нээлээ: {self.filename}")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("  [__exit__] Файлыг хааж байна...")
        if self.file:
            self.file.close()
        # Хэрэв True буцаавал гарсан алдааг дээш нь шидэхгүй (suppress хийнэ)
        return False

# Custom Context Manager үүсгэх 2-р арга: @contextmanager decorator
@contextmanager
def simple_timer(label):
    start = time.time()
    print(f"\n⏳ '{label}' эхэллээ...")
    try:
        yield  # control goes back to the with-block
    finally:
        end = time.time()
        print(f"⏱️ '{label}' дууслаа. Хугацаа: {end - start:.5f} сек")


def example_3_context_managers():
    print("\n=== 3. Context Managers (Нөөц удирдах) ===")
    
    filename = "temp_test.txt"
    
    # 1. Сонгодог файл бичих / унших
    # Python-д built-in `open` нь context manager бөгөөд 'with'-ээр ашигладаг
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Сайн байна уу! Энэ бол context manager-ийн жишээ.\n")
        f.write("Төгсгөлд нь файлыг автоматаар хаана.\n")
        
    print(f"Файл '{filename}' амжилттай үүслээ.")
    
    # 2. Custom Class Context Manager ажиллуулах
    print("\nCustom Class Context Manager тест:")
    with FileOpener(filename, "r") as f:
        content = f.read()
        print(f"Уншсан контент: {content.strip()}")
        
    # 3. Custom Timer Context Manager ажиллуулах
    with simple_timer("Хүнд тооцоолол"):
        # Хүнд тооцоолол дуурайлгах
        total = sum(x**2 for x in range(10000000))
        print(f"Үр дүн: {total}")
        
    # Цэвэрлэгээ
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\nTүр файл '{filename}' устгагдлаа.")


# ============================================================
# 📌 ХЭСЭГ 4: Advanced Dictionary & Set Operations
# ============================================================
"""
Python-ийн Dictionary болон Set нь дотроо Hash Table ашигладаг тул маш хурдан (O(1) lookup).
Tech With Tim-ийн хэлснээр, дунд шатны программист болохын тулд
эдгээрийн дараах функцуудыг өдөр тутам ашиглаж сурах хэрэгтэй:
"""

def example_4_advanced_ops():
    print("\n=== 4. Advanced Dictionary & Set Operations ===")
    
    # --- 1. Түлхүүр байхгүй үед алдаа гаргахгүй авах (get) ---
    user = {"name": "Баяраа", "role": "admin"}
    # Алдаа гаргахгүй: get(key, default_value)
    age = user.get("age", 18) 
    print(f"Олдсон нас (default утгатай): {age}")
    
    # --- 2. defaultdict ашиглах ---
    # Хэрэв түлхүүр байхгүй бол автоматаар хоосон жагсаалт, тоо гэх мэт утга онооно
    # collections.defaultdict нь маш хэрэгтэй сан
    grouped_users = defaultdict(list)
    grouped_users["admins"].append("Баяраа")
    grouped_users["admins"].append("Доржоо")
    grouped_users["users"].append("Алимаа")
    print(f"defaultdict ашиглан ангилсан: {dict(grouped_users)}")
    
    # --- 3. Dictionary нэгтгэх (Python 3.9+ 'Merge' оператор '|') ---
    profile = {"name": "Баяраа", "age": 28}
    settings = {"theme": "dark", "age": 29}  # 'age' давхцаж байна
    
    merged = profile | settings  # Баруун талынх нь давамгайлна
    print(f"Нэгтгэсэн dictionary (| оператор): {merged}")
    
    # --- 4. Олонлогийн үйлдлүүд (Set Operations) ---
    # Python-д Set ашиглаж математикийн олонлогийн харьцуулалтыг маш хурдан хийнэ
    frontend_skills = {"HTML", "CSS", "JavaScript", "React"}
    backend_skills = {"Python", "Node.js", "SQL", "JavaScript"}
    
    # А. Огтлолцол (Хоёуланд нь байгаа ур чадвар) - Intersection
    common = frontend_skills & backend_skills # эсвэл .intersection()
    # Б. Нэгдэл (Бүх ур чадварууд давхардалгүй) - Union
    all_skills = frontend_skills | backend_skills # эсвэл .union()
    # В. Ялгавар (Зөвхөн frontend дээр байдаг, backend-д байхгүй) - Difference
    only_frontend = frontend_skills - backend_skills # эсвэл .difference()
    
    print(f"\nFrontend skills: {frontend_skills}")
    print(f"Backend skills:  {backend_skills}")
    print(f"  - Огтлолцол skills (&): {common}")
    print(f"  - Нэгдэл skills (|):    {all_skills}")
    print(f"  - Frontend ялгавар (-): {only_frontend}")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🐍 Pythonic Features — Хичээл 2.3              ║
║  Tech With Tim-ийн зөвлөмжүүд                    ║
║                                                  ║
║  Ямар жишээ ажиллуулах вэ?                      ║
║                                                  ║
║  1. 📝 List, Dict & Set Comprehensions           ║
║  2. ⚡ Generators & Generator Expressions       ║
║  3. ⏳ Context Managers (with оператор)          ║
║  4. 📊 Advanced Dictionary & Set Operations      ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-4): ").strip()
            if choice == "1":
                example_1_comprehensions()
            elif choice == "2":
                example_2_generators()
            elif choice == "3":
                example_3_context_managers()
            elif choice == "4":
                example_4_advanced_ops()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-4 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break
