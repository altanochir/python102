"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 3.3: Matplotlib & Seaborn — Өгөгдлийг Зураглах          ║
║  Өгөгдлийг ойлгох хамгийн хурдан арга бол дүрслэл (Plots)       ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Яагаад Data Visualization чухал вэ?
   - Өгөгдлийн хамаарал, тархалт, алдаатай утгуудыг нүдээр харахад тусална.
   - Машин сургалтын үр дүн, түүний алдааг зураглахад байнга хэрэглэдэг.
   - Matplotlib нь суурь сан, Seaborn нь түүн дээр суурилсан илүү үзэмжтэй статик график зурдаг сан юм.

📌 Суулгах заавар (Terminal дээр ажиллуулах):
   pip install matplotlib seaborn pandas numpy
"""

import sys
import os

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
except ImportError:
    print("""
⚠️  Шаардлагатай сангууд суугаагүй байна!
Дараах тушаалаар суулгана уу:
    pip install matplotlib seaborn pandas numpy
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: Matplotlib - Шугаман ба Баганан график (Line & Bar)
# ============================================================

def example_1_matplotlib_basics():
    print("\n=== 1. Matplotlib Үндсэн графикууд (Файлаар хадгалах) ===")
    
    # Жишээ өгөгдөл: Сүүлийн 6 сарын борлуулалт
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales_a = [120, 150, 140, 180, 220, 210]
    sales_b = [90, 110, 130, 150, 170, 200]
    
    # 1. Шинэ зураг үүсгэх (өргөн x өндөр инчээр)
    plt.figure(figsize=(10, 5))
    
    # 2. Шугам зурах
    # label нь тайлбарт (legend) ашиглагдана
    plt.plot(months, sales_a, marker="o", color="#89b4fa", linewidth=2.5, label="Бүтээгдэхүүн А")
    plt.plot(months, sales_b, marker="s", color="#f38ba8", linewidth=2, linestyle="--", label="Бүтээгдэхүүн Б")
    
    # 3. Графикийн гарчиг, тэнхлэгийн нэрс
    plt.title("Сар бүрийн борлуулалтын харьцуулалт 📈", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Сар", fontsize=11)
    plt.ylabel("Борлуулалт (Сая ₮)", fontsize=11)
    
    # 4. Тайлбар (Legend) болон Grid (хэрчих шугам) харуулах
    plt.legend(loc="upper left")
    plt.grid(True, linestyle=":", alpha=0.6)
    
    # 5. Графикийг файл болгож хадгалах (маш чухал!)
    # Терминал дээр шууд зураг харуулах боломжгүй эсвэл хүндрэлтэй үед файл болгож хадгалдаг
    output_filename = "sales_plot.png"
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close() # Зургийн санах ойг цэвэрлэх
    
    print(f"✅ Шугаман график амжилттай үүсэж, '{output_filename}' нэрээр хадгалагдлаа.")


# ============================================================
# 📌 ХЭСЭГ 2: Seaborn - Өгөгдлийн тархалт харах (Histplot & Boxplot)
# ============================================================
"""
Seaborn нь өгөгдлийн тархалтыг (distribution) харахад маш тохиромжтой.
- Histplot (Гистограмм): Тоонууд ямар хэсэгт илүү бөөгнөрч байгааг харуулна.
- Boxplot: Дундаж утга болон хэт их/бага байгаа гажуудал (Outliers)-ыг илрүүлнэ.
"""

def example_2_distribution_plots():
    print("\n=== 2. Seaborn - Тархалт & Гажуудал харах ===")
    
    # Жишээ өгөгдөл: 200 хүний цалингийн хэмжээ (Санамсаргүй өгөгдөл)
    # Зүүн тийш хазайсан хэвийн бус тархалт үүсгэх
    np.random.seed(42)
    salaries = np.random.normal(loc=1.8, scale=0.5, size=200) # Дундаж 1.8M, стандарт хазайлт 0.5M
    # Зарим нэг маш өндөр цалин нэмэх (Outliers)
    salaries = np.append(salaries, [4.5, 4.8, 5.2])
    
    df = pd.DataFrame({"Salary": salaries})
    
    # Зургийн загварыг Seaborn-оор тохируулах
    sns.set_theme(style="whitegrid")
    
    # А. Histplot
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x="Salary", kde=True, color="#89b4fa", bins=20)
    plt.title("Ажилтнуудын цалингийн тархалт (Гистограмм)", fontsize=12)
    plt.xlabel("Цалин (Сая ₮)")
    plt.ylabel("Хүний тоо")
    
    hist_file = "salary_distribution.png"
    plt.savefig(hist_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    # Б. Boxplot (Хайрцаг график)
    plt.figure(figsize=(8, 3))
    sns.boxplot(data=df, x="Salary", color="#a6e3a1")
    plt.title("Ажилтнуудын цалингийн хайрцаг график (Outliers харах)", fontsize=12)
    plt.xlabel("Цалин (Сая ₮)")
    
    box_file = "salary_boxplot.png"
    plt.savefig(box_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"✅ Тархалтын график '{hist_file}' нэрээр хадгалагдлаа.")
    print(f"✅ Boxplot график '{box_file}' нэрээр хадгалагдлаа. (Баруун талын цэгүүд бол Outliers юм!)")


# ============================================================
# 📌 ХЭСЭГ 3: Хамаарлын матриц (Correlation Heatmap)
# ============================================================
"""
Машин сургалтын модельд өгөх шинж чанарууд (features) хоорондоо хэр зэрэг хамааралтай байгааг
шалгахдаа "Correlation Matrix Heatmap"-ийг үргэлж ашигладаг.
Хэмжигдэхүүн: -1-ээс 1 хооронд байна (1 = шууд хамааралтай, 0 = хамааралгүй).
"""

def example_3_correlation_heatmap():
    print("\n=== 3. Хамаарлын матриц (Correlation Heatmap) ===")
    
    # Өгөгдөл үүсгэх
    np.random.seed(10)
    n = 100
    studying_hours = np.random.uniform(2, 10, n)  # 2-оос 10 цаг хичээллэдэг
    sleep_hours = 12 - studying_hours + np.random.normal(0, 0.5, n) # Хичээл их хийвэл бага унтана (сөрөг хамаарал)
    exam_score = studying_hours * 8 + sleep_hours * 2 + np.random.normal(0, 5, n) # Эерэг хамаарал
    coffee_cups = np.random.randint(0, 5, n) # Хамааралгүй
    
    df = pd.DataFrame({
        "Study_Hours": studying_hours,
        "Sleep_Hours": sleep_hours,
        "Coffee_Cups": coffee_cups,
        "Exam_Score": exam_score
    })
    
    # Хамаарлын коэффициентыг бодох
    corr_matrix = df.corr()
    
    print("Хамаарлын матриц (Тоон хэлбэрээр):")
    print(corr_matrix.round(2))
    
    # Heatmap дүрслэл
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        corr_matrix, 
        annot=True,          # Тоонуудыг нүдэн дотор нь бичих
        cmap="coolwarm",     # Өнгөний сонголт (хүйтэнээс халуун)
        vmin=-1, vmax=1,     # Хязгаар
        linewidths=0.5,
        fmt=".2f"
    )
    plt.title("Ажиглалтуудын хамаарлын Heatmap 🌡️", pad=15)
    
    heatmap_file = "correlation_heatmap.png"
    plt.savefig(heatmap_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"\n✅ Heatmap график '{heatmap_file}' нэрээр хадгалагдлаа.")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🎨 Өгөгдөл Дүрслэл — Хичээл 3.3                  ║
║                                                  ║
║  Ямар сэдвийг ажиллуулж үзэх вэ?                 ║
║  (Үүссэн графикууд төслийн хавтаст хадгалагдана)  ║
║                                                  ║
║  1. 📈 Шугаман график (Matplotlib Basics)        ║
║  2. 📊 Тархалт & Хайрцаг график (Seaborn Basics)  ║
║  3. 🌡️ Хамаарлын Heatmap (Feature Correlation)   ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-3): ").strip()
            if choice == "1":
                example_1_matplotlib_basics()
            elif choice == "2":
                example_2_distribution_plots()
            elif choice == "3":
                example_3_correlation_heatmap()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-3 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break
