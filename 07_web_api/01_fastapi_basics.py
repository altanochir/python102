"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 7.1: FastAPI — REST API үүсгэх & Өгөгдлийн Шүүлт       ║
║  Python 102 — JavaScript (Express.js) туршлагатай хөгжүүлэгчдэд   ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. FastAPI ашиглан вэб сервер асаах
   2. Path parameters (Замын параметр) ба Query parameters (Асуулгын параметр)
   3. Pydantic ашиглан Request Body-ийг баталгаажуулах (Validation)
   4. CRUD (Унших, Нэмэх, Шинэчлэх, Устгах) API бүтээх

💡 JS / Express.js хөгжүүлэгч танд:
   - Express дээр бид `body-parser` ашиглаж, өгөгдлийг гараар шалгадаг эсвэл `Zod` сан
     ашигладаг бол, FastAPI-д Python-ий Type Hints болон Pydantic-ийг ашиглан
     оролтын өгөгдлийг шууд, автоматаар шалгадаг.
   - Өөрөөр хэлбэл, кодоо бичээд л ямар ч нэмэлт тохиргоогүйгээр
     TypeScript + Runtime validation + Swagger Docs-той болно гэсэн үг! 🎉
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

# Шаардлагатай сангуудыг шалгах
try:
    from fastapi import FastAPI, HTTPException, status
    from pydantic import BaseModel, Field
    from typing import Optional, List
except ImportError:
    print("""
⚠️  FastAPI эсвэл Pydantic суугаагүй байна!
Терминал дээр дараах тушаалаар суулгана уу:
    pip install fastapi uvicorn
    """)
    sys.exit(1)

# 1. FastAPI аппликейшн үүсгэх (Express: const app = express())
app = FastAPI(
    title="Todo жагсаалтын API 📝",
    description="Python 102 - FastAPI сургалтын хүрээнд хийсэн CRUD вэб үйлчилгээ",
    version="1.0.0"
)


# ============================================================
# 📌 ХЭСЭГ 1: Өгөгдлийн Модел (Pydantic BaseModel)
# ============================================================
"""
Pydantic нь орох болон гарах өгөгдлийг баталгаажуулахад хэрэглэгддэг.
JS-ийн Zod эсвэл TypeScript Interface-тэй маш төстэй.
Хэрэглэгч буруу төрлийн өгөгдөл илгээвэл (жишээ нь string байх ёстой газар int өгвөл)
FastAPI автоматаар '422 Unprocessable Entity' алдаа болон тайлбарыг буцаана.
"""

class TodoItem(BaseModel):
    id: int
    title: str = Field(..., min_length=2, max_length=100, description="Ажлын гарчиг, хамгийн багадаа 2 тэмдэгт байна")
    description: Optional[str] = Field(None, description="Нэмэлт тайлбар")
    completed: bool = Field(default=False, description="Ажил дууссан эсэх")

class TodoCreate(BaseModel):
    """Шинээр ажил нэмэхэд хэрэглэх модел (ID шаардлагагүй, систем автоматаар үүсгэнэ)"""
    title: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    completed: bool = False

class TodoUpdate(BaseModel):
    """Ажлыг засахад хэрэглэх модел (Зөвхөн засах талбаруудыг оноож болно)"""
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    completed: Optional[bool] = None


# ============================================================
# 📌 ХЭСЭГ 2: Санах ойд суурилсан Өгөгдлийн Сан (In-memory DB)
# ============================================================
# Сургалтын зориулалтаар өгөгдлийг Python List дотор хадгална.
todo_db: List[TodoItem] = [
    TodoItem(id=1, title="Python 102 хичээлийг унших", description="Анхан шатны суурь хичээлүүдийг дуусгах", completed=True),
    TodoItem(id=2, title="FastAPI ашиглан API хийх", description="CRUD сэдвийг судлах", completed=False),
    TodoItem(id=3, title="Дасгал ажлуудыг хийх", description="Файл тус бүрийн төгсгөлд байгаа дасгалууд", completed=False),
]


# ============================================================
# 📌 ХЭСЭГ 3: GET - Өгөгдөл Унших (Read)
# ============================================================

# Эхлэх цонх
@app.get("/", tags=["Ерөнхий"])
def read_root():
    return {
        "message": "FastAPI Todo API-д тавтай морил! 🚀",
        "docs": "API-ийг туршихын тулд /docs хаяг руу хандана уу."
    }

# Бүх ажиллуудыг авах (Query Parameter ашиглах)
# Хэрэглэгч /todos?completed=true гэж шүүж болно.
@app.get("/todos", response_model=List[TodoItem], tags=["Todo Ажлууд"])
def get_todos(completed: Optional[bool] = None):
    """
    Бүх ажлын жагсаалтыг буцаана. 
    'completed' параметрээр шүүх боломжтой.
    """
    if completed is not None:
        filtered_todos = [todo for todo in todo_db if todo.completed == completed]
        return filtered_todos
    return todo_db

# Тодорхой нэг ажлыг ID-аар нь авах (Path Parameter ашиглах)
@app.get("/todos/{todo_id}", response_model=TodoItem, tags=["Todo Ажлууд"])
def get_todo(todo_id: int):
    """Ажлыг ID-аар нь хайна. Олдохгүй бол 404 алдаа буцаана."""
    for todo in todo_db:
        if todo.id == todo_id:
            return todo
            
    # Express: res.status(404).json({message: "Not Found"})
    # FastAPI:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"ID={todo_id} бүхий ажил олдсонгүй!"
    )


# ============================================================
# 📌 ХЭСЭГ 4: POST - Шинээр Өгөгдөл Үүсгэх (Create)
# ============================================================

@app.post("/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED, tags=["Todo Ажлууд"])
def create_todo(todo_in: TodoCreate):
    """Шинэ Todo ажил нэмэх. Автоматаар шинэ ID онооно."""
    # Шинэ ID олох
    new_id = max([todo.id for todo in todo_db]) + 1 if todo_db else 1
    
    # Шинэ TodoItem үүсгэх
    new_todo = TodoItem(
        id=new_id,
        title=todo_in.title,
        description=todo_in.description,
        completed=todo_in.completed
    )
    
    # Жагсаалтад нэмэх
    todo_db.append(new_todo)
    return new_todo


# ============================================================
# 📌 ХЭСЭГ 5: PUT - Өгөгдөл Шинэчлэх (Update)
# ============================================================

@app.put("/todos/{todo_id}", response_model=TodoItem, tags=["Todo Ажлууд"])
def update_todo(todo_id: int, todo_in: TodoUpdate):
    """Өгөгдсөн ID-тай ажлын мэдээллийг шинэчилнэ."""
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            # Зөвхөн хэрэглэгчийн илгээсэн талбаруудыг шинэчлэх
            update_data = todo_in.model_dump(exclude_unset=True) # Илгээгүй талбаруудыг орхих
            
            # Хуучин өгөгдлийг шинээр сольж шинэ TodoItem объект үүсгэх
            updated_todo = todo.model_copy(update=update_data)
            
            todo_db[index] = updated_todo
            return updated_todo
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID={todo_id} бүхий ажил олдсонгүй тул засах боломжгүй!"
    )


# ============================================================
# 📌 ХЭСЭГ 6: DELETE - Өгөгдөл Устгах (Delete)
# ============================================================

@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK, tags=["Todo Ажлууд"])
def delete_todo(todo_id: int):
    """Өгөгдсөн ID-тай ажлыг устгана."""
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            deleted_todo = todo_db.pop(index)
            return {"detail": f"ID={todo_id} бүхий ажлыг амжилттай устгалаа.", "deleted_item": deleted_todo}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID={todo_id} бүхий ажил олдсонгүй тул устгах боломжгүй!"
    )


# ============================================================
# ⚙️ Хэрхэн ажиллуулах заавар
# ============================================================
"""
Терминал дээр дараах тушаалаар серверээ асаана уу:
   uvicorn 07_web_api.01_fastapi_basics:app --reload

Сервер ассаны дараа хөтчөөрөө:
   - http://127.0.0.1:8000           <- Эхлэх хуудас
   - http://127.0.0.1:8000/docs      <- Автомат интерактив Swagger бичиг баримт
   - http://127.0.0.1:8000/redoc     <- Өөр загварын бичиг баримт
"""

# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 7.1.1:
   Хэрэглэгчийн мэдээллийн CRUD API-ийг Todo-той адил системээр нэмж бичнэ үү.
   
   Шаардлага:
   1. `User` (id: int, username: str, email: str, is_active: bool) гэсэн Pydantic модел үүсгэх.
   2. Санах ойд `user_db = [...]` жагсаалт бэлдэх.
   3. Дараах endpoint-уудыг нэмэх:
      - `GET /users` (Хэрэглэгчдийг жагсаалтаар авах, `is_active`-ээр шүүх боломжтой)
      - `GET /users/{user_id}` (Хэрэглэгчийг ID-аар авах, байхгүй бол 404 буцаах)
      - `POST /users` (Шинэ хэрэглэгч нэмэх, Email формат зөв эсэхийг Pydantic-оор шалгах)
      - `PUT /users/{user_id}` (Хэрэглэгчийн мэдээллийг шинэчлэх)
      - `DELETE /users/{user_id}` (Хэрэглэгчийг устгах)
   4. Серверээ дахин ажиллуулж, `/docs` хаяг руу хандан шинээр үүсгэсэн API-уудаа туршиж шалгаарай.
"""
