"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 3.1: NumPy — Математик & Шугаман Алгебрийн Үндэс       ║
║  Өгөгдлийн шинжилгээ болон Машин сургалтын тулгуур багана       ║
╚══════════════════════════════════════════════════════════════════╝

🎯 NumPy (Numerical Python) гэж юу вэ?
   - Python-ий стандарт List нь уян хатан боловч маш удаан.
   - NumPy нь C хэл дээр бичигдсэн бөгөөд олон хэмжээст массив (Matrix, Tensor) дээр
     маш хурдан математик үйлдлүүд хийх боломжийг олгодог.
   - ML/AI-ийн цаана байдаг вектор болон матрицын бүх тооцоолол NumPy-аар хийгддэг.

📌 Суулгах заавар (Terminal дээр ажиллуулах):
   pip install numpy
"""

import sys
import time

try:
    import numpy as np
except ImportError:
    print("""
⚠️  NumPy суугаагүй байна!
Дараах тушаалаар суулгаж болно:
    pip install numpy
    """)
    # Туршилт хийхийн тулд mock хийх эсвэл шууд зогсоох
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: NumPy Array vs Python List (Хурдны харьцуулалт)
# ============================================================
"""
NumPy массив (ndarray) нь:
1. Нэг төрлийн (homogeneous) өгөгдөл хадгалдаг (бүгд float эсвэл int).
2. Санах ойд дараалсан байдлаар байрладаг тул хурдан.
3. Векторчлол (Vectorization) дэмждэг тул давталт (for loop) ашиглахгүйгээр шууд тооцоолол хийдэг.
"""

def example_1_speed_comparison():
    print("\n=== 1. NumPy Array vs Python List (Хурдны тест) ===")
    
    size = 1000000
    
    # Сонгодог Python List үүсгэх
    list1 = list(range(size))
    list2 = list(range(size))
    
    # NumPy Array үүсгэх
    arr1 = np.arange(size)
    arr2 = np.arange(size)
    
    # А. Python List дээр гишүүн тус бүрийг нэмэх (for loop)
    start_time = time.time()
    list_result = [list1[i] + list2[i] for i in range(size)]
    list_time = time.time() - start_time
    
    # Б. NumPy Array дээр нэмэх (Векторчлол)
    start_time = time.time()
    arr_result = arr1 + arr2  # Хэчнээн энгийн!
    arr_time = time.time() - start_time
    
    print(f"1 сая элементийг нэмэх хугацаа:")
    print(f"  - Python List (for loop): {list_time:.5f} секунд")
    print(f"  - NumPy Array (+):         {arr_time:.5f} секунд")
    print(f"🚀 NumPy нь Python list-ээс {list_time / arr_time:.1f} дахин хурдан ажиллалаа!")


# ============================================================
# 📌 ХЭСЭГ 2: Массив үүсгэх аргууд & Хэлбэр (Shape, Reshape)
# ============================================================

def example_2_creating_arrays():
    print("\n=== 2. Массив үүсгэх & Хэлбэрийг өөрчлөх ===")
    
    # 1. Листээс массив үүсгэх
    arr_1d = np.array([1, 2, 3, 4])
    print(f"1D Массив (Вектор): {arr_1d}, Хэмжээс (ndim): {arr_1d.ndim}, Хэлбэр (shape): {arr_1d.shape}")
    
    # 2. Олон хэмжээст массив (Матриц)
    arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\n2D Массив (Матриц 2x3):\n{arr_2d}")
    print(f"Хэлбэр (shape): {arr_2d.shape}, Өгөгдлийн төрөл (dtype): {arr_2d.dtype}")
    
    # 3. Тусгай массив үүсгэх аргууд
    zeros = np.zeros((2, 4)) # Бүгд 0 утгатай 2x4 матриц
    ones = np.ones((3, 3))   # Бүгд 1 утгатай 3x3 матриц
    identity = np.eye(3)     # 3x3 Нэгж матриц (Диагональ нь 1, бусад нь 0)
    arange = np.arange(0, 10, 2) # [0, 2, 4, 6, 8]
    linspace = np.linspace(0, 1, 5) # [0.0, 0.25, 0.5, 0.75, 1.0] (Тэнцүү хуваах)
    
    print(f"\nZeros (2x4):\n{zeros}")
    print(f"\nIdentity matrix (3x3):\n{identity}")
    print(f"\nLinspace (0-1 хооронд 5 хуваах): {linspace}")
    
    # 4. Хэлбэрийг өөрчлөх (Reshape)
    # Машин сургалтанд өгөгдлийн хэлбэрийг тохируулахад байнга хэрэглэгддэг
    original = np.arange(12)  # 0-оос 11 хүртэл тоо
    reshaped = original.reshape(3, 4)  # 3 мөр, 4 багана бүхий 2D матриц болгох
    print(f"\nOriginal (1D): {original}")
    print(f"Reshaped (3x4 2D):\n{reshaped}")


# ============================================================
# 📌 ХЭСЭГ 3: Индексжүүлэлт & Зүсэлт (Indexing & Slicing)
# ============================================================
"""
NumPy-д олон хэмжээст массивыг хялбархан зүсэж (slice) авч болдог.
Загвар: matrix[row_slice, col_slice]
"""

def example_3_indexing_slicing():
    print("\n=== 3. Индексжүүлэлт & Зүсэлт (Slicing) ===")
    
    matrix = np.array([
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        [30, 31, 32, 33]
    ])
    print(f"Эх матриц:\n{matrix}")
    
    # Тодорхой элемент авах (мөр 1, багана 2 -> 22)
    # 0-ээс эхэлж тоолно
    print(f"\nМөр 1, Багана 2-ын элемент: {matrix[1, 2]}")
    
    # Тодорхой мөр авах (Мөр 0)
    print(f"Зөвхөн 0-р мөр: {matrix[0, :]}")
    
    # Тодорхой багана авах (Багана 3)
    print(f"Зөвхөн 3-р багана: {matrix[:, 3]}")
    
    # Дэд матриц зүсэж авах (Эхний 2 мөр, Багана 1 болон 2)
    sub_matrix = matrix[0:2, 1:3]
    print(f"Дэд матриц (0:2 мөр, 1:3 багана):\n{sub_matrix}")
    
    # Нөхцөлт шүүлт (Boolean Indexing) - Өгөгдөл шүүхэд маш хэрэгтэй
    arr = np.array([1, 5, 8, 12, 3, 15, 7])
    mask = arr > 7
    print(f"\nШүүх нөхцөл (arr > 7): {mask}")
    print(f"Шүүгдсэн массив: {arr[mask]}")


# ============================================================
# 📌 ХЭСЭГ 4: Математик үйлдлүүд & Статистик нэгтгэлүүд
# ============================================================

def example_4_math_ops():
    print("\n=== 4. Математик & Статистик үйлдлүүд ===")
    
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # 1. Element-wise үйлдлүүд (Гишүүн тус бүрээр)
    print(f"a: {a}, b: {b}")
    print(f"Нэмэх (a + b):  {a + b}")
    print(f"Үржих (a * b):  {a * b}")
    print(f"Зэрэгт дэвшүүлэх (a ** 2): {a ** 2}")
    
    # 2. Статистик функцүүд
    data = np.array([[1, 2], [3, 4]])
    print(f"\nӨгөгдөл матриц:\n{data}")
    print(f"Нийт нийлбэр (sum): {data.sum()}")
    print(f"Мөр дагуух нийлбэр (axis=1): {data.sum(axis=1)}")
    print(f"Багана дагуух нийлбэр (axis=0): {data.sum(axis=0)}")
    print(f"Дундаж (mean): {data.mean()}")
    print(f"Стандарт хазайлт (std): {data.std():.4f}")
    
    # 3. Матрицын үржвэр (Dot Product)
    # Машин сургалтын шугаман тэгшитгэлд хамгийн чухал үйлдэл
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    # 2 аргаар үржүүлж болно:
    dot_product = np.dot(A, B)
    matmul_operator = A @ B  # Python 3.5+ '@' оператор
    
    print(f"\nМатриц A:\n{A}")
    print(f"Матриц B:\n{B}")
    print(f"Матрицын үржвэр A @ B:\n{matmul_operator}")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  📊 NumPy Үндэс — Хичээл 3.1                     ║
║                                                  ║
║  Ямар сэдвийг ажиллуулж үзэх вэ?                 ║
║                                                  ║
║  1. ⚡ NumPy Array vs Python List (Хурдны тест)    ║
║  2. 📐 Массив үүсгэх & Хэлбэр өөрчлөх (Reshape)   ║
║  3. 🔪 Индексжүүлэлт & Зүсэлт (Slicing)           ║
║  4. 🧮 Математик & Матрицын үржвэр (@)            ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-4): ").strip()
            if choice == "1":
                example_1_speed_comparison()
            elif choice == "2":
                example_2_creating_arrays()
            elif choice == "3":
                example_3_indexing_slicing()
            elif choice == "4":
                example_4_math_ops()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-4 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break
