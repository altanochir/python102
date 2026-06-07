# 🌐 Хэсэг 7: Web API Хөгжүүлэлт — FastAPI-ийн Үндэс

Орчин үеийн вэб хөгжүүлэлтэд хурдан, аюулгүй, хэрэглэхэд хялбар API бүтээх нь хамгийн чухал асуудлын нэг юм. Энэхүү бүлгээр бид Python хэлний хамгийн эрэлттэй, орчин үеийн вэб фреймворк болох **FastAPI**-ийг судалж, REST API хөгжүүлэх суурь ойлголтуудыг үзэх болно.

---

## ⚡ FastAPI гэж юу вэ? Яагаад хэрэглэх ёстой вэ?

**FastAPI** нь Python 3.8+ хувилбарын стандарт Type Hints (төрөл заалт)-д суурилсан, өндөр бүтээмжтэй (High Performance) вэб фреймворк юм.

Гол давуу талууд:
1. **Маш хурдан (Fast)**: NodeJS (Express.js) болон Go хэлтэй дүйцэхүйц маш өндөр хурдтай. (Starlette болон Uvicorn сангууд дээр суурилсан).
2. **Автомат бичиг баримт (Auto Docs)**: Кодоо бичихэд автоматаар OpenAPI (Swagger UI) болон ReDoc интерфейс үүсэж, API-уудыг хөтөч дээрээс шууд турших боломжтой болдог.
3. **Pydantic-ийн хүч**: Хүсэлтийн өгөгдлийг шалгах (Validation) болон хөрвүүлэх үйлдлийг Python-ийн `Pydantic` сан автоматаар гүйцэтгэнэ.
4. **Асинхрон дэмжлэг (Async/Await)**: Node.js шиг асинхрон (non-blocking) кодыг шууд бичих боломжтой.

---

## ⚔️ Express.js vs FastAPI: Харьцуулалт

JS (Express.js) хөгжүүлэгчдэд зориулсан синтаксын дүйцэл:

| Үйлдэл | Express.js (JavaScript) | FastAPI (Python) |
| :--- | :--- | :--- |
| **Фреймворк эхлүүлэх** | `const app = express();` | `app = FastAPI()` |
| **GET хүсэлт** | `app.get("/items", (req, res) => ...)` | `@app.get("/items") def get_items(): ...` |
| **Path Parameter** | `/items/:id` (`req.params.id`) | `/items/{id}` (`id: int` параметр) |
| **Query Parameter** | `/items?limit=10` (`req.query.limit`) | `/items` (`limit: int = 10` параметр) |
| **Request Body** | `req.body` (Zod эсвэл Joi-оор шалгадаг) | `Pydantic BaseModel` ашиглан автоматаар шалгана |
| **Ажиллуулах** | `node app.js` эсвэл `nodemon` | `uvicorn main:app --reload` |

---

## 📌 Шаардлагатай сангуудыг суулгах

FastAPI-ийг ажиллуулахад ASGI вэб сервер (Uvicorn) хэрэгтэй болно.

```bash
# Идэвхтэй виртуал орчин (venv) дотор дараах тушаалыг ажиллуулна:
pip install fastapi uvicorn
```

---

## 🚀 Хэрхэн ажиллуулж шалгах вэ?

1. Дараах тушаалаар FastAPI серверээ асаана:
   ```bash
   uvicorn 07_web_api.01_fastapi_basics:app --reload
   ```
2. Сервер ассаны дараа хөтчөө нээж:
   - **Үндсэн хаяг**: `http://127.0.0.1:8000`
   - **Автомат бичиг баримт (Swagger UI)**: `http://127.0.0.1:8000/docs` руу хандаж туршаарай.
