# 🐍 Python 102: Python Хэлийг Алхам Алхмаар Сурах Бүрэн Хөтөч

Энэхүү хадгалах сан (repository) нь Python хэлийг анхан шатнаас эхлэн ахисан шатны сэдвүүд (өгөгдлийн шинжилгээ, тоглоом хөгжүүлэлт, машин сургалт) хүртэл Монгол хэл дээр практик жишээ, дасгал ажлын хамтаар сурахад зориулагдсан цогц гарын авлага юм.

Ялангуяа **JavaScript (Node.js)** болон **Visual Basic** гэх мэт өөр програмчлалын хэлний туршлагатай хөгжүүлэгчдэд зориулж синтаксын болон концепцийн харьцуулсан тайлбаруудыг оруулснаараа онцлогтой.

---

## 📂 Төслийн Бүтэц ба Сэдвүүд

Сургалтын хөтөлбөр нь дараах 5 үндсэн хэсэгт хуваагдана:

| Хавтас / Файл | Сэдэв | Зорилтот түвшин / Хамрах хүрээ |
| :--- | :--- | :--- |
| [📁 01_basics](file:///c:/work/python102/01_basics) | **Python-ий Суурь Ойлголтууд** | Орчин бэлдэх, хувьсагч, өгөгдлийн бүтэц, нөхцөл шалгах, функц, объект хандалтат програмчлал (OOP). JS хөгжүүлэгчдэд тусгайлан зориулсан. |
| [📁 02_intermediate](file:///c:/work/python102/02_intermediate) | **Дунд шат & GUI Хөгжүүлэлт** | `Tkinter` сан ашиглан Desktop цонхтой програм хийх (Layout, Events, Dialogs). Visual Basic туршлагатай хүмүүстэй харьцуулсан. |
| [📁 03_data_analysis](file:///c:/work/python102/03_data_analysis) | **Өгөгдлийн Шинжилгээ** | `NumPy` (математик, матриц), `Pandas` (өгөгдлийн хүснэгт), `Matplotlib/Seaborn` (өгөгдлийн дүрслэл, график). |
| [📁 04_game_dev](file:///c:/work/python102/04_game_dev) | **Тоглоом Хөгжүүлэлт** | `Pygame` ашиглан 2D тоглоомууд (Pong, Snake, Space Invaders, Tetris, Chess, Platformer) хийх арга зүй. |
| [📁 05_machine_learning](file:///c:/work/python102/05_machine_learning) | **Машин Сургалт (ML/AI)** | Шугаман регресс, хиймэл мэдрэлийн сүлжээ, `TensorFlow` болон `PyTorch` сангуудын суурь ойлголтууд. |
| [📄 calculator.py](file:///c:/work/python102/calculator.py) | **Бодит Төсөл** | `Tkinter` ашиглан бичсэн бүрэн ажиллагаатай тооны машин (Calculator). |

---

## 🚀 Алхам Алхмаар Суралцах Заавар (Step-by-Step Guide)

Python хэлийг хамгийн үр дүнтэй сурахын тулд дараах дарааллын дагуу судална уу:

### 1-р Алхам: Орчин Бэлдэх & Эхлэл
Хамгийн эхлээд өөрийн компьютер дээр Python болон код засварлагч (VS Code гэх мэт) суулгасан байх шаардлагатай.

1. **Python татах**: [python.org](https://www.python.org/downloads/) руу орж суулгана. Суулгах явцад **"Add Python to PATH"** сонголтыг заавал чагтална уу.
2. **Төслийн хавтаст орох**: Терминал (Terminal / PowerShell / Command Prompt) нээнэ.
3. **Виртуал Орчин үүсгэх (venv)**: Төсөл бүр өөр өөр сангуудын хувилбар ашиглах тул тусгаарлагдсан орчин бэлдэнэ.
   ```powershell
   python -m venv venv
   ```
4. **Виртуал орчныг идэвхжүүлэх**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **Mac / Linux**:
     ```bash
     source venv/bin/activate
     ```
   *(Идэвхжсэний дараа терминалын урд `(venv)` гэж бичигдэх болно)*

---

### 2-р Алхам: Суурь Шатны Хичээлүүд (`01_basics`)
Энэ хэсэг нь JavaScript болон бусад хөгжүүлэгчдэд зориулсан тул синтаксын ялгаануудыг маш тодорхой харуулсан. Хичээлүүдийг дарааллын дагуу уншиж, файл бүрийг ажиллуулж үзээрэй.

1. [01_hello.py](file:///c:/work/python102/01_basics/01_hello.py) - Синтаксын онцлог (хаалтгүй, индент/зай ашиглах), хувьсагч зарлахгүй байх, `pip` пакеж менежер болон `venv` идэвхжүүлэх.
2. [02_variables.py](file:///c:/work/python102/01_basics/02_variables.py) - Өгөгдлийн төрлүүд (Number, String, Boolean), хөрвүүлэлтүүд, dynamic typing.
3. [03_data_structures.py](file:///c:/work/python102/01_basics/03_data_structures.py) - Массив ба жагсаалтууд (List, Tuple, Set, Dictionary). JS Array болон Object-той харьцуулсан нь.
4. [04_control_flow.py](file:///c:/work/python102/01_basics/04_control_flow.py) - Нөхцөл шалгах (`if-elif-else`), давталтууд (`for`, `while`), `break/continue`.
5. [05_functions.py](file:///c:/work/python102/01_basics/05_functions.py) - Функц зарлах, параметр дамжуулах, Lambda (Arrow function), Scope (global/local).
6. [06_oop.py](file:///c:/work/python102/01_basics/06_oop.py) - Объект Хандалтат Програмчлал (Класс, Ид шидийн аргууд `__init__`, Удамшил, Полиморфизм).

**Скрипт ажиллуулах тушаал:**
```bash
python 01_basics/01_hello.py
```

---

### 3-р Алхам: Дунд шатны GUI Хөгжүүлэлт (`02_intermediate`)
Энэ хэсэгт Desktop аппликейшн хөгжүүлж сурна. Visual Basic хэлний Form, MsgBox, Controls зэрэгтэй харьцуулж сурахад хялбаршуулсан.

1. [01_gui_basics.py](file:///c:/work/python102/02_intermediate/01_gui_basics.py) - Цонх үүсгэх, Label, Button, Entry (текст оруулах), Layout (pack, grid), Event binding, Dialog цонхнууд болон бодит Тооцоолуур програм.
2. [02_gui_apps.py](file:///c:/work/python102/02_intermediate/02_gui_apps.py) - Илүү ахисан шатны GUI аппликейшн, Цэс (Menu), Canvas ашиглан зурах, зэрэг ажиллах процесс.
3. [03_pythonic_features.py](file:///c:/work/python102/02_intermediate/03_pythonic_features.py) - Python-ийг "Pythonic" болгодог онцлогууд (List Comprehensions, Generators, Decorators, Context Managers).
4. [04_shipping_projects.py](file:///c:/work/python102/02_intermediate/04_shipping_projects.py) - Төслөө хэрхэн бэлэн бүтээгдэхүүн болгож бусдад тараах, package үүсгэх, `.exe` файл болгон хөрвүүлэх.

*Дадлага ажил:* Төслийн үндсэн хавтсанд байгаа [calculator.py](file:///c:/work/python102/calculator.py) файлыг ажиллуулж, GUI тооны машины бүтцийг судлаарай:
```bash
python calculator.py
```

---

### 4-р Алхам: Өөрийн Чиглэлийг Сонгон Гүнзгийрүүлэх

Суурь болон дунд шатаа дуусгасан бол та өөрийн сонирхлоор дараах чиглэлүүдийн аль нэгийг (эсвэл бүгдийг) сонгон суралцах боломжтой:

#### 📊 Чиглэл А: Өгөгдлийн Шинжилгээ & Дүрслэл (`03_data_analysis`)
Дата дээр ажиллах, тооцоолол хийх, график дүрслэл бүтээх суурийг тавина.

1. Шаардлагатай сангуудыг суулгах:
   ```bash
   pip install numpy pandas matplotlib seaborn
   ```
2. Хичээлүүд:
   - [01_numpy_basics.py](file:///c:/work/python102/03_data_analysis/01_numpy_basics.py) - Матрицын тооцоолол, vectorization (for loop-оос хэд дахин хурдан болох хурдны тест).
   - [02_pandas_basics.py](file:///c:/work/python102/03_data_analysis/02_pandas_basics.py) - Өгөгдлийн хүснэгт (DataFrame), Excel/CSV унших, өгөгдөл цэвэрлэх, шүүх.
   - [03_visualization.py](file:///c:/work/python102/03_data_analysis/03_visualization.py) - Шугаман график, баганан график, тархалтын диаграмм зэргийг зурах.
   - [04_analysis_project.py](file:///c:/work/python102/03_data_analysis/04_analysis_project.py) - Бодит датасет дээр шинжилгээ хийж дүгнэлт гаргах бяцхан төсөл.

#### 🎮 Чиглэл Б: 2D Тоглоом Хөгжүүлэлт (`04_game_dev`)
Тоглоомын логик, объект мөргөлдөлт (collision), дэлгэцийн давтамж (frame rate), хөдөлгөөний физик зэргийг сурна.

1. Pygame сан суулгах:
   ```bash
   pip install pygame
   ```
2. Тоглоомын файлуудыг ажиллуулж, кодын логикийг судлах:
   - [01_pygame_basics.py](file:///c:/work/python102/04_game_dev/01_pygame_basics.py) - Pygame-ийн суурь бүтэц, цонх, үндсэн loop.
   - [02_pong.py](file:///c:/work/python102/04_game_dev/02_pong.py) - Сонгодог Pong тоглоом.
   - [03_snake.py](file:///c:/work/python102/04_game_dev/03_snake.py) - Могой тоглоом.
   - [04_space_invaders.py](file:///c:/work/python102/04_game_dev/04_space_invaders.py) - Сансрын дайн тоглоом.
   - [05_solitaire.py](file:///c:/work/python102/04_game_dev/05_solitaire.py) - Хөзрийн пасьянс тоглоом.
   - [06_decision_maker.py](file:///c:/work/python102/04_game_dev/06_decision_maker.py) - Сонголт хийгч хөгжөөнт тоглоом.
   - [07_tetris.py](file:///c:/work/python102/04_game_dev/07_tetris.py) - Тетрис.
   - [08_chess.py](file:///c:/work/python102/04_game_dev/08_chess.py) - Шатрын тоглоом (Логик ба дүрслэл).
   - [09_platformer.py](file:///c:/work/python102/04_game_dev/09_platformer.py) - Марио шиг үсэрч харайдаг Platformer тоглоом.

#### 🧠 Чиглэл В: Машин Сургалт & Хиймэл Оюун Ухаан (`05_machine_learning`)
Математик загварчлал, Хиймэл мэдрэлийн сүлжээ (Neural Networks) хэрхэн ажилладагийг суралцаж, TensorFlow, PyTorch сангуудын ялгааг танина.

1. Сангуудыг суулгах:
   ```bash
   pip install tensorflow torch torchvision
   ```
2. Сэдэвчилсэн хичээлүүд:
   - [01_linear_regression.py](file:///c:/work/python102/05_machine_learning/01_linear_regression.py) - Шугаман регрессийн математик суурь болон загвар сургах.
   - [02_tensorflow_basics.py](file:///c:/work/python102/05_machine_learning/02_tensorflow_basics.py) - TensorFlow дээр Tensor үүсгэх, үйлдэл хийх.
   - [03_pytorch_basics.py](file:///c:/work/python102/05_machine_learning/03_pytorch_basics.py) - PyTorch-ийн үндсэн үйлдлүүд болон Dynamic Computation Graph.
   - [04_classification_tensorflow.py](file:///c:/work/python102/05_machine_learning/04_classification_tensorflow.py) - TensorFlow Keras ашиглан зураг ангилах (Classification) сүлжээ угсрах.
   - [05_classification_pytorch.py](file:///c:/work/python102/05_machine_learning/05_classification_pytorch.py) - PyTorch ашиглан мэдрэлийн сүлжээ үүсгэж, сургах, шалгах алхмууд.

---

## 💡 Үр Дүнтэй Суралцах Зөвлөмжүүд

1. **Кодоо Унших**: Хичээлийн код бүр дээр маш дэлгэрэнгүй тайлбар комментуудыг (Монголоор) бичсэн тул зөвхөн ажиллуулаад өнгөрөх биш, комментуудыг анхааралтай уншаарай.
2. **Дасгалыг Заавал Хийх**: Файл бүрийн төгсгөлд байгаа **"🏋️ ДАСГАЛ АЖИЛ"** хэсгийг өөрийн гараар бичиж хийж үзээрэй. Энэ нь таны ойлголтыг бататгахад тусална.
3. **Интерактив Горимыг Ашиглах**: Код бичиж байхдаа аливаа функц эсвэл өгөгдлийг шалгахын тулд `-i` тушаалаар ажиллуулж болно. Ингэснээр код ажиллаж дууссаны дараа терминал хаагдахгүй бөгөөд та шууд хувьсагчийн утгыг шалгах боломжтой:
   ```bash
   python -i 01_basics/02_variables.py
   ```
4. **Хөгжүүлэлтийн явцад асуудал гарвал**: Виртуал орчин (`venv`) идэвхжсэн эсэхийг болон хэрэгцээт сангууд (`requirements.txt` эсвэл `pip install ...`) зөв суусан эсэхийг дахин нэг нягтлаарай.

Амжилт хүсье! 🚀 Python хэлийг сурснаар та Data Science, AI, Вэб хөгжүүлэлт зэрэг маш олон салбарт хөрвөх боломжтой болно.
