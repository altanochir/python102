"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 6.1: LangChain — LLM-тэй холбогдох & LCEL Гинжин Хэлхээ║
║  Python 102 — JavaScript/Node.js туршлагатай хөгжүүлэгчдэд       ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. ChatPromptTemplate ашиглан промпт удирдах
   2. Custom Chat Model үүсгэх (Offline / Mock горимоор ажиллуулах)
   3. LCEL (LangChain Expression Language) буюу `|` операторын хүч
   4. Гаралтыг цэгцлэх (StrOutputParser)

💡 JS програмист та бүхэнд:
   - JS-д бид `const chain = [step1, step2].reduce(...)` гэж бичдэг бол
     Python LangChain-д `chain = step1 | step2` гэсэн маш хялбар бичиглэл ашиглана.
   - Энэ `|` (pipe) операторыг Python-д "operator overloading" ашиглан хийсэн байдаг.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Шаардлагатай сангуудыг шалгах
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import BaseMessage, ChatMessage, AIMessage, HumanMessage
    from langchain_core.outputs import ChatResult, ChatGeneration
except ImportError:
    print("""
⚠️  LangChain сан суугаагүй байна!
Терминал дээр дараах тушаалаар суулгана уу:
    pip install langchain langchain-core
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: Mock Chat Model (Оффлайн орчинд турших зориулалттай)
# ============================================================
"""
Суралцагчид OpenAI эсвэл бусад төлбөртэй API түлхүүр (API Key) байхгүй байсан ч
энэ хичээлийг оффлайн байдлаар ажиллуулж, логикийг нь ойлгох боломжийг олгохын тулд
BaseChatModel-оос удамшсан Mock модель үүсгэе.
"""

class MockChatModel(BaseChatModel):
    """Сонгосон промпт дээр тулгуурлан хийсвэр хариулт өгөх оффлайн модел"""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        # Хэрэглэгчийн хамгийн сүүлд илгээсэн мессежийг авах
        last_message = messages[-1].content
        
        # Хэрэглэгчийн мессежийн агуулгаас хамааран тохирох хариулт өгөх
        prompt_text = str(messages)
        
        response_text = ""
        if "орчуул" in prompt_text.lower() or "translate" in prompt_text.lower():
            response_text = "Hello, how are you? (Энэ бол Mock орчуулга юм)"
        elif "жор" in prompt_text.lower() or "recipe" in prompt_text.lower():
            response_text = "1. Ус буцалгана.\n2. Цайны навч хийнэ.\n3. Сүү нэмээд буцалгана. (Энэ бол Mock цайны жор)"
        elif "ном" in prompt_text.lower() or "book" in prompt_text.lower():
            response_text = "Энэхүү ном нь хувь хүний хөгжил болон цаг төлөвлөлтийн тухай өгүүлдэг. (Mock хураангуй)"
        else:
            response_text = f"[Mock LLM Хариулт]: Би таны дараах хүсэлтийг хүлээн авлаа: '{last_message}'"

        # AI-ийн мессеж хэлбэрээр буцаах
        message = AIMessage(content=response_text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock-chat-model"


# ============================================================
# 📌 ХЭСЭГ 2: ChatPromptTemplate (Промптын загвар)
# ============================================================
"""
JS: const systemPrompt = `Та ${role} үүрэгтэй туслах юм.`;
Python LangChain: ChatPromptTemplate ашиглан Промптыг илүү цэгцтэй бүтэцжүүлнэ.
Энэ нь систем болон хэрэглэгчийн дүрүүдийг зааглаж өгдөг.
"""

def example_1_prompts():
    print("\n=== 1. ChatPromptTemplate Жишээ ===")
    
    # Промптын загвар үүсгэх
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Та {field} чиглэлээр мэргэшсэн Монгол хэлний багш юм. Хэрэглэгчийн асуултад энгийнээр тайлбарлаж хариулна уу."),
        ("user", "Дараах сэдвийг тайлбарлана уу: {topic}")
    ])
    
    # Динамик утгуудаа оноож промптыг бэлдэх
    formatted_prompt = prompt_template.invoke({
        "field": "Програмчлалын үндэс",
        "topic": "Индент буюу Кодын догол мөр"
    })
    
    print("Formatted Prompt (Промптын бэлэн бүтэц):")
    print(formatted_prompt)
    print("\nЗөвхөн мессежүүдийг харах:")
    for msg in formatted_prompt.to_messages():
        print(f"  [{msg.type.upper()}]: {msg.content}")


# ============================================================
# 📌 ХЭСЭГ 3: LCEL (LangChain Expression Language)
# ============================================================
"""
LCEL нь LangChain-ийн хамгийн хүчирхэг шинж чанар юм.
`|` (pipe) тэмдэгтийг ашиглан кодын блокуудыг гинжин холбоосонд оруулна.

Синтакс: chain = prompt | model | output_parser
"""

def example_2_lcel_chain():
    print("\n=== 2. LCEL Гинжин Хэлхээ (Chain) ===")
    
    # 1. Промпт үүсгэх
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Та англи хэлнээс монгол хэл рүү орчуулагч юм. Өгөгдсөн текстийг {accent} аялгаар орчуулна уу."),
        ("user", "Орчуулах текст: '{text}'")
    ])
    
    # 2. Модел сонгох (Хэрэв OpenAI ашиглах бол ChatOpenAI(api_key="...") гэж бичнэ)
    # Одоогоор бид өөрсдийн бичсэн оффлайн Mock моделийг ашиглана.
    model = MockChatModel()
    
    # 3. Гаралтыг хөрвүүлэгч (LLM-ийн AIMessage-ээс зөвхөн текстийг шүүж авах)
    parser = StrOutputParser()
    
    # 4. LCEL ашиглан хэлхээ үүсгэх
    # JS-д: const chain = (input) => parser(model(prompt(input)))
    # Python-д:
    chain = prompt | model | parser
    
    # 5. Хэлхээг ажиллуулах (invoke)
    print("Хэлхээг ажиллуулж байна...")
    result = chain.invoke({
        "accent": "Энгийн ярианы",
        "text": "Hello, how are you doing today?"
    })
    
    print("\nХариулт:")
    print(result)


# ============================================================
# 📌 ХЭСЭГ 4: Бодит LLM ашиглах (Сонголтоор)
# ============================================================
def example_3_real_llm():
    print("\n=== 3. Бодит OpenAI LLM ашиглах (Заавар) ===")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("💡 Мэдээлэл: Систем дээр OPENAI_API_KEY байхгүй байгаа тул бодит загварыг ажиллуулах боломжгүй.")
        print("Хэрэв та ажиллуулахыг хүсвэл дараах алхмыг хийнэ үү:")
        print("  1. 'pip install langchain-openai' суулгах")
        print("  2. Системийн environment variable дээр 'OPENAI_API_KEY' тохируулах")
        print("  3. Код дээр дараах байдлаар бичнэ:")
        print("""
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        """)
        return
        
    try:
        from langchain_openai import ChatOpenAI
        print("✅ OPENAI_API_KEY олдлоо. GPT-4o-mini загвартай холбогдож байна...")
        
        prompt = ChatPromptTemplate.from_template("Дараах сэдвээр 1 өгүүлбэрт багтаан хошин шог ярьж өгнө үү: {topic}")
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        parser = StrOutputParser()
        
        chain = prompt | model | parser
        
        topic = input("Хошигнох сэдэв оруулах: ").strip()
        if not topic:
            topic = "Код бичих"
            
        print("GPT хариулж байна...")
        print(chain.invoke({"topic": topic}))
        
    except ImportError:
        print("⚠️ 'langchain-openai' сан суугаагүй байна. Үүнийг 'pip install langchain-openai' гэж суулгана уу.")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🔗 LangChain Үндэс — Хичээл 6.1                  ║
║                                                  ║
║  Ямар сэдвийг ажиллуулж үзэх вэ?                 ║
║                                                  ║
║  1. 📝 ChatPromptTemplate (Промпт загварчлах)   ║
║  2. ⛓️  LCEL Chain (Mock оффлайн хэлхээ)           ║
║  3. 🧠 Бодит OpenAI LLM-тэй ажиллах (Хэрэв байгаа бол)║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-3): ").strip()
            if choice == "1":
                example_1_prompts()
            elif choice == "2":
                example_2_lcel_chain()
            elif choice == "3":
                example_3_real_llm()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-3 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break

# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 6.1.1:
   Хэрэглэгчээс "номын нэр" авч, тэрхүү номын "төрөл зүйл" болон "хураангуй"-г
   хэвлэдэг Chain үүсгэ.
   - Промпт нь систем болон хэрэглэгчийн гэсэн 2 хэсэгтэй байх.
   - Манай оффлайн `MockChatModel`-ийг ашиглаж хариултыг хэвлэж үзүүл.
   - Хэрэв боломжтой бол real LLM дээр турш.
"""
