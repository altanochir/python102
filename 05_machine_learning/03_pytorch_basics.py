"""
╔══════════════════════════════════════════════════════════════════╗
║  🔥 Хичээл 5.3: PyTorch-ийн Үндэс                                ║
║  Tensor-той ажиллах, Autograd (Автомат уламжлал), SGD Linear Reg ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. PyTorch Tensor гэж юу вэ? (Үүсгэх, Хэлбэр өөрчлөх, CPU vs GPU)
   2. Autograd буюу Автомат уламжлал (requires_grad=True, backward)
   3. PyTorch ашиглан Linear Regression загвар үүсгэж сургах

📌 Суулгах заавар:
   pip install torch numpy
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import time

try:
    import numpy as np
    import torch
    import torch.nn as nn
    import torch.optim as optim
except ImportError:
    print("""
⚠️  PyTorch эсвэл NumPy суугаагүй байна!
Дараах тушаалаар суулгана уу:
    pip install torch numpy
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: PyTorch Tensor Үндэс & Төхөөрөмж (Device)
# ============================================================
def test_pytorch_tensors():
    print("\n=== 1. PyTorch Tensor-той ажиллах ===")
    
    # 1. Энгийн Tensor үүсгэх
    x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    print(f"Энгийн Tensor:\n{x}")
    print(f"Хэлбэр (Shape): {x.shape}, Өгөгдлийн төрөл: {x.dtype}")
    
    # 2. Тусгай Tensor-ууд
    zeros = torch.zeros(2, 3)
    ones = torch.ones(3, 1)
    rand = torch.randn(2, 2) # Нормал тархалттай санамсаргүй утга
    
    print(f"\nZeros (2x3):\n{zeros}")
    print(f"\nOnes (3x1):\n{ones}")
    print(f"\nRandom Normal (2x2):\n{rand}")
    
    # 3. Хэлбэр өөрчлөх (Reshape/View)
    # PyTorch-д ихэвчлэн view() эсвэл reshape()-ийг ашигладаг
    arr = torch.arange(9)
    reshaped = arr.view(3, 3)
    print(f"\nАнхны Tensor: {arr}")
    print(f"Шинэчилсэн Tensor (3x3):\n{reshaped}")
    
    # 4. Төхөөрөмж хооронд шилжих (CPU vs GPU/CUDA)
    # PyTorch нь GPU ашиглан тооцооллыг хурдасгахдаа маш хүчирхэг
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🖥️  Ашиглаж буй төхөөрөмж: {device.upper()}")
    
    # Tensor-ийг тодорхой төхөөрөмж рүү илгээх
    x_device = x.to(device)
    print(f"Tensor төхөөрөмж дээр шилжсэн: {x_device.device}")
    
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 2: PyTorch Autograd (Автомат уламжлал)
# ============================================================
def test_pytorch_autograd():
    print("\n=== 2. PyTorch Autograd (Автомат Уламжлал) ===")
    print("""
PyTorch-д `requires_grad=True` гэж тохируулснаар тухайн tensor дээр
хийгдсэн бүх үйлдлийг тэмдэглэж авдаг ба `.backward()` дуудах үед
автоматаар бүх уламжлалыг (gradient) бодож өгдөг.

Жишээ тэгшитгэл: y = 2*x^2 + 5*x
Уламжлал: dy/dx = 4*x + 5

Хэрэв x = 2.0 бол:
y = 2*(2.0^2) + 5*(2.0) = 8.0 + 10.0 = 18.0
dy/dx = 4 * 2.0 + 5 = 13.0
    """)
    
    # requires_grad=True нь градиент тооцох шаардлагатайг илтгэнэ
    x = torch.tensor(2.0, requires_grad=True)
    
    # Үйлдэл хийх
    y = 2 * (x ** 2) + 5 * x
    
    # Градиент бодох (Backward pass)
    y.backward()
    
    print(f"Оролтын утга x = {x.item()}")
    print(f"Бодсон утга y = 2*x^2 + 5*x = {y.item()}")
    print(f"📊 PyTorch-оор бодсон уламжлал (x.grad) = {x.grad.item()}")
    
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 3: PyTorch Linear Regression загвар сургах
# ============================================================
# Загвар болон өгөгдөл
torch_model = None

class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        # 1 оролттой, 1 гаралттай шугаман давхарга (w*x + b)
        self.linear = nn.Linear(in_features=1, out_features=1)
        
    def forward(self, x):
        # Forward pass: Оролтыг шугаман давхаргаар дамжуулах
        return self.linear(x)

def train_pytorch_regression():
    global torch_model
    print("\n=== 3. PyTorch Linear Regression Сургах ===")
    
    # 1. Өгөгдөл үүсгэх (y = 4*x + 3 + noise)
    np.random.seed(42)
    x_raw = np.random.rand(200, 1) * 10
    noise = np.random.randn(200, 1) * 1.0
    y_raw = 4 * x_raw + 3 + noise
    
    # Өгөгдлийг PyTorch Tensor болгон хөрвүүлэх (float32 төрөл чухал)
    X = torch.tensor(x_raw, dtype=torch.float32)
    y = torch.tensor(y_raw, dtype=torch.float32)
    
    # 2. Загвар, Алдааны функц (Loss), Оновчлогч (Optimizer) тодорхойлох
    torch_model = LinearRegressionModel()
    criterion = nn.MSELoss() # Mean Squared Error алдааны функц
    optimizer = optim.SGD(torch_model.parameters(), lr=0.01) # Stochastic Gradient Descent
    
    # Сургахаас өмнөх жин ба хазайлт
    with torch.no_grad(): # Сургах явцаас гадуур үед градиент тооцохгүй
        w_init, b_init = torch_model.linear.weight.item(), torch_model.linear.bias.item()
    print(f"Сургахаас өмнөх жин w = {w_init:.4f}, хазайлт b = {b_init:.4f}")
    
    # 3. Сургах цикл (Training Loop)
    epochs = 100
    print("\nСургаж байна (100 Epoch)...")
    print(f"{'Epoch':<10}{'Loss (MSE)':<15}")
    print("-" * 30)
    
    for epoch in range(1, epochs + 1):
        # А. Forward Pass: Таамаглал хийх
        y_pred = torch_model(X)
        
        # Б. Алдааг (Loss) тооцох
        loss = criterion(y_pred, y)
        
        # В. Градиентийг тэгэлэх (Заавал хийх алхам!)
        # PyTorch нь градиентийг хуримтлуулдаг тул алхам тутамд тэгэлэх ёстой.
        optimizer.zero_grad()
        
        # Г. Backward Pass: Уламжлалуудыг бодох
        loss.backward()
        
        # Д. Параметрүүдийг шинэчлэх (Optimizer step)
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"{epoch:<10}{loss.item():<15.4f}")
            time.sleep(0.05)
            
    print("-" * 30)
    
    # Сургасны дараах жин ба хазайлт
    with torch.no_grad():
        w_final, b_final = torch_model.linear.weight.item(), torch_model.linear.bias.item()
    print("🎉 Сургалт амжилттай дууслаа!")
    print(f"Сургагдсан жин w = {w_final:.4f}")
    print(f"Сургагдсан хазайлт b = {b_final:.4f}")
    print("Бодит утга: w = 4.0, b = 3.0")


def test_pytorch_predictions():
    global torch_model
    print("\n=== 4. PyTorch Загвараар Таамаглал Хийх ===")
    if torch_model is None:
        print("⚠️  Анхаар: Эхлээд 3-р цэсээр орж загварыг сургана уу!")
        return
        
    torch_model.eval() # Загварыг үнэлгээний (Evaluation) горимд шилжүүлнэ
    
    while True:
        try:
            val = input("Оролтын утга X-ийг оруулна уу (Гарахын тулд 'q'): ").strip()
            if val.lower() == 'q':
                break
            
            # Таамаглал хийхэд градиент тооцох шаардлагагүй
            with torch.no_grad():
                x_input = torch.tensor([[float(val)]], dtype=torch.float32)
                y_pred = torch_model(x_input)
                
            y_real = 4 * float(val) + 3
            
            print(f"🔮 Загварын таамаглал (y_pred) = {y_pred.item():.4f}")
            print(f"📏 Бодит шулууны утга (y_real) = {y_real:.4f}")
            print(f"📉 Зөрүү (Error) = {abs(y_pred.item() - y_real):.4f}")
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
║  🔥 PyTorch Үндэс — Хичээл 5.3                    ║
║                                                  ║
║  1. 📦 PyTorch Tensor-той ажиллах                ║
║  2. 📉 Autograd (Автомат уламжлал)               ║
║  3. 🏋️ PyTorch-оор Linear Regression сургах       ║
║  4. 🔮 Таамаглал хийж үзэх                       ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
        """)
        
        choice = input("Сонголт (0-4): ").strip()
        
        if choice == "1":
            test_pytorch_tensors()
        elif choice == "2":
            test_pytorch_autograd()
        elif choice == "3":
            train_pytorch_regression()
        elif choice == "4":
            test_pytorch_predictions()
        elif choice == "0":
            print("👋 Хичээл 5.3 дууслаа. Баяртай!")
            break
        else:
            print("⚠️ 0-4 хооронд сонгоно уу!")
        print("-" * 50)
