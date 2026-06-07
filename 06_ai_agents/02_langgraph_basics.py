"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 6.2: LangGraph — Төлөвт суурилсан Агент & Router     ║
║  Python 102 — Ахисан түвшний Агент зохион бүтээх                 ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. State (Төлөв) гэж юу вэ? (TypedDict ашиглан тодорхойлох)
   2. Nodes (Зангилаа) ба Edges (Холбоосууд)
   3. Conditional Edges (Нөхцөлт холбоос) ашиглан Router Агент бүтээх
   4. Графыг хянах, ажиллуулах (StateGraph compile & invoke)

💡 Тайлбар:
   LangGraph нь агентын алхмуудыг Граф (хүрээ) хэлбэрээр дүрсэлдэг.
   Зангилаа (Node) бүр нь тодорхой функц бөгөөд "Төлөв"-ийг оролт болгон авч,
   өөрчлөлт оруулсан "Төлөв"-өө буцаадаг.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

# Шаардлагатай сангуудыг шалгах
try:
    from typing import TypedDict
    from langgraph.graph import StateGraph, START, END
except ImportError:
    print("""
⚠️  LangGraph сан суугаагүй байна!
Терминал дээр дараах тушаалаар суулгана уу:
    pip install langgraph
    """)
    sys.exit(1)


# ============================================================
# 📌 ХЭСЭГ 1: State (Төлөв) тодорхойлох
# ============================================================
"""
Төлөв (State) нь Графын бүх зангилаануудын дунд дундын санах ой (Shared Memory) болдог.
Python-ий `TypedDict`-ийг ашиглан төлөвт ямар өгөгдлүүд хадгалагдахыг заана.
"""

class AgentState(TypedDict):
    query: str         # Хэрэглэгчийн асуулт
    category: str      # Ангилал (billing, tech, general)
    response: str      # Эцсийн хариулт


# ============================================================
# 📌 ХЭСЭГ 2: Nodes (Зангилаанууд буюу Функцүүд)
# ============================================================
"""
Зангилаа бүр нь AgentState-ийг авч, тодорхой үйлдэл хийгээд шинэчлэгдсэн төлөвийг буцаана.
Синтакс: def node_func(state: AgentState) -> dict: ...
Буцааж буй dict нь State доторх ижил нэртэй түлхүүрүүдийн утгыг автоматаар шинэчилнэ.
"""

# 1. Ангилагч зангилаа (Classifier Node)
def classify_node(state: AgentState):
    print("\n🔍 [Classifier Node]: Хэрэглэгчийн асуултыг шинжилж байна...")
    query = state["query"].lower()
    
    # Бодит төсөл дээр энд LLM ашиглан ангилалт хийнэ.
    # Бид оффлайн ажиллуулахын тулд энгийн түлхүүр үг шалгах логик бичье.
    if any(word in query for word in ["төлбөр", "мөнгө", "нэхэмжлэх", "үнэ", "billing", "money"]):
        category = "billing"
    elif any(word in query for word in ["алдаа", "ажиллахгүй", "код", "гацчихлаа", "error", "bug"]):
        category = "tech"
    else:
        category = "general"
        
    print(f"   ↳ Ангилал: {category.upper()}")
    return {"category": category}


# 2. Санхүүгийн туслах зангилаа (Billing Specialist Node)
def billing_node(state: AgentState):
    print("💰 [Billing Node]: Санхүүгийн туслах хариу бэлдэж байна...")
    query = state["query"]
    # Оффлайн Mock хариулт
    response = f"[Санхүүгийн Хэлтэс]: Таны төлбөртэй холбоотой хүсэлтийг ('{query}') хүлээн авлаа. Манай санхүүгийн ажилтан ажлын 2 цагт багтан тантай холбогдох болно."
    return {"response": response}


# 3. Техник туслах зангилаа (Tech Support Node)
def tech_node(state: AgentState):
    print("💻 [Tech Node]: Техникийн туслах хариу бэлдэж байна...")
    query = state["query"]
    # Оффлайн Mock хариулт
    response = f"[Техник Тусламж]: Таны системийн алдааны тухай мэдээллийг ('{query}') шалгаж байна. Програмыг унтраагаад дахин асааж үзнэ үү. Хэрэв болохгүй бол log файлаа илгээнэ үү."
    return {"response": response}


# 4. Ерөнхий туслах зангилаа (General Node)
def general_node(state: AgentState):
    print("🤖 [General Node]: Ерөнхий туслах хариу бэлдэж байна...")
    query = state["query"]
    # Оффлайн Mock хариулт
    response = f"[Ерөнхий Туслах]: Сайн байна уу! Танд өөр ямар асуулт байна вэ? (Таны асуулт: '{query}')"
    return {"response": response}


# ============================================================
# 📌 ХЭСЭГ 3: Edges (Холбоосууд) болон Router функц
# ============================================================
"""
Router функц нь төлөвөөс хамаарч дараагийн алхамд аль зангилаа руу шилжихийг шийднэ.
"""

def route_decision(state: AgentState):
    # Ангилсан категорийг уншиж, тохирох зангилааны нэрийг буцаана
    category = state["category"]
    if category == "billing":
        return "billing"
    elif category == "tech":
        return "tech"
    else:
        return "general"


# ============================================================
# 📌 ХЭСЭГ 4: Граф Угсрах & Ажиллуулах (StateGraph)
# ============================================================

def build_agent_graph():
    # 1. Графын бүтцийг тодорхойлно (Төлөвийг дамжуулна)
    workflow = StateGraph(AgentState)
    
    # 2. Зангилаануудаа нэмнэ
    workflow.add_node("classify", classify_node)
    workflow.add_node("billing_agent", billing_node)
    workflow.add_node("tech_agent", tech_node)
    workflow.add_node("general_agent", general_node)
    
    # 3. Холбоосуудыг тохируулна
    # Эхлэх цэг -> classify зангилаа руу
    workflow.add_edge(START, "classify")
    
    # classify-оос дараагийн зангилаа руу шилжихдээ Router функц ашиглана
    workflow.add_conditional_edges(
        "classify",            # Аль зангилааны дараа шилжих вэ
        route_decision,        # Шилжилтийг шийдэх функц
        {
            "billing": "billing_agent",   # Хэрэв billing гэж буцаавал billing_agent руу
            "tech": "tech_agent",         # Хэрэв tech гэж буцаавал tech_agent руу
            "general": "general_agent"    # Хэрэв general гэж буцаавал general_agent руу
        }
    )
    
    # Агентууд хариултаа бэлдээд шууд дуусна (END)
    workflow.add_edge("billing_agent", END)
    workflow.add_edge("tech_agent", END)
    workflow.add_edge("general_agent", END)
    
    # 4. Графыг ажиллуулахад бэлэн болгож хөрвүүлнэ (Compile)
    app = workflow.compile()
    return app


# ============================================================
# 📌 Ажиллуулж турших хэсэг
# ============================================================

def run_agent_demo():
    print("\n--- LangGraph Агентыг ажиллуулж байна ---")
    app = build_agent_graph()
    
    # Сонгох асуултууд
    test_queries = [
        "Миний нэхэмжлэх дээр 50,000 төгрөг илүү бодогдсон байна. Шалгаад өгөөч.",
        "Програм ажиллахгүй байна, хөгжүүлэлтийн явцад ImportError: No module named 'langgraph' алдаа заалаа.",
        "Танай компани хаана байрладаг вэ? Хаягаа хэлнэ үү."
    ]
    
    for i, query in enumerate(test_queries, start=1):
        print(f"\n================ Тест {i} ================")
        print(f"Хэрэглэгчийн асуулт: '{query}'")
        
        # Эхний төлөвт зөвхөн query-ийг өгч ажиллуулна
        initial_state = {"query": query, "category": "", "response": ""}
        final_state = app.invoke(initial_state)
        
        print("\n📥 [Эцсийн Төлөв (Final State)]:")
        print(f"   Ангилал (Category): {final_state['category']}")
        print(f"   Агентын Хариулт (Response): {final_state['response']}")


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🕸️  LangGraph Үндэс — Хичээл 6.2                 ║
║                                                  ║
║  1. 🤖 Харилцагчийн үйлчилгээний Router Агент    ║
║  0. 🚪 Гарах                                     ║
╚══════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input("Сонголт (0-1): ").strip()
            if choice == "1":
                run_agent_demo()
            elif choice == "0":
                print("👋 Баяртай!")
                break
            else:
                print("⚠️ 0-1 хооронд сонгоно уу!")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n👋 Баяртай!")
            break

# ============================================================
# 🏋️ ДАСГАЛ АЖИЛ
# ============================================================
"""
✏️ Дасгал 6.2.1:
   Дээрх агентын бүтцэд "Маргаан үүсгэх" (dispute_agent) гэсэн шинэ зангилаа нэмнэ үү.
   - Хэрэв хэрэглэгчийн асуултад "гомдол", "хэрүүл", "шүүх", "буруу" гэх мэт үг орсон байвал
     'dispute' ангилалд оруулна.
   - Dispute зангилаа нь тусгай урамшуулал эсвэл менежертэй холбох хариу бэлдэнэ.
   - Графын шилжилт (Router) болон холбоосуудыг шинэчлэн ажиллуулж шалгаарай.
"""
