"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 3.4: Өгөгдлийн Шинжилгээний Төсөл                     ║
║  Бодит датасет дээр дүн шинжилгээ хийж, дүгнэлт гаргах           ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Төслийн зорилго:
   1. Онлайн дэлгүүрийн борлуулалтын датасет (CSV) үүсгэх.
   2. Pandas ашиглан өгөгдлийг цэвэрлэх, баяжуулах (Feature Engineering).
   3. Бизнесийн чухал асуултуудад хариулах (Бүлэглэх, Нэгтгэх).
   4. Үр дүнг графикоор дүрсэлж, тайлан бэлтгэх.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# ============================================================
# 📌 АЛХАМ 1: Жишээ өгөгдөл (Датасет) үүсгэх
# ============================================================
def generate_store_dataset(filename="temp_online_store_sales.csv"):
    """~500 мөр борлуулалтын жишээ өгөгдөл үүсгэх"""
    np.random.seed(42)
    n_records = 500
    
    # Огноо үүсгэх (2025 оны турш)
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n_records)]
    
    # Хэрэглэгчийн мэдээлэл
    customer_ids = np.random.randint(1000, 1150, n_records) # 150 байнгын үйлчлүүлэгч
    ages = np.random.randint(18, 65, n_records)
    genders = np.random.choice(["Male", "Female"], n_records, p=[0.45, 0.55])
    
    # Бүтээгдэхүүн ба үнэ
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Beauty"]
    category_choices = np.random.choice(categories, n_records, p=[0.25, 0.30, 0.20, 0.15, 0.10])
    
    prices = []
    quantities = np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.5, 0.3, 0.1, 0.05, 0.05])
    
    # Ангилал бүрт тохирсон үнийн хязгаар
    price_ranges = {
        "Electronics": (150, 1200),
        "Clothing": (20, 150),
        "Home & Kitchen": (30, 400),
        "Books": (10, 50),
        "Beauty": (15, 120)
    }
    
    for cat in category_choices:
        low, high = price_ranges[cat]
        prices.append(np.round(np.random.uniform(low, high), 2))
        
    prices = np.array(prices)
    
    # Зарим дутуу утга (NaN) зориуд нэмж өгөгдөл цэвэрлэгээ хийх боломж олгох
    # Жишээ нь: 5% цалин/үнэ дутуу, 3% нас дутуу
    prices[np.random.choice(n_records, int(n_records * 0.05), replace=False)] = np.nan
    ages = ages.astype(float)
    ages[np.random.choice(n_records, int(n_records * 0.03), replace=False)] = np.nan
    
    # DataFrame үүсгэх
    df = pd.DataFrame({
        "Transaction_ID": range(5001, 5001 + n_records),
        "Date": [d.strftime("%Y-%m-%d") for d in dates],
        "Customer_ID": customer_ids,
        "Age": ages,
        "Gender": genders,
        "Category": category_choices,
        "Price": prices,
        "Quantity": quantities,
        "Payment_Method": np.random.choice(["Credit Card", "PayPal", "Cash"], n_records)
    })
    
    df.to_csv(filename, index=False)
    print(f"📁 Датасет амжилттай үүсэж, '{filename}' нэрээр хадгалагдлаа. (Нийт: {n_records} мөр)")


# ============================================================
# 📌 АЛХАМ 2: Өгөгдлийг унших & Шалгах
# ============================================================
def load_and_inspect(filename):
    print("\n--- 2. Өгөгдөл унших ба Шалгах ---")
    df = pd.read_csv(filename)
    
    # Эхний 5 мөр
    print("\nЭхний 5 мөр:")
    print(df.head())
    
    # Мэдээлэл шалгах
    print("\nӨгөгдлийн төрлүүд ба хоосон утгууд:")
    print(df.info())
    
    # Статистик мэдээлэл
    print("\nСтатистик тодорхойлолт:")
    print(df.describe())
    
    return df


# ============================================================
# 📌 АЛХАМ 3: Өгөгдөл Цэвэрлэх & Шинэ хувьсагч үүсгэх
# ============================================================
def clean_and_prepare(df):
    print("\n--- 3. Өгөгдөл цэвэрлэх & Feature Engineering ---")
    
    # 1. Огноо баганыг string-ээс datetime төрөлд шилжүүлэх
    df["Date"] = pd.to_datetime(df["Date"])
    
    # 2. Насны баганы дутуу утгыг дундаж насаар дүүргэх
    mean_age = df["Age"].mean()
    df["Age"] = df["Age"].fillna(mean_age).astype(int)
    print(f"  - Дутуу наснуудыг дундаж насаар ({mean_age:.1f}) дүүргэв.")
    
    # 3. Үнийн дутуу утгыг харгалзах ангиллын дундаж үнээр дүүргэх
    # groupby-аар ангилал бүрийн дундаж үнийг олж, fillna хийнэ
    df["Price"] = df.groupby("Category")["Price"].transform(lambda x: x.fillna(x.mean()))
    print("  - Дутуу үнийг тухайн барааны ангиллын дундаж үнээр дүүргэв.")
    
    # 4. Шинэ багана үүсгэх (Нийт зарцуулсан мөнгө: Total_Amount = Price * Quantity)
    df["Total_Amount"] = df["Price"] * df["Quantity"]
    
    # 5. Огнооноос Сар (Month)-ыг салгаж авах
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    
    print("\nЦэвэрлэгээ болон хувиргалтын дараах өгөгдлийн дутуу утга:")
    print(df.isna().sum())
    
    return df


# ============================================================
# 📌 АЛХАМ 4: Дата Анализ (Бизнес Асуултуудад хариулах)
# ============================================================
def perform_analysis(df):
    print("\n--- 4. Бизнес дүн шинжилгээ (EDA) ---")
    
    # Асуулт 1: Нийт борлуулалтын хэмжээ ба дундаж сагс
    total_sales = df["Total_Amount"].sum()
    avg_order = df["Total_Amount"].mean()
    print(f"💰 Нийт борлуулалт: ${total_sales:,.2f}")
    print(f"🛒 Захиалгын дундаж үнэ: ${avg_order:.2f}")
    
    # Асуулт 2: Аль ангилал хамгийн их борлуулалттай байна вэ?
    category_sales = df.groupby("Category")["Total_Amount"].sum().sort_values(ascending=False)
    print("\nАнгилал бүрийн нийт борлуулалт:")
    for cat, val in category_sales.items():
        print(f"  - {cat}: ${val:,.2f}")
        
    # Асуулт 3: Хэрэглэгчдийг хүйс болон төлбөрийн хэлбэрээр ангилах
    gender_sales = df.groupby("Gender")["Total_Amount"].mean()
    payment_counts = df["Payment_Method"].value_counts(normalize=True) * 100
    print("\nХүйсийн дундаж худалдан авалт:")
    print(gender_sales)
    print("\nTөлбөрийн хэлбэрүүдийн хувь хэмжээ:")
    print(payment_counts)
    
    # Асуулт 4: Сар бүрийн борлуулалтын чиг хандлага
    monthly_sales = df.groupby("Month")["Total_Amount"].sum().sort_index()
    
    return category_sales, monthly_sales


# ============================================================
# 📌 АЛХАМ 5: Үр дүнг Зураглах (Visualization)
# ============================================================
def create_visualizations(df, category_sales, monthly_sales):
    print("\n--- 5. Үр дүнг графикоор дүрслэх ---")
    sns.set_theme(style="whitegrid")
    
    # График 1: Ангилал бүрийн борлуулалт (Bar plot)
    plt.figure(figsize=(8, 4))
    sns.barplot(x=category_sales.values, y=category_sales.index, palette="viridis")
    plt.title("Барааны ангилал тус бүрийн нийт борлуулалт ($)", fontsize=13, fontweight="bold")
    plt.xlabel("Борлуулалт ($)")
    plt.ylabel("Ангилал")
    plot_cat_file = "project_sales_by_category.png"
    plt.savefig(plot_cat_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    # График 2: Сар бүрийн борлуулалтын хандлага (Line plot)
    plt.figure(figsize=(10, 4))
    plt.plot(monthly_sales.index, monthly_sales.values, marker="o", color="#e64553", linewidth=2.5)
    plt.title("2025 оны Сар бүрийн борлуулалтын тренд ($)", fontsize=13, fontweight="bold")
    plt.xlabel("Сар")
    plt.ylabel("Борлуулалт ($)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.5)
    plot_trend_file = "project_monthly_trend.png"
    plt.savefig(plot_trend_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    # График 3: Хэрэглэгчдийн насны бүтэц (Histogram)
    plt.figure(figsize=(8, 4))
    sns.histplot(df["Age"], bins=15, kde=True, color="#40a02b")
    plt.title("Үйлчлүүлэгчдийн насны бүтэц (Тархалт)", fontsize=13, fontweight="bold")
    plt.xlabel("Нас")
    plt.ylabel("Давтамж")
    plot_age_file = "project_customer_ages.png"
    plt.savefig(plot_age_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"✅ График 1: '{plot_cat_file}' нэрээр хадгалагдлаа.")
    print(f"✅ График 2: '{plot_trend_file}' нэрээр хадгалагдлаа.")
    print(f"✅ График 3: '{plot_age_file}' нэрээр хадгалагдлаа.")


# ============================================================
# 🎯 ҮНДСЭН АЖИЛЛУУЛАХ ХЭСЭГ
# ============================================================
def main():
    dataset_file = "temp_online_store_sales.csv"
    
    print("🚀 Өгөгдлийн шинжилгээний төсөл эхэллээ...")
    
    # 1. Дата үүсгэх
    generate_store_dataset(dataset_file)
    
    # 2. Дата унших
    df = load_and_inspect(dataset_file)
    
    # 3. Дата цэвэрлэх
    df_clean = clean_and_prepare(df)
    
    # 4. Шинжилгээ
    cat_sales, month_sales = perform_analysis(df_clean)
    
    # 5. График зурах
    create_visualizations(df_clean, cat_sales, month_sales)
    
    # Датасет файлыг устгах (хүсвэл устгахгүй үлдээж болно)
    if os.path.exists(dataset_file):
        os.remove(dataset_file)
        print(f"\n🗑️ Түр ашигласан датасет файл '{dataset_file}' устгагдлаа.")
        
    print("\n🎉 Төсөл амжилттай дууслаа. Бүх үр дүнгийн зураг төслийн хавтсанд үүссэн.")

if __name__ == "__main__":
    main()
