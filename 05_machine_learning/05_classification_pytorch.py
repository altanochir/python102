"""
╔══════════════════════════════════════════════════════════════════╗
║  🔥 Хичээл 5.5: PyTorch Custom Dataset & MLP Ангилал             ║
║  Dataset, DataLoader, nn.Module, Сургах цикл (Training Loop)      ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. PyTorch-д Custom Dataset болон DataLoader үүсгэх
   2. nn.Module ашиглан MLP Мэдрэлийн Сүлжээг угсрах
   3. PyTorch-ийн Сургах Цикл (Training Loop)-ийг гараас бичиж ажиллуулах
   4. Шинэ өгөгдөл дээр таамаглал (Inference) хийх

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
    from torch.utils.data import Dataset, DataLoader
except ImportError:
    print("""
⚠️  PyTorch эсвэл NumPy суугаагүй байна!
Дараах тушаалаар суулгана уу:
    pip install torch numpy
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: PyTorch Custom Dataset & DataLoader
# ============================================================
class CircleDataset(Dataset):
    """
    PyTorch-д өгөгдлийг оновчтой удирдахын тулд Dataset ангийг өвлүүлэн үүсгэдэг.
    Шардлагатай 3 функц:
      - __init__: Өгөгдлийг бэлдэх
      - __len__: Өгөгдлийн нийт тоог буцаах
      - __getitem__: Индексээр нэг элементийг сонгож буцаах
    """
    def __init__(self, num_samples=1000):
        np.random.seed(42)
        # 2D цэгүүд үүсгэх (-2-оос 2 хооронд)
        self.X = np.random.uniform(-2, 2, (num_samples, 2)).astype(np.float32)
        # Хэрэв x1^2 + x2^2 < 1.5 бол 1, үгүй бол 0
        self.y = (np.sum(self.X**2, axis=1) < 1.5).astype(np.float32).reshape(-1, 1)
        
    def __len__(self):
        return len(self.X)
        
    def __getitem__(self, idx):
        # Хүссэн индексийн өгөгдлийг PyTorch Tensor болгон буцаана
        x_tensor = torch.tensor(self.X[idx])
        y_tensor = torch.tensor(self.y[idx])
        return x_tensor, y_tensor


# Өгөгдлийн багцуудыг бэлтгэх
train_dataset = CircleDataset(num_samples=800)
test_dataset = CircleDataset(num_samples=200)

# DataLoader нь өгөгдлийг багцлан (Mini-batch), холих (Shuffle) үүргийг гүйцэтгэнэ
train_loader = DataLoader(dataset=train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=32, shuffle=False)

def show_dataset_info():
    print("\n=== 1. Custom Dataset & DataLoader Харах ===")
    print(f"Сургалтын нийт өгөгдлийн хэмжээ: {len(train_dataset)}")
    print(f"Тестийн нийт өгөгдлийн хэмжээ:   {len(test_dataset)}")
    
    # Эхний багцыг аваад харах
    for X_batch, y_batch in train_loader:
        print(f"\nБагц (Batch) хэмжээ:")
        print(f"  - X_batch хэлбэр (Shape): {X_batch.shape} (32 цэг, тус бүр 2D)")
        print(f"  - y_batch хэлбэр (Shape): {y_batch.shape} (32 хариулт)")
        break
        
    input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")


# ============================================================
# 📌 ХЭСЭГ 2: MLP Загвар тодорхойлох (nn.Module)
# ============================================================
class MLPClassifier(nn.Module):
    """
    PyTorch-д загварыг nn.Module-оос өвлүүлж үүсгэдэг.
    __init__-д сүлжээний давхаргуудыг зарлаж, forward-д хэрхэн дамжихыг тодорхойлно.
    """
    def __init__(self):
        super(MLPClassifier, self).__init__()
        
        # Sequental ашиглан давхаргуудыг дараалуулан холбох
        self.network = nn.Sequential(
            nn.Linear(in_features=2, out_features=16),
            nn.ReLU(),
            nn.Linear(in_features=16, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=1),
            nn.Sigmoid()  # Бинар ангилалд тохирох идэвхжүүлэлт
        )
        
    def forward(self, x):
        return self.network(x)


# ============================================================
# 📌 ХЭСЭГ 3: PyTorch Сонгодог Сургах Цикл (Training Loop)
# ============================================================
py_model = None

def train_pytorch_mlp():
    global py_model
    print("\n=== 3. PyTorch MLP Загварыг Сургах Цогц Цикл ===")
    
    # 1. Загвар, Оновчлогч, Алдааны функц үүсгэх
    py_model = MLPClassifier()
    criterion = nn.BCELoss() # Binary Cross Entropy loss (Sigmoid-ийн дараа хэрэглэнэ)
    optimizer = optim.Adam(py_model.parameters(), lr=0.01)
    
    epochs = 30
    print(f"Сургаж эхэллээ (Нийт {epochs} epoch, Batch size = 32)...")
    print(f"{'Epoch':<10}{'Train Loss':<15}{'Val Loss':<15}{'Val Acc':<10}")
    print("-" * 55)
    
    for epoch in range(1, epochs + 1):
        # А. Загварыг сургалтын горимд оруулах
        py_model.train()
        train_loss = 0.0
        
        for X_batch, y_batch in train_loader:
            # 1. Градиентийг тэгэлэх
            optimizer.zero_grad()
            # 2. Forward pass
            outputs = py_model(X_batch)
            # 3. Loss тооцох
            loss = criterion(outputs, y_batch)
            # 4. Backward pass
            loss.backward()
            # 5. Параметрийг шинэчлэх (Optimizer step)
            optimizer.step()
            
            train_loss += loss.item() * X_batch.size(0)
            
        train_loss = train_loss / len(train_loader.dataset)
        
        # Б. Загварыг үнэлгээний горимд оруулах (Тест өгөгдөл дээр шалгах)
        py_model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad(): # Градиент бодох шаардлагагүй
            for X_batch, y_batch in test_loader:
                outputs = py_model(X_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item() * X_batch.size(0)
                
                # Нарийвчлалыг тооцох (Хэрэв магадлал >= 0.5 бол Class 1, үгүй бол Class 0)
                predictions = (outputs >= 0.5).float()
                correct += (predictions == y_batch).sum().item()
                total += y_batch.size(0)
                
        val_loss = val_loss / len(test_loader.dataset)
        val_acc = (correct / total) * 100
        
        if epoch % 5 == 0 or epoch == 1:
            print(f"{epoch:<10}{train_loss:<15.4f}{val_loss:<15.4f}{val_acc:<10.2f}%")
            time.sleep(0.05)
            
    print("-" * 55)
    print("🎉 Сургалт амжилттай дууслаа!")


# ============================================================
# 📌 ХЭСЭГ 4: Таамаглал Хийж Үзэх (Inference)
# ============================================================
def predict_with_pytorch():
    global py_model
    print("\n=== 4. PyTorch Загвараар Таамаглал Хийх ===")
    if py_model is None:
        print("⚠️  Анхаар: Эхлээд 3-р цэсээр орж загварыг сургана уу!")
        return
        
    py_model.eval()
    print("Координат оруулан дугуйн дотор (1) эсвэл гадна (0) байгааг таана уу. (Хил: X1^2 + X2^2 < 1.5)")
    
    while True:
        try:
            x1_str = input("Координат X1 (жишээ нь, -0.6) эсвэл гарахын тулд 'q': ").strip()
            if x1_str.lower() == 'q':
                break
            x2_str = input("Координат X2 (жишээ нь, 1.1): ").strip()
            
            x1 = float(x1_str)
            x2 = float(x2_str)
            
            # Оролтыг PyTorch Tensor болгож бэлдэх
            point = torch.tensor([[x1, x2]], dtype=torch.float32)
            
            with torch.no_grad():
                pred_prob = py_model(point).item()
                pred_class = 1 if pred_prob >= 0.5 else 0
                
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
║  🤖 PyTorch MLP Ангилал — Хичээл 5.5             ║
║                                                  ║
║  1. 📦 Custom Dataset & DataLoader харах          ║
║  2. 📐 nn.Module ашиглан MLP бүтэц харах          ║
║  3. 🏋️ PyTorch-ийн Сургах Циклийг ажиллуулах       ║
║  4. 🔮 Шинэ цэг дээр таамаглал хийх              ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
        """)
        
        choice = input("Сонголт (0-4): ").strip()
        
        if choice == "1":
            show_dataset_info()
        elif choice == "2":
            # MLP бүтэцтэй танилцуулах тайлбарыг хэвлэх
            print("\n=== 2. MLP Мэдрэлийн Сүлжээний Бүтэц ===")
            temp_model = MLPClassifier()
            print(temp_model)
            print("""
Давхаргуудын үүрэг:
- self.network[0] (nn.Linear 2 -> 16): Оролтын 2 хэмжээст цэгийг 16 хэмжээст орон зайд шилжүүлнэ.
- self.network[1] (nn.ReLU): Шугаман бус шинж чанарыг оруулна.
- self.network[2] (nn.Linear 16 -> 8): 16 нейроны гаралтыг 8 нейрон руу хумьж далд шинжүүдийг сурна.
- self.network[3] (nn.ReLU): Дахин шугаман бус шинж чанар оруулна.
- self.network[4] (nn.Linear 8 -> 1): 8 нейроныг 1 гаралт болгон нэгтгэнэ.
- self.network[5] (nn.Sigmoid): Гаралтыг 0-оос 1-ийн хооронд шилжүүлж магадлал болгоно.
            """)
            input("\nҮргэлжлүүлэхийн тулд [Enter] дарна уу...")
        elif choice == "3":
            train_pytorch_mlp()
        elif choice == "4":
            predict_with_pytorch()
        elif choice == "0":
            print("👋 Хичээл 5.5 дууслаа. Баяртай!")
            break
        else:
            print("⚠️ 0-4 хооронд сонгоно уу!")
        print("-" * 50)
