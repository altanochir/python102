"""
╔══════════════════════════════════════════════════════════════════╗
║  🔥 Хичээл 5.4: Мэдрэлийн Сүлжээ & TensorFlow Ангилал            ║
║  Идэвхжүүлэх функц, Keras MLP, Бинар Ангилал (Binary Class)       ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Идэвхжүүлэх функц (Activation Function) гэж юу вэ? (ReLU, Sigmoid, Softmax)
   2. Олон давхаргат мэдрэлийн сүлжээ (Multi-Layer Perceptron - MLP) угсрах
   3. Угаалгын өрөө шиг дугуй өгөгдөл (Circle boundary) дээр загвараа сургаж, үнэлэх

📌 Суулгах заавар:
   pip install tensorflow numpy
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import time

try:
    import numpy as np
    import tensorflow as tf
except ImportError:
    print("""
⚠️  TensorFlow эсвэл NumPy суугаагүй байна!
Дараах тушаалаар суулгана уу:
    pip install tensorflow numpy
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: Идэвхжүүлэх Функцүүдийн Тайлбар
# ============================================================
def show_activations():
    print("\n=== 1. Идэвхжүүлэх Функц (Activation Functions) ===")
    print("""
Мэдрэлийн сүлжээнд шугаман бус шинж чанарыг (Non-linearity) оруулахын тулд
идэвхжүүлэх функцийг ашигладаг. Үүнгүйгээр сүлжээ хэчнээн олон давхаргатай
байсан ч ердөө шугаман регресс шиг ажиллана.

Гол функцүүд:
1. ReLU (Rectified Linear Unit):
   - Томьёо: f(x) = max(0, x)
   - Хэрэглээ: Далд давхаргуудад (Hidden layers) хамгийн өргөн ашиглагддаг.
   - Давуу тал: Тооцоолоход маш хурдан бөгөөд градиент устах (vanishing gradient) асуудлыг шийддэг.

2. Sigmoid:
   - Томьёо: f(x) = 1 / (1 + e^-x)
   - Утгын муж: 0-оос 1-ийн хооронд утга буцаана (Магадлал).
   - Хэрэглээ: Бинар ангилалын (Хоёр ангилалтай бодлого) гаралтын давхаргад ашиглана.

3. Softmax:
   - Томьёо: Олон ангилалт магадлалын вектор үүсгэнэ (Нийлбэр нь 1 байна).
   - Хэрэглээ: Олон ангилалт (Multi-class: жишээ нь 0-9 тоог ялгах) гаралтын давхаргад ашиглана.
    """)
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 2: Бинар Өгөгдөл Бэлтгэх (Дугуйн хилийн бодлого)
# ============================================================
# Сургалтын болон тестийн өгөгдөл бэлтгэх
# Дугуйн доторх цэгүүд нь Class 1, гаднах нь Class 0
np.random.seed(42)
n_samples = 1000

# -2-оос 2-ын хооронд 2D цэгүүд үүсгэх
X_data = np.random.uniform(-2, 2, (n_samples, 2))
# Хэрэв x1^2 + x2^2 < 1.5 бол ангилал нь 1, үгүй бол 0
y_data = (np.sum(X_data**2, axis=1) < 1.5).astype(np.float32)

# Өгөгдлийг сургалтын (80%) ба тестийн (20%) болгон хуваах
split_idx = int(n_samples * 0.8)
X_train, X_test = X_data[:split_idx], X_data[split_idx:]
y_train, y_test = y_data[:split_idx], y_data[split_idx:]

def show_data_info():
    print("\n=== 2. Өгөгдлийн Мэдээлэл (Нэгэн төвт дугуйнууд) ===")
    print("Шугаман зааггүй, дугуй хэлбэртэй хилийг мэдрэлийн сүлжээ сурах шаардлагатай.")
    print(f"Сургалтын оролт X хэлбэр: {X_train.shape}, Хариулт y хэлбэр: {y_train.shape}")
    print(f"Тестийн оролт X хэлбэр: {X_test.shape}, Хариулт y хэлбэр: {y_test.shape}")
    
    # Ангиллын хуваарилалт
    class1_count = np.sum(y_train == 1)
    class0_count = np.sum(y_train == 0)
    print(f"Ангилал 1-ийн тоо (Дугуйн дотор): {class1_count}")
    print(f"Ангилал 0-ийн тоо (Дугуйн гадна): {class0_count}")
    
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 3: Keras MLP Загвар Угсрах & Сургах
# ============================================================
mlp_model = None

def train_keras_mlp():
    global mlp_model
    print("\n=== 3. Keras MLP Загвар Үүсгэж Сургах ===")
    
    # MLP загварын бүтэц:
    # - Оролт: 2 хэмжээст цэг (x1, x2)
    # - Далд давхарга 1: 16 нейрон, ReLU идэвхжүүлэлт
    # - Далд давхарга 2: 8 нейрон, ReLU идэвхжүүлэлт
    # - Гаралтын давхарга: 1 нейрон, Sigmoid идэвхжүүлэлт (Бинар ангилал)
    
    mlp_model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(2,)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Загварыг compile хийх
    # Бинар ангилалд 'binary_crossentropy' алдааны функц хэрэглэдэг
    mlp_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nМэдрэлийн сүлжээний бүтэц:")
    mlp_model.summary()
    
    print("\nСургаж байна (30 Epoch)...")
    # validation_split ашиглан сургалтын явцад тест өгөгдөл дээрх нарийвчлалыг хянах
    history = mlp_model.fit(
        X_train, y_train,
        epochs=30,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Эцсийн үнэлгээ
    loss, accuracy = mlp_model.evaluate(X_test, y_test, verbose=0)
    print("\n🎉 Сургалт дууслаа!")
    print(f"📈 Тестийн өгөгдөл дээрх Алдаа (Loss):     {loss:.4f}")
    print(f"🎯 Тестийн өгөгдөл дээрх Нарийвчлал (Accuracy): {accuracy * 100:.2f}%")


def test_custom_point():
    global mlp_model
    print("\n=== 4. Цэг оруулан Ангиллыг шалгах ===")
    if mlp_model is None:
        print("⚠️  Анхаар: Эхлээд 3-р цэсээр орж загварыг сургана уу!")
        return
        
    print("Заавар: 2D цэгийн координат X1, X2-ийг оруулж загвар дугуйн дотор (1) эсвэл гадна (0) гэж тааж байгааг шалгана уу.")
    print("Санамж: Манай сургалтын хил нь: x1^2 + x2^2 < 1.5 (радиус нь ~1.225) юм.")
    
    while True:
        try:
            x1_str = input("Координат X1 (жишээ нь, 0.5) эсвэл гарахын тулд 'q': ").strip()
            if x1_str.lower() == 'q':
                break
            x2_str = input("Координат X2 (жишээ нь, 0.8): ").strip()
            
            x1 = float(x1_str)
            x2 = float(x2_str)
            
            # Таамаглал хийх
            point = np.array([[x1, x2]])
            pred_prob = mlp_model.predict(point, verbose=0)[0][0]
            pred_class = 1 if pred_prob >= 0.5 else 0
            
            # Бодит ангилал
            distance_sq = x1**2 + x2**2
            real_class = 1 if distance_sq < 1.5 else 0
            
            print(f"\n📊 Тооцоолсон зай (X1^2 + X2^2) = {distance_sq:.4f}")
            print(f"🔮 Загварын таамагласан магадлал: {pred_prob:.4f}")
            print(f"🎯 Загварын таамаглал (Class):  {pred_class} ({'Дугуйн дотор' if pred_class == 1 else 'Дугуйн гадна'})")
            print(f"📏 Бодит ангилал (Real Class):     {real_class} ({'Дугуйн дотор' if real_class == 1 else 'Дугуйн гадна'})")
            if pred_class == real_class:
                print("✅ Зөв таамаглалаа!")
            else:
                print("❌ Буруу таамаглалаа.")
            print("-" * 50)
        except ValueError:
            print("⚠️  Тоон утга оруулна уу!")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЦЭС
# ============================================================
if __name__ == "__main__":
    while True:
        print("""
╔══════════════════════════════════════════════════╗
║  🤖 TensorFlow MLP Ангилал — Хичээл 5.4          ║
║                                                  ║
║  1. 📖 Идэвхжүүлэх функцүүдийн онол              ║
║  2. 📊 Ангилах өгөгдлийн мэдээлэл                ║
║  3. 🏋️ Keras MLP загвар сургах                    ║
║  4. 🔮 Шинэ цэг дээр таамаглал хийх              ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
        """)
        
        choice = input("Сонголт (0-4): ").strip()
        
        if choice == "1":
            show_activations()
        elif choice == "2":
            show_data_info()
        elif choice == "3":
            train_keras_mlp()
        elif choice == "4":
            test_custom_point()
        elif choice == "0":
            print("👋 Хичээл 5.4 дууслаа. Баяртай!")
            break
        else:
            print("⚠️ 0-4 хооронд сонгоно уу!")
        print("-" * 50)
