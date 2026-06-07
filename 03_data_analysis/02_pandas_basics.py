"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 3.2: Pandas — Өгөгдлийн Хүснэгттэй Ажиллах            ║
║  Data Science-ийн өдөр тутмын хамгийн гол хэрэгсэл               ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Pandas гэж юу вэ?
   - Өгөгдлийг Excel, SQL хүснэгт шиг хэлбэртэйгээр (DataFrame) уншиж, боловсруулж,
     шинжилдэг Python-ий хамгийн алдартай сан.
   - Өгөгдлийг цэвэрлэх (data cleaning), шүүх (filtering), нэгтгэх (aggregation)
     үйлдлүүдийг маш хялбар кодоор гүйцэтгэнэ.

📌 Суулгах заавар (Terminal дээр ажиллуулах):
   pip install pandas
"""

import sys
import os

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("""
⚠️  Pandas эсвэл NumPy суугаагүй байна!
Дараах тушаалаар суулгана уу:
    pip install pandas numpy
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: Series & DataFrame үүсгэх
# ============================================================
"""
Pandas-ийн 2 гол бүтэц:
1. Series: Нэг хэмжээст массив (Хүснэгтийн нэг багана эсвэл Excel-ийн нэг мөр)
2. DataFrame: Хоёр хэмжээст хүснэгт (Бүхэл бүтэн Excel хуудас эсвэл SQL Table)
"""

def example_1_series_dataframe():
    print("\n=== 1. Series & DataFrame Үндсэн ойлголт ===")
    
    # 1. Series үүсгэх (индекстэй цуваа)
    ages = pd.Series([25, 30, 35, 40], name="Нас")
    print("Энгийн Series:")
    print(ages)
    
    # 2. Dictionary-оос DataFrame үүсгэх (JS-ийн array of objects шиг)
    data = {
        "Нэр": ["Баяраа", "Доржоо", "Алимаа", "Цэцгээ"],
        "Нас": [28, 34, 22, 29],
        "Хот": ["Улаанбаатар", "Эрдэнэт", "Улаанбаатар", "Дархан"],
        "Цалин": [1500000, 2200000, 1200000, 1800000]
    }
    
    df = pd.DataFrame(data)
    print("\nЭнгийн DataFrame (Хүснэгт):")
    print(df)
    
    # DataFrame-ийн мэдээллийг харах
    print(f"\nХүснэгтийн хэлбэр (Shape): {df.shape} (мөр, багана)")
    print("\nБагануудын нэрс:", df.columns.tolist())


# ============================================================
# 📌 ХЭСЭГ 2: Өгөгдөл унших, Хадгалах (CSV файлтай ажиллах)
# ============================================================

def create_sample_csv(filename):
    """Жишээ өгөгдөл бүхий CSV файл үүсгэх туслах функц"""
    data = """id,name,department,salary,join_date,is_remote
101,Bayaraa,IT,2500000,2022-03-15,True
102,Dorj,Sales,1800000,2021-06-20,False
103,Alimaa,IT,,2023-01-10,True
104,Tsetseg,HR,1500000,2020-11-01,False
105,Bold,Sales,2100000,,False
106,Saraa,IT,3000000,2019-05-18,True
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


def example_2_csv_handling():
    print("\n=== 2. CSV Файл унших & Хадгалах ===")
    
    filename = "temp_employees.csv"
    create_sample_csv(filename)
    
    # 1. CSV файлаас унших
    # Pandas нь файлаас уншихдаа автоматаар DataFrame болгож хувиргана
    df = pd.read_csv(filename)
    print("Файлаас уншсан өгөгдөл:")
    print(df)
    
    # 2. Өгөгдлийг шүүж шинэ файл болгон хадгалах
    # Зөвхөн IT-ийн ажилтнуудыг сонгох
    it_employees = df[df["department"] == "IT"]
    
    output_file = "temp_it_employees.csv"
    # index=False нь мөрийн дугаарыг CSV рүү хадгалахгүй
    it_employees.to_csv(output_file, index=False)
    print(f"\nIT ажилтнуудын өгөгдлийг '{output_file}' файл руу хадгаллаа.")
    
    # Цэвэрлэгээ
    if os.path.exists(filename): os.remove(filename)
    if os.path.exists(output_file): os.remove(output_file)


# ============================================================
# 📌 ХЭСЭГ 3: Өгөгдөл цэвэрлэх & Шүүх (Data Cleaning & Filtering)
# ============================================================
"""
Бодит амьдрал дээрх өгөгдөл маш их бохир (хоосон нүдтэй, буруу бичилттэй) байдаг.
Pandas нь эдгээр дутуу утгыг (NaN / Null) маш хялбар удирддаг.
"""

def example_3_data_cleaning():
    print("\n=== 3. Өгөгдөл цэвэрлэх & Шүүх ===")
    
    filename = "temp_employees_cleaning.csv"
    create_sample_csv(filename)
    df = pd.read_csv(filename)
    
    # 1. Өгөгдлийн ерөнхий мэдээллийг шалгах
    print("Багануудын дутуу утга байгаа эсэхийг харах:")
    print(df.isna().sum()) # Багана бүр дэх хоосон нүдний тоо
    
    # 2. Дутуу утгыг дүүргэх (fillna)
    # Цалин нь дутуу ажилтны цалинг IT хэлтсийн дундаж цалингаар дүүргэх (эсвэл нийт дунджаар)
    mean_salary = df["salary"].mean()
    df["salary"] = df["salary"].fillna(mean_salary)
    print(f"\nЦалинг дундаж цалингаар ({mean_salary:.0f}) дүүргэв:")
    print(df[["name", "salary"]])
    
    # 3. Дутуу утгатай мөрийг устгах (dropna)
    # Огноо (join_date) дутуу ажилтны мөрийг хасах
    cleaned_df = df.dropna(subset=["join_date"])
    print("\nОгноо нь дутуу мөрийг хассан үр дүн:")
    print(cleaned_df)
    
    # 4. Шүүлт (Filtering)
    # Цалин нь 2,000,000-аас их бөгөөд Remote ажилладаг хүмүүс
    high_pay_remote = df[(df["salary"] > 2000000) & (df["is_remote"] == True)]
    print("\nШүүгдсэн өгөгдөл (Цалин > 2M ба Remote):")
    print(high_pay_remote)
    
    # Цэвэрлэгээ
    if os.path.exists(filename): os.remove(filename)


# ============================================================
# 📌 ХЭСЭГ 4: Бүлэглэлт & Нэгтгэлт (Groupby & Aggregation)
# ============================================================
"""
💡 SQL-ийн "GROUP BY" үйлдлийг Pandas-т маш хялбар хийнэ.
Жишээлбэл, хэлтэс бүрээр цалингийн дунджийг бодох:
"""

def example_4_groupby():
    print("\n=== 4. Groupby & Aggregation (Өгөгдөл бүлэглэх) ===")
    
    filename = "temp_employees_groupby.csv"
    create_sample_csv(filename)
    df = pd.read_csv(filename)
    
    # Дутуу цалинг 0-ээр дүүргэе
    df["salary"] = df["salary"].fillna(0)
    
    # 1. Хэлтэс бүрээр бүлэглэж, ажилтны тоо болон дундаж цалинг олох
    # SQL: SELECT department, COUNT(*), AVG(salary) FROM employees GROUP BY department;
    grouped = df.groupby("department").agg(
        ажилтны_тоо=("name", "count"),
        дундаж_цалин=("salary", "mean")
    )
    
    print("Хэлтэс бүрийн ажилтны тоо ба дундаж цалин:")
    print(grouped)
    
    # 2. Remote болон Оффисоос ажилладаг хүмүүсийн нийт цалин
    remote_stats = df.groupby("is_remote")["salary"].sum()
    print("\nRemote болон Оффис ажилтнуудын нийт цалингийн сан:")
    print(remote_stats)
    
    # Цэвэрлэгээ
    if os.path.exists(filename): os.remove(filename)


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🐼 Pandas Үндэс — Хичээл 3.2                     ║
║                                                  ║
║  Ямар сэдвийг ажиллуулж үзэх вэ?                 ║
║                                                  ║
║  1. 📊 Series & DataFrame (Үндсэн бүтэц)         ║
║  2. 📂 CSV файлтай ажиллах (Унших/Хадгалах)      ║
║  3. 🧼 Өгөгдөл цэвэрлэх & Шүүх (Data Cleaning)   ║
║  4. 📈 Groupby & Aggregation (Бүлэглэх)          ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-4): ").strip()
            if choice == "1":
                example_1_series_dataframe()
            elif choice == "2":
                example_2_csv_handling()
            elif choice == "3":
                example_3_data_cleaning()
            elif choice == "4":
                example_4_groupby()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-4 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break
