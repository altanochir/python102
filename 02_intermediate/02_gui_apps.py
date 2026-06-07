"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 2.2: Tkinter — Бодит Програмууд                     ║
║  Python 102 — Visual Basic туршлагатай програмистад зориулсан    ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - Menu бүтээх (VB: MenuBar)
   - Listbox + CRUD үйлдлүүд
   - Treeview (хүснэгт)
   - Олон цонхтой програм (Toplevel)
   - Бодит програм: Todo List, Тэмдэглэлийн дэвтэр

💡 Энэ хичээлд VB-ийн бодит төслүүдтэй адилхан
   програмуудыг Python-оор бүтээнэ!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
import json
import os


# ============================================================
# 📌 ЖИШЭЭ 1: Todo List Програм (Бүрэн CRUD!)
# ============================================================

def todo_app():
    """📋 Todo List — VB-ийн сонгодог ListBox + Button програм"""

    # --- Өнгөний тохиргоо (Catppuccin Mocha theme) ---
    COLORS = {
        "bg": "#1e1e2e",
        "surface": "#313244",
        "overlay": "#45475a",
        "text": "#cdd6f4",
        "subtext": "#a6adc8",
        "blue": "#89b4fa",
        "green": "#a6e3a1",
        "red": "#f38ba8",
        "yellow": "#f9e2af",
        "mauve": "#cba6f7",
    }

    window = tk.Tk()
    window.title("📋 Todo List")
    window.geometry("500x650")
    window.configure(bg=COLORS["bg"])
    window.resizable(False, False)

    # --- Өгөгдөл ---
    todos = []  # [{"text": "...", "done": False, "created": "..."}, ...]

    # === ГАРЧИГ ===
    header_frame = tk.Frame(window, bg=COLORS["bg"])
    header_frame.pack(fill="x", padx=15, pady=(15, 5))

    tk.Label(
        header_frame, text="📋", font=("Arial", 28),
        bg=COLORS["bg"]
    ).pack(side="left")

    tk.Label(
        header_frame, text="Todo List",
        font=("Arial", 24, "bold"), fg=COLORS["text"], bg=COLORS["bg"]
    ).pack(side="left", padx=10)

    count_label = tk.Label(
        header_frame, text="0 даалгавар",
        font=("Arial", 10), fg=COLORS["subtext"], bg=COLORS["bg"]
    )
    count_label.pack(side="right")

    # === ОРОЛТ (Entry + Button) ===
    input_frame = tk.Frame(window, bg=COLORS["bg"])
    input_frame.pack(fill="x", padx=15, pady=10)

    entry = tk.Entry(
        input_frame, font=("Arial", 13), bg=COLORS["surface"],
        fg=COLORS["text"], insertbackground=COLORS["text"],
        relief="flat", width=35
    )
    entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

    add_btn = tk.Button(
        input_frame, text="➕ Нэмэх", font=("Arial", 11, "bold"),
        bg=COLORS["blue"], fg=COLORS["bg"], relief="flat",
        padx=15, pady=6, cursor="hand2"
    )
    add_btn.pack(side="right")

    # === ЖАГСААЛТ (Listbox + Scrollbar) ===
    list_frame = tk.Frame(window, bg=COLORS["bg"])
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(
        list_frame,
        font=("Arial", 13),
        bg=COLORS["surface"],
        fg=COLORS["text"],
        selectbackground=COLORS["blue"],
        selectforeground=COLORS["bg"],
        relief="flat",
        activestyle="none",
        yscrollcommand=scrollbar.set,
        height=15,
    )
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    # === ТОВЧНУУД ===
    btn_frame = tk.Frame(window, bg=COLORS["bg"])
    btn_frame.pack(fill="x", padx=15, pady=5)

    def make_btn(parent, text, color, cmd):
        return tk.Button(
            parent, text=text, font=("Arial", 10),
            bg=color, fg="white" if color in [COLORS["red"]] else COLORS["bg"],
            relief="flat", padx=12, pady=4, cursor="hand2", command=cmd
        )

    # === ФУНКЦҮҮД (VB: Private Sub ...) ===

    def refresh_list():
        """Жагсаалтыг шинэчлэх"""
        listbox.delete(0, tk.END)
        for i, todo in enumerate(todos):
            prefix = "✅" if todo["done"] else "⬜"
            listbox.insert(tk.END, f"  {prefix}  {todo['text']}")
            if todo["done"]:
                listbox.itemconfig(i, fg=COLORS["subtext"])

        done_count = sum(1 for t in todos if t["done"])
        total = len(todos)
        count_label.config(text=f"{done_count}/{total} дууссан")

    def add_todo(event=None):
        """Даалгавар нэмэх — VB: cmdAdd_Click()"""
        text = entry.get().strip()
        if not text:
            return

        todos.append({
            "text": text,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        entry.delete(0, tk.END)
        refresh_list()

    def toggle_done():
        """Дууссан/Дуусаагүй — VB: cmdToggle_Click()"""
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("ℹ️", "Даалгавар сонгоно уу!")
            return

        idx = sel[0]
        todos[idx]["done"] = not todos[idx]["done"]
        refresh_list()

    def delete_todo():
        """Устгах — VB: cmdDelete_Click()"""
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("ℹ️", "Даалгавар сонгоно уу!")
            return

        idx = sel[0]
        if messagebox.askyesno("🗑️ Устгах", f"'{todos[idx]['text']}' устгах уу?"):
            todos.pop(idx)
            refresh_list()

    def edit_todo():
        """Засах"""
        sel = listbox.curselection()
        if not sel:
            return

        idx = sel[0]
        new_text = simpledialog.askstring(
            "✏️ Засах",
            "Шинэ текст:",
            initialvalue=todos[idx]["text"]
        )
        if new_text:
            todos[idx]["text"] = new_text.strip()
            refresh_list()

    def clear_done():
        """Дууссан бүгдийг устгах"""
        nonlocal todos
        done_count = sum(1 for t in todos if t["done"])
        if done_count == 0:
            messagebox.showinfo("ℹ️", "Дууссан даалгавар байхгүй!")
            return

        if messagebox.askyesno("🧹 Цэвэрлэх", f"{done_count} дууссан даалгавар устгах уу?"):
            todos = [t for t in todos if not t["done"]]
            refresh_list()

    def save_todos():
        """Файлд хадгалах — VB: CommonDialog.ShowSave"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Хадгалах"
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("✅", f"Хадгаллаа!\n{filepath}")

    def load_todos():
        """Файлаас уншиж ачаалах — VB: CommonDialog.ShowOpen"""
        nonlocal todos
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Нээх"
        )
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                todos = json.load(f)
            refresh_list()
            messagebox.showinfo("✅", f"Ачааллаа! ({len(todos)} даалгавар)")

    # --- Товчнуудыг нэмэх ---
    make_btn(btn_frame, "✅ Дууссан", COLORS["green"], toggle_done).pack(side="left", padx=3)
    make_btn(btn_frame, "✏️ Засах", COLORS["yellow"], edit_todo).pack(side="left", padx=3)
    make_btn(btn_frame, "🗑️ Устгах", COLORS["red"], delete_todo).pack(side="left", padx=3)
    make_btn(btn_frame, "🧹 Цэвэрлэх", COLORS["mauve"], clear_done).pack(side="left", padx=3)

    # === ХАДГАЛАХ/АЧААЛАХ ТОВЧ ===
    io_frame = tk.Frame(window, bg=COLORS["bg"])
    io_frame.pack(fill="x", padx=15, pady=5)

    make_btn(io_frame, "💾 Хадгалах", COLORS["overlay"], save_todos).pack(side="left", padx=3)
    make_btn(io_frame, "📂 Ачаалах", COLORS["overlay"], load_todos).pack(side="left", padx=3)

    # === EVENT BINDING ===
    entry.bind("<Return>", add_todo)               # Enter = Нэмэх
    add_btn.config(command=add_todo)
    listbox.bind("<Double-Button-1>", lambda e: toggle_done())  # Давхар дарах = Toggle

    # Placeholder текст
    entry.insert(0, "Шинэ даалгавар бичнэ үү...")
    entry.config(fg=COLORS["subtext"])

    def on_entry_focus_in(e):
        if entry.get() == "Шинэ даалгавар бичнэ үү...":
            entry.delete(0, tk.END)
            entry.config(fg=COLORS["text"])

    def on_entry_focus_out(e):
        if not entry.get():
            entry.insert(0, "Шинэ даалгавар бичнэ үү...")
            entry.config(fg=COLORS["subtext"])

    entry.bind("<FocusIn>", on_entry_focus_in)
    entry.bind("<FocusOut>", on_entry_focus_out)

    # Жишээ даалгаврууд
    for text in ["Python GUI сурах 🐍", "Тооцоолуур бүтээх 🔢", "Todo app дуусгах ✅"]:
        todos.append({"text": text, "done": False, "created": datetime.now().strftime("%Y-%m-%d %H:%M")})
    refresh_list()

    window.mainloop()


# ============================================================
# 📌 ЖИШЭЭ 2: Тэмдэглэлийн Дэвтэр (Notepad clone!)
# ============================================================

def notepad_app():
    """📝 Тэмдэглэл — VB-ийн Notepad шиг програм"""

    window = tk.Tk()
    window.title("📝 Тэмдэглэл — Нэргүй")
    window.geometry("700x500")
    window.configure(bg="#1e1e2e")

    current_file = [None]   # Одоогийн файлын зам

    # === MENU BAR (VB: Menu Editor) ===
    menubar = tk.Menu(window, bg="#313244", fg="#cdd6f4", activebackground="#89b4fa")

    # --- Файл цэс ---
    file_menu = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4")
    menubar.add_cascade(label="📁 Файл", menu=file_menu)

    # --- Засварлах цэс ---
    edit_menu = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4")
    menubar.add_cascade(label="✏️ Засвар", menu=edit_menu)

    # --- Харах цэс ---
    view_menu = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4")
    menubar.add_cascade(label="👁️ Харах", menu=view_menu)

    # --- Тусламж цэс ---
    help_menu = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4")
    menubar.add_cascade(label="❓ Тусламж", menu=help_menu)

    window.config(menu=menubar)

    # === TOOLBAR (VB: Toolbar) ===
    toolbar = tk.Frame(window, bg="#313244", height=35)
    toolbar.pack(fill="x")

    def toolbar_btn(text, cmd):
        btn = tk.Button(
            toolbar, text=text, font=("Arial", 10),
            bg="#313244", fg="#cdd6f4", relief="flat",
            padx=8, cursor="hand2", command=cmd,
            activebackground="#45475a"
        )
        btn.pack(side="left", padx=1, pady=3)
        return btn

    # === ТЕКСТ ТАЛБАР (VB: RichTextBox) ===
    text_frame = tk.Frame(window, bg="#1e1e2e")
    text_frame.pack(fill="both", expand=True)

    # Мөрийн дугаар
    line_numbers = tk.Text(
        text_frame, width=4, font=("Consolas", 12),
        bg="#181825", fg="#585b70", relief="flat",
        state="disabled", padx=5
    )
    line_numbers.pack(side="left", fill="y")

    # Scrollbar
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    # Текст
    text_area = tk.Text(
        text_frame,
        font=("Consolas", 12),
        bg="#1e1e2e",
        fg="#cdd6f4",
        insertbackground="#89b4fa",
        selectbackground="#45475a",
        selectforeground="#cdd6f4",
        relief="flat",
        undo=True,                       # VB: Undo боломж!
        wrap="word",
        padx=10,
        pady=5,
        yscrollcommand=scrollbar.set,
    )
    text_area.pack(fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # === СТАТУС МӨР (VB: StatusBar) ===
    status_bar = tk.Frame(window, bg="#181825", height=25)
    status_bar.pack(fill="x")

    status_left = tk.Label(
        status_bar, text="🟢 Бэлэн",
        font=("Arial", 9), fg="#a6adc8", bg="#181825", anchor="w"
    )
    status_left.pack(side="left", padx=10)

    status_right = tk.Label(
        status_bar, text="Мөр: 1, Багана: 1",
        font=("Arial", 9), fg="#a6adc8", bg="#181825", anchor="e"
    )
    status_right.pack(side="right", padx=10)

    # === ФУНКЦҮҮД ===

    def update_title():
        name = os.path.basename(current_file[0]) if current_file[0] else "Нэргүй"
        window.title(f"📝 Тэмдэглэл — {name}")

    def update_line_numbers(event=None):
        """Мөрийн дугаарыг шинэчлэх"""
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", tk.END)

        line_count = int(text_area.index("end-1c").split(".")[0])
        numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        line_numbers.insert("1.0", numbers)
        line_numbers.config(state="disabled")

    def update_cursor_pos(event=None):
        """Курсорын байрлалыг шинэчлэх"""
        pos = text_area.index(tk.INSERT)
        line, col = pos.split(".")
        status_right.config(text=f"Мөр: {line}, Багана: {int(col) + 1}")

    def new_file():
        """Шинэ файл — VB: mnuNew_Click()"""
        if text_area.get("1.0", tk.END).strip():
            if not messagebox.askyesno("❓", "Хадгалаагүй өөрчлөлт байна. Үргэлжлүүлэх үү?"):
                return
        text_area.delete("1.0", tk.END)
        current_file[0] = None
        update_title()
        status_left.config(text="📄 Шинэ файл")

    def open_file():
        """Файл нээх — VB: mnuOpen_Click() + CommonDialog"""
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Текст файл", "*.txt"),
                ("Python файл", "*.py"),
                ("Бүх файл", "*.*"),
            ]
        )
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", content)
            current_file[0] = filepath
            update_title()
            update_line_numbers()
            status_left.config(text=f"📂 Нээлээ: {os.path.basename(filepath)}")

    def save_file():
        """Хадгалах — VB: mnuSave_Click()"""
        if current_file[0]:
            with open(current_file[0], "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
            status_left.config(text=f"💾 Хадгаллаа: {os.path.basename(current_file[0])}")
        else:
            save_as()

    def save_as():
        """Өөр нэрээр хадгалах — VB: mnuSaveAs_Click()"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текст файл", "*.txt"), ("Python файл", "*.py"), ("Бүх файл", "*.*")]
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
            current_file[0] = filepath
            update_title()
            status_left.config(text=f"💾 Хадгаллаа: {os.path.basename(filepath)}")

    # === ЦЭСИЙН ЗҮЙЛҮҮД НЭМЭХ ===
    file_menu.add_command(label="📄 Шинэ", command=new_file, accelerator="Ctrl+N")
    file_menu.add_command(label="📂 Нээх...", command=open_file, accelerator="Ctrl+O")
    file_menu.add_command(label="💾 Хадгалах", command=save_file, accelerator="Ctrl+S")
    file_menu.add_command(label="💾 Өөр нэрээр...", command=save_as, accelerator="Ctrl+Shift+S")
    file_menu.add_separator()
    file_menu.add_command(label="🚪 Гарах", command=window.destroy, accelerator="Alt+F4")

    edit_menu.add_command(label="↩️ Буцаах (Undo)", command=lambda: text_area.edit_undo(), accelerator="Ctrl+Z")
    edit_menu.add_command(label="↪️ Дахих (Redo)", command=lambda: text_area.edit_redo(), accelerator="Ctrl+Y")
    edit_menu.add_separator()
    edit_menu.add_command(label="✂️ Тасдах", command=lambda: text_area.event_generate("<<Cut>>"), accelerator="Ctrl+X")
    edit_menu.add_command(label="📋 Хуулах", command=lambda: text_area.event_generate("<<Copy>>"), accelerator="Ctrl+C")
    edit_menu.add_command(label="📌 Буулгах", command=lambda: text_area.event_generate("<<Paste>>"), accelerator="Ctrl+V")
    edit_menu.add_separator()
    edit_menu.add_command(label="🔍 Бүгдийг сонгох", command=lambda: text_area.tag_add("sel", "1.0", tk.END), accelerator="Ctrl+A")

    # Фонтын хэмжээ
    font_size = [12]

    def change_font_size(delta):
        font_size[0] = max(8, min(32, font_size[0] + delta))
        text_area.config(font=("Consolas", font_size[0]))
        status_left.config(text=f"🔤 Фонт: {font_size[0]}pt")

    view_menu.add_command(label="🔍 Томруулах", command=lambda: change_font_size(2), accelerator="Ctrl++")
    view_menu.add_command(label="🔍 Жижигрүүлэх", command=lambda: change_font_size(-2), accelerator="Ctrl+-")

    # Word count
    def word_count():
        content = text_area.get("1.0", tk.END)
        chars = len(content) - 1
        words = len(content.split())
        lines = content.count("\n")
        messagebox.showinfo("📊 Тоо", f"Тэмдэгт: {chars}\nҮг: {words}\nМөр: {lines}")

    view_menu.add_separator()
    view_menu.add_command(label="📊 Үг тоолох", command=word_count)

    help_menu.add_command(label="ℹ️ Тухай", command=lambda: messagebox.showinfo(
        "ℹ️ Тухай",
        "📝 Тэмдэглэл v1.0\n\nPython Tkinter ашиглан бүтээсэн.\nHичээл 2.2 — Python 102"
    ))

    # === TOOLBAR ТОВЧНУУД ===
    toolbar_btn("📄", new_file)
    toolbar_btn("📂", open_file)
    toolbar_btn("💾", save_file)
    tk.Label(toolbar, text="|", fg="#45475a", bg="#313244").pack(side="left", padx=3)
    toolbar_btn("🔍+", lambda: change_font_size(2))
    toolbar_btn("🔍-", lambda: change_font_size(-2))

    # === KEYBOARD SHORTCUTS (VB: KeyDown event) ===
    window.bind("<Control-n>", lambda e: new_file())
    window.bind("<Control-o>", lambda e: open_file())
    window.bind("<Control-s>", lambda e: save_file())
    window.bind("<Control-plus>", lambda e: change_font_size(2))
    window.bind("<Control-minus>", lambda e: change_font_size(-2))

    # === EVENT BINDING ===
    text_area.bind("<KeyRelease>", lambda e: (update_line_numbers(), update_cursor_pos()))
    text_area.bind("<ButtonRelease-1>", update_cursor_pos)

    # Эхний мөрийн дугаар
    update_line_numbers()

    # Жишээ текст
    text_area.insert("1.0", """# 📝 Python Тэмдэглэл
# Энэ бол таны тэмдэглэлийн дэвтэр юм!

# Та энд Python код бичиж, хадгалж болно.
# Ctrl+S = Хадгалах
# Ctrl+O = Нээх
# Ctrl+N = Шинэ

print("Hello from Notepad! 🐍")

# Файл цэсээс бусад сонголтуудыг харна уу.
""")
    update_line_numbers()

    window.mainloop()


# ============================================================
# 📌 ЖИШЭЭ 3: Хэрэглэгчдийн Хүснэгт (Treeview)
# ============================================================

def table_app():
    """📊 Хэрэглэгчдийн хүснэгт — VB DataGrid / ListView шиг"""

    window = tk.Tk()
    window.title("📊 Хэрэглэгчдийн Жагсаалт")
    window.geometry("700x500")
    window.configure(bg="#1e1e2e")

    COLORS = {
        "bg": "#1e1e2e", "surface": "#313244",
        "text": "#cdd6f4", "blue": "#89b4fa",
        "green": "#a6e3a1", "red": "#f38ba8", "yellow": "#f9e2af",
    }

    # Гарчиг
    tk.Label(
        window, text="📊 Хэрэглэгчдийн Жагсаалт",
        font=("Arial", 18, "bold"), fg=COLORS["blue"], bg=COLORS["bg"]
    ).pack(pady=10)

    # === ХАЙЛТЫН ХЭСЭГ ===
    search_frame = tk.Frame(window, bg=COLORS["bg"])
    search_frame.pack(fill="x", padx=15, pady=5)

    tk.Label(search_frame, text="🔍", font=("Arial", 12), bg=COLORS["bg"]).pack(side="left")
    search_entry = tk.Entry(
        search_frame, font=("Arial", 12), bg=COLORS["surface"],
        fg=COLORS["text"], insertbackground=COLORS["text"],
        relief="flat", width=30
    )
    search_entry.pack(side="left", padx=5, ipady=4)

    # === TREEVIEW (Хүснэгт) ===
    # VB:  ListView / DataGrid / MSFlexGrid
    tree_frame = tk.Frame(window, bg=COLORS["bg"])
    tree_frame.pack(fill="both", expand=True, padx=15, pady=5)

    # Стиль
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                     background=COLORS["surface"],
                     foreground=COLORS["text"],
                     fieldbackground=COLORS["surface"],
                     font=("Arial", 11),
                     rowheight=30)
    style.configure("Custom.Treeview.Heading",
                     background="#45475a",
                     foreground=COLORS["text"],
                     font=("Arial", 11, "bold"))
    style.map("Custom.Treeview",
              background=[("selected", COLORS["blue"])],
              foreground=[("selected", COLORS["bg"])])

    columns = ("id", "name", "email", "age", "city", "status")
    tree = ttk.Treeview(
        tree_frame, columns=columns, show="headings",
        style="Custom.Treeview", height=12
    )

    # Баганы тохиргоо
    tree.heading("id", text="ID")
    tree.heading("name", text="Нэр")
    tree.heading("email", text="И-мэйл")
    tree.heading("age", text="Нас")
    tree.heading("city", text="Хот")
    tree.heading("status", text="Статус")

    tree.column("id", width=40, anchor="center")
    tree.column("name", width=100)
    tree.column("email", width=180)
    tree.column("age", width=50, anchor="center")
    tree.column("city", width=100)
    tree.column("status", width=80, anchor="center")

    tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)

    tree.pack(side="left", fill="both", expand=True)
    tree_scroll.pack(side="right", fill="y")

    # === ӨГӨГДӨЛ ===
    users = [
        (1, "Болд", "bold@email.mn", 25, "Улаанбаатар", "✅ Идэвхтэй"),
        (2, "Дорж", "dorj@email.mn", 30, "Дархан", "✅ Идэвхтэй"),
        (3, "Сараа", "saraa@email.mn", 22, "Эрдэнэт", "⏸️ Түр зогсоосон"),
        (4, "Түмэн", "tumen@email.mn", 28, "Чойбалсан", "✅ Идэвхтэй"),
        (5, "Оюука", "oyuka@email.mn", 35, "Улаанбаатар", "❌ Идэвхгүй"),
        (6, "Баатар", "baatar@email.mn", 27, "Дархан", "✅ Идэвхтэй"),
        (7, "Цэцэг", "tsetseg@email.mn", 24, "Улаанбаатар", "✅ Идэвхтэй"),
        (8, "Ганбат", "ganbat@email.mn", 40, "Ховд", "⏸️ Түр зогсоосон"),
    ]

    def load_data(filter_text=""):
        """Өгөгдөл ачаалах (шүүлттэй)"""
        tree.delete(*tree.get_children())
        for user in users:
            if filter_text.lower() in str(user).lower():
                tree.insert("", tk.END, values=user)

    load_data()

    # Хайлтын шүүлт
    def on_search(event=None):
        load_data(search_entry.get())

    search_entry.bind("<KeyRelease>", on_search)

    # === ТОВЧНУУД ===
    btn_frame = tk.Frame(window, bg=COLORS["bg"])
    btn_frame.pack(fill="x", padx=15, pady=10)

    def add_user():
        name = simpledialog.askstring("➕ Нэмэх", "Нэр:")
        if name:
            email = simpledialog.askstring("➕ Нэмэх", "И-мэйл:")
            age = simpledialog.askinteger("➕ Нэмэх", "Нас:")
            if email and age:
                new_id = max(u[0] for u in users) + 1
                user = (new_id, name, email, age, "Улаанбаатар", "✅ Идэвхтэй")
                users.append(user)
                load_data()

    def delete_user():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("ℹ️", "Хэрэглэгч сонгоно уу!")
            return
        values = tree.item(sel[0])["values"]
        if messagebox.askyesno("🗑️ Устгах", f"'{values[1]}' устгах уу?"):
            users[:] = [u for u in users if u[0] != values[0]]
            load_data()

    def view_details():
        sel = tree.selection()
        if not sel:
            return
        values = tree.item(sel[0])["values"]
        messagebox.showinfo("👤 Дэлгэрэнгүй",
                            f"ID: {values[0]}\nНэр: {values[1]}\nИ-мэйл: {values[2]}\n"
                            f"Нас: {values[3]}\nХот: {values[4]}\nСтатус: {values[5]}")

    for text, color, cmd in [
        ("➕ Нэмэх", COLORS["green"], add_user),
        ("🗑️ Устгах", COLORS["red"], delete_user),
        ("👤 Дэлгэрэнгүй", COLORS["blue"], view_details),
    ]:
        tk.Button(
            btn_frame, text=text, font=("Arial", 11),
            bg=color, fg=COLORS["bg"], relief="flat",
            padx=15, pady=5, cursor="hand2", command=cmd
        ).pack(side="left", padx=5)

    # Давхар дарах = Дэлгэрэнгүй
    tree.bind("<Double-Button-1>", lambda e: view_details())

    # Статус
    tk.Label(
        window, text=f"📊 Нийт: {len(users)} хэрэглэгч",
        font=("Arial", 9), fg="#a6adc8", bg="#181825", anchor="w"
    ).pack(fill="x", padx=0, ipady=3)

    window.mainloop()


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🐍 Python GUI — Бодит Програмууд (2.2)         ║
║                                                  ║
║  Ямар програм ажиллуулах вэ?                    ║
║                                                  ║
║  1. 📋  Todo List (CRUD)                        ║
║  2. 📝  Тэмдэглэлийн Дэвтэр (Notepad)         ║
║  3. 📊  Хэрэглэгчдийн Хүснэгт (Table)         ║
║  0. 🚪  Гарах                                    ║
╚══════════════════════════════════════════════════╝
    """)

    while True:
        choice = input("Сонголт (0-3): ").strip()

        match choice:
            case "1":
                todo_app()
            case "2":
                notepad_app()
            case "3":
                table_app()
            case "0":
                print("👋 Баяртай!")
                break
            case _:
                print("⚠️ 0-3 хооронд сонгоно уу!")
