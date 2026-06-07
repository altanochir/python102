"""
╔══════════════════════════════════════════════════════════════════╗
║  🔥 Хичээл 5.2: TensorFlow / Keras-ийн Үндэс                     ║
║  Tensor-той ажиллах, tf.GradientTape, Keras Linear Regression    ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. TensorFlow Tensor гэж юу вэ? (Үүсгэх, Хэлбэр, Математик үйлдлүүд)
   2. Автомат уламжлал (Automatic Differentiation) ба tf.GradientTape
   3. Keras ашиглан Linear Regression загвар бэлдэж сургах

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
# 📌 ХЭСЭГ 1: TensorFlow Tensor Үндэс
# ============================================================
def test_tensors():
    print("\n=== 1. TensorFlow Tensor-той ажиллах ===")
    
    # 1. Сонгодог утгаас Tensor үүсгэх (Скаляр, Вектор, Матриц)
    scalar = tf.constant(42)
    vector = tf.constant([1.0, 2.0, 3.0])
    matrix = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
    
    print(f"Скаляр: {scalar}, Хэмжээс: {scalar.ndim}")
    print(f"Вектор: {vector}, Хэлбэр (Shape): {vector.shape}")
    print(f"Матриц:\n{matrix}\nӨгөгдлийн төрөл: {matrix.dtype}")
    
    # 2. Тусгай Tensor үүсгэх (Zeros, Ones, Random)
    zeros = tf.zeros(shape=(2, 3))
    ones = tf.ones(shape=(3, 1))
    random_tensor = tf.random.normal(shape=(2, 2), mean=0.0, stddev=1.0)
    
    print(f"\nZeros (2x3):\n{zeros}")
    print(f"\nOnes (3x1):\n{ones}")
    print(f"\nСанамсаргүй Tensor (Random Normal 2x2):\n{random_tensor}")
    
    # 3. Математик үйлдлүүд
    a = tf.constant([[1, 2], [3, 4]])
    b = tf.constant([[5, 6], [7, 8]])
    
    add = tf.add(a, b)       # a + b
    matmul = tf.matmul(a, b) # Матрицын үржвэр (a @ b)
    
    print(f"\nМатриц нэмэх (a + b):\n{add}")
    print(f"\nМатрицын үржвэр (a @ b):\n{matmul}")
    
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 2: tf.GradientTape (Автомат дифференциал)
# ============================================================
def test_gradient_tape():
    print("\n=== 2. tf.GradientTape (Автомат Уламжлал) ===")
    print("""
TensorFlow нь уламжлал (gradient) тооцоолохдоо tf.GradientTape-ийг ашигладаг.
Энэ нь мэдрэлийн сүлжээг арын хэсэгт сургах (Backpropagation) гол суурь юм.

Жишээ тэгшитгэл: y = x^2
Уламжлал (дифференциал): dy/dx = 2*x

Хэрэв x = 3.0 бол:
y = 3^2 = 9.0
dy/dx = 2 * 3.0 = 6.0
    """)
    
    x = tf.Variable(3.0) # Параметрийг tf.Variable болгож зарлана (Шинэчлэгдэх боломжтой)
    
    with tf.GradientTape() as tape:
        y = x ** 2
        
    # y-ээс x-ийн дагуу уламжлал авах
    dy_dx = tape.gradient(y, x)
    
    print(f"Оролтын утга x = {x.numpy()}")
    print(f"Бодсон утга y = x^2 = {y.numpy()}")
    print(f"📊 tf.GradientTape-ээр бодсон уламжлал (dy/dx) = {dy_dx.numpy()}")
    
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 3: Keras API ашиглан Linear Regression хийх
# ============================================================
# Загварын параметрүүд
model = None
X_train = None
y_train = None

def train_keras_linear_regression():
    global model, X_train, y_train
    print("\n=== 3. Keras Linear Regression Загвар Сургах ===")
    
    # 1. Энгийн өгөгдөл үүсгэх (y = 3*x + 2 + noise)
    np.random.seed(42)
    X_train = np.random.rand(200, 1) * 10
    noise = np.random.randn(200, 1) * 1.0
    y_train = 3 * X_train + 2 + noise
    
    print("Сургалтын өгөгдлийг бэлдлээ (Үнэн тэгшитгэл: y = 3*x + 2)")
    print(f"Оролтын X хэлбэр: {X_train.shape}, Хариултын y хэлбэр: {y_train.shape}")
    
    # 2. Keras Sequential загвар үүсгэх
    # 1 оролттой, 1 гаралттай ганц Dense давхарга (Dense нь y = w*x + b-ийг хийдэг)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[1])
    ])
    
    # 3. Загвараа compile хийх (Алдааны функц болон Optimizer тохируулах)
    model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
        loss='mean_squared_error'
    )
    
    print("\nKeras загварын бүтэц (Summary):")
    model.summary()
    
    # Сургахаас өмнөх жин болон хазайлтыг харах
    weights = model.layers[0].get_weights()
    print(f"\nСургахаас өмнөх жин w = {weights[0][0][0]:.4f}, хазайлт b = {weights[1][0]:.4f}")
    
    print("\nСургаж байна (20 Epoch)...")
    # verbose=1 нь сургалтын явцыг харуулна
    model.fit(X_train, y_train, epochs=20, verbose=1)
    
    # Сургасны дараах жин болон хазайлтыг харах
    trained_weights = model.layers[0].get_weights()
    print(f"\n🎉 Сургалт дууслаа!")
    print(f"Сургагдсан жин w = {trained_weights[0][0][0]:.4f}")
    print(f"Сургагдсан хазайлт b = {trained_weights[1][0]:.4f}")
    print("Бодит утга: w = 3.0, b = 2.0")


def test_keras_predictions():
    global model
    print("\n=== 4. Keras Загвараар Таамаглал Хийх ===")
    if model is None:
        print("⚠️  Анхаар: Эхлээд 3-р цэсээр орж загварыг сургана уу!")
        return
        
    while True:
        try:
            val = input("Оролтын утга X-ийг оруулна уу (Гарахын тулд 'q'): ").strip()
            if val.lower() == 'q':
                break
            
            x_input = np.array([[float(val)]])
            y_pred = model.predict(x_input, verbose=0)
            
            # Бодит хариулттай харьцуулах (y = 3*x + 2)
            y_real = 3 * float(val) + 2
            
            print(f"🔮 Загварын таамаглал (y_pred) = {y_pred[0][0]:.4f}")
            print(f"📏 Бодит шулууны утга (y_real) = {y_real:.4f}")
            print(f"📉 Зөрүү (Error) = {abs(y_pred[0][0] - y_real):.4f}")
            print("-" * 40)
        except ValueError:
            print("⚠️  Зөвхөн тоон утга эсвэл 'q' оруулна уу!")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЦЭС
# ============================================================
if __name__ == "__main__":
    while True:
        print("""
╔══════════════════════════════════════════════════╗
║  🔥 TensorFlow / Keras Үндэс — Хичээл 5.2         ║
║                                                  ║
║  1. 📦 TensorFlow Tensor-той ажиллах             ║
║  2. 📉 tf.GradientTape (Автомат уламжлал)         ║
║  3. 🏋️ Keras-аар Linear Regression сургах         ║
║  4. 🔮 Таамаглал хийж үзэх                       ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
        """)
        
        choice = input("Сонголт (0-4): ").strip()
        
        if choice == "1":
            test_tensors()
        elif choice == "2":
            test_gradient_tape()
        elif choice == "3":
            train_keras_linear_regression()
        elif choice == "4":
            test_keras_predictions()
        elif choice == "0":
            print("👋 Хичээл 5.2 дууслаа. Баяртай!")
            break
        else:
            print("⚠️ 0-4 хооронд сонгоно уу!")
        print("-" * 50)
