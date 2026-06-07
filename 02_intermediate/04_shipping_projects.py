"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 2.4: Төслөө Дэлгэх (Shipping & Deploying Projects)     ║
║  Tech With Tim-ийн зөвлөмж: Профессионал хөгжүүлэгчийн дадал     ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Virtual Environments (venv) & requirements.txt
   2. Төслийн бүтэц (Project Architecture)
   3. Git & GitHub (Хувилбар удирдах систем)
   4. Desktop App-ийг EXE болгон багцлах (PyInstaller)
   5. Web App байршуулах (Render, Railway гэх мэт)
"""

import os
import sys
import subprocess

def show_venv_info():
    print("\n=== 1. Virtual Environments (venv) & Багц удирдах ===")
    print("""
💡 Хэрэв та Node.js дээр ажиллаж байсан бол төсөл бүр өөрийн 'node_modules'-той байдаг.
Python-д үүнийг 'Virtual Environment' (venv) гэж нэрлэдэг.

Яагаад venv хэрэгтэй вэ?
- Төсөл бүрийн сангууд (dependencies) хоорондоо зөрчилдөхөөс сэргийлнэ.
- Global орчинд зөвхөн Python өөрөө байх ба төслийн сангуудыг тусад нь суулгана.

📌 Үндсэн командууд (Terminal дээр ажиллуулна):
1. Venv үүсгэх:
   python -m venv .venv

2. Venv-ийг идэвхжүүлэх:
   - Windows (PowerShell):   .\\.venv\\Scripts\\Activate.ps1
   - Windows (CMD):          .\\.venv\\Scripts\\activate.bat
   - Mac/Linux:              source .venv/bin/activate

3. Багц суулгах:
   pip install <багцын_нэр>

4. Суулгасан багцуудыг жагсаалт болгон хадгалах (Node.js-ийн package.json шиг):
   pip freeze > requirements.txt

5. Өөр компьютер дээр багцуудыг нэг дор суулгах:
   pip install -r requirements.txt
    """)
    
    # Одоогийн ажиллаж байгаа Python venv дотор байгаа эсэхийг харуулах
    in_venv = sys.prefix != sys.base_prefix
    print(f"👉 Таны одоогийн орчин: {'🟢 VIRTUAL ENVIRONMENT дотор байна' if in_venv else '🔴 GLOBAL орчин байна'}")
    print(f"👉 Python ажиллаж буй зам: {sys.executable}")


def show_project_structure():
    print("\n=== 2. Төслийн стандарт бүтэц (Project Structure) ===")
    print("""
Жижиг биш дунд/том хэмжээний Python төсөл бичихэд дараах бүтэцтэй байх нь тохиромжтой:

my_project/
│
├── .venv/                  # Virtual environment (git-д оруулахгүй)
├── .gitignore              # Git-д орохгүй файлуудын жагсаалт (жишээ нь: .venv, __pycache__)
├── requirements.txt        # Төслийн хамаарлууд (dependencies)
├── README.md               # Төслийн тайлбар, хэрхэн ажиллуулах заавар
├── pyproject.toml          # Төслийн мета өгөгдөл, тохиргоо (орчин үеийн стандарт)
│
├── src/                    # Төслийн эх код байрлах хавтас
│   ├── __init__.py         # Хавтсыг package болгох файл
│   ├── main.py             # Үндсэн орох цэг
│   └── utils.py            # Туслах функцүүд
│
└── tests/                  # Автомат тестүүд
    ├── __init__.py
    └── test_utils.py

💡 Tech With Tim-ийн зөвлөгөө: "Төслөө анхнаас нь цэгцтэй зохион байгуулж сур. Энэ нь таныг сайн программист гэдгийг харуулна."
    """)


def show_git_commands():
    print("\n=== 3. Git & GitHub (Хувилбар удирдах систем) ===")
    print("""
💡 "Бичсэн кодоо зөвхөн компьютер дээрээ хадгалаад орхих нь хөгжүүлэгчийн хамгийн том алдаа" - Tech With Tim.
GitHub дээр төслөө байршуулах нь ажлын байранд очих гол багц (portfolio) болдог.

📌 Git-ийн үндсэн ажлын урсгал:

1. Төсөлдөө git үүсгэх:
   git init

2. Өөрчлөлтийг тэмдэглэх (Stage):
   git add .

3. Өөрчлөлтийг бүртгэх (Commit):
   git commit -m "Initial commit - Created GUI calculator"

4. Алсын сервер (GitHub)-тэй холбох:
   git remote add origin <GitHub_URL>

5. Кодоо сервер лүү илгээх (Push):
   git push -u origin main

💡 Чухал санамж: '.gitignore' файл үүсгэж, дотор нь '.venv/', '__pycache__/', '*.pyc' гэж бичээд git-д оруулахаас сэргийлнэ!
    """)


def explain_packaging():
    print("\n=== 4. Desktop App-ийг EXE болгон багцлах (PyInstaller) ===")
    print("""
Хэрэв та Tkinter-ээр бичсэн тооны машин (calculator.py)-аа өөр хүнд (компьютер дээр нь Python суугаагүй хүнд)
өгч ажиллуулахыг хүсвэл .exe (Windows) эсвэл .app (Mac) файл болгон багцалж болно.

Үүнд 'pyinstaller' багцыг ашиглана:

1. PyInstaller суулгах:
   pip install pyinstaller

2. Энгийнээр EXE үүсгэх:
   pyinstaller calculator.py

3. Зөвхөн ганц файл болгох (нэмэлт фолдер үүсгэхгүй):
   pyinstaller --onefile calculator.py

4. Цонхтой програмд зориулж terminal нээгдэхээс сэргийлэх (--noconsole):
   pyinstaller --onefile --windowed calculator.py

💡 Үүний дараа төслийн хавтсанд 'dist/' гэдэг хавтас үүсэх ба дотор нь таны 'calculator.exe' файл бэлэн болно!
    """)


def explain_web_deployment():
    print("\n=== 5. Web App & API байршуулах (Deployment) ===")
    print("""
Хэрэв та Python дээр Вэб аппликейшн (FastAPI, Flask, Django) хийсэн бол үүнийг үнэгүй серверүүд дээр хурдан байршуулж болно:

🟢 Render (render.com):
   - GitHub хаягтайгаа холбоод, FastAPI / Flask төслөө шууд үнэгүй асааж болно.
   - Ажиллуулах тушаал: uvicorn main:app --host 0.0.0.0 --port $PORT

🟡 Railway (railway.app):
   - Dockerfile эсвэл python buildpack ашиглан маш хурдан деплой хийдэг.
   - Өгөгдлийн сан (PostgreSQL, Redis)-тай холбоход маш хялбар.

🔵 Hugging Face Spaces / Streamlit Community Cloud:
   - Хэрэв та AI/ML, Data Science аппликейшн (Streamlit, Gradio) хийсэн бол эдгээр платформ дээр үнэгүй байршуулахад хамгийн тохиромжтой.
    """)


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  📦 Төслөө Дэлгэх — Хичээл 2.4                    ║
║  Python төслийг хэрхэн бэлтгэж, байршуулах вэ?    ║
║                                                  ║
║  Ямар сэдвийг үзэх вэ?                           ║
║                                                  ║
║  1. 🟢 Virtual Environments (venv) & pip         ║
║  2. 📂 Төслийн бүтэц (Project Structure)         ║
║  3. 🐙 Git & GitHub ажлын урсгал                 ║
║  4. 💻 App-ийг EXE болгож багцлах (PyInstaller)  ║
║  5. 🌐 Web App деплой хийх (Render, Railway)     ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-5): ").strip()
            if choice == "1":
                show_venv_info()
            elif choice == "2":
                show_project_structure()
            elif choice == "3":
                show_git_commands()
            elif choice == "4":
                explain_packaging()
            elif choice == "5":
                explain_web_deployment()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-5 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break
