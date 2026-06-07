"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 2.1: Tkinter — Эхний Цонх & Widget-үүд              ║
║  Python 102 — Visual Basic туршлагатай програмистад зориулсан    ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Зорилго:
   - tkinter ашиглан цонхтой програм бүтээх
   - Label, Button, Entry — Үндсэн widget-үүд
   - Event handling — Товч дарах, оролт авах
   - Layout — Widget-үүдийг байрлуулах

💡 Visual Basic туршлагатай танд:
   VB:  Form          →  Python: tk.Tk() (Үндсэн цонх)
   VB:  Label         →  Python: tk.Label()
   VB:  TextBox       →  Python: tk.Entry() (нэг мөр), tk.Text() (олон мөр)
   VB:  CommandButton  →  Python: tk.Button()
   VB:  ListBox       →  Python: tk.Listbox()
   VB:  ComboBox      →  Python: ttk.Combobox()
   VB:  CheckBox      →  Python: tk.Checkbutton()
   VB:  OptionButton  →  Python: tk.Radiobutton()
   VB:  PictureBox    →  Python: tk.Canvas()
   VB:  Frame         →  Python: tk.Frame() / ttk.Frame()
   VB:  MsgBox        →  Python: messagebox.showinfo()

   tkinter нь Python-д СУУЛГАЛТГҮЙ ирдэг!
   pip install хийх шаардлагагүй! 🎉
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# 📌 ХЭСЭГ 1: Хамгийн энгийн цонх
# ============================================================
"""
VB-д Form нээхэд:
   - Properties цонхонд Title, Width, Height тохируулдаг
   - Python-д кодоор бичнэ

Доорх код нь хамгийн энгийн цонх үүсгэнэ.
"""

def example_1_basic_window():
    """Хамгийн энгийн цонх"""

    # 1. Үндсэн цонх үүсгэх (VB: Form)
    window = tk.Tk()

    # 2. Цонхны шинж чанарууд (VB: Properties)
    window.title("Миний Эхний Програм 🐍")    # VB: Form.Caption
    window.geometry("400x300")                  # VB: Form.Width, Form.Height (өргөн x өндөр)
    window.resizable(True, True)                # VB: Form.BorderStyle (хэмжээ өөрчлөх боломж)
    window.configure(bg="#1e1e2e")              # VB: Form.BackColor (арын өнгө)

    # 3. Label нэмэх (VB: Label1.Caption = "Hello")
    label = tk.Label(
        window,
        text="Сайн байна уу! 🎉",
        font=("Arial", 24, "bold"),
        fg="#cdd6f4",                           # Текстийн өнгө (ForeColor)
        bg="#1e1e2e",                            # Арын өнгө (BackColor)
    )
    label.pack(pady=50)                         # Цонхонд байрлуулах

    # 4. Товч нэмэх (VB: Command1.Caption = "Click Me")
    button = tk.Button(
        window,
        text="Намайг дар! 👆",
        font=("Arial", 14),
        command=lambda: messagebox.showinfo(    # VB: MsgBox "Hello!"
            "Мэдэгдэл",
            "Товч дарлаа! 🎊"
        ),
        bg="#89b4fa",
        fg="#1e1e2e",
        activebackground="#74c7ec",
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
    )
    button.pack(pady=20)

    # 5. Програм ажиллуулах (VB: Form.Show / Run)
    # mainloop() = VB-ийн event loop
    # Энэ нь цонхыг нээлттэй байлгаж, хэрэглэгчийн үйлдлийг хүлээнэ
    window.mainloop()


# ============================================================
# 📌 ХЭСЭГ 2: Бүх Widget-үүд (VB Controls)
# ============================================================

def example_2_all_widgets():
    """Бүх үндсэн widget-үүдийн жишээ"""

    window = tk.Tk()
    window.title("📦 Бүх Widget-үүд")
    window.geometry("500x700")
    window.configure(bg="#1e1e2e")

    # --- Стиль тохируулах ---
    style = ttk.Style()
    style.theme_use("clam")  # Орчин үеийн харагдах байдал

    # Нийтлэг өнгөнүүд
    BG = "#1e1e2e"
    FG = "#cdd6f4"
    ACCENT = "#89b4fa"

    # ==========================================
    # 📝 Label (VB: Label)
    # ==========================================
    tk.Label(
        window, text="📝 Label — Текст харуулах",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    tk.Label(
        window, text="Энэ бол энгийн текст (Label)",
        font=("Arial", 10), fg=FG, bg=BG
    ).pack(anchor="w", padx=20)

    # ==========================================
    # 🔘 Button (VB: CommandButton)
    # ==========================================
    tk.Label(
        window, text="🔘 Button — Товч",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    btn_frame = tk.Frame(window, bg=BG)
    btn_frame.pack(anchor="w", padx=20)

    tk.Button(btn_frame, text="Энгийн товч", bg="#a6e3a1", fg="#1e1e2e",
              relief="flat", padx=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Өнгөтэй товч", bg="#f38ba8", fg="white",
              relief="flat", padx=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🚀 Emoji товч", bg="#fab387", fg="#1e1e2e",
              relief="flat", padx=10).pack(side="left", padx=5)

    # ==========================================
    # ✏️ Entry (VB: TextBox — нэг мөр)
    # ==========================================
    tk.Label(
        window, text="✏️ Entry — Текст оруулах (нэг мөр)",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    entry = tk.Entry(
        window, font=("Arial", 12), bg="#313244", fg=FG,
        insertbackground=FG, relief="flat", width=40
    )
    entry.pack(anchor="w", padx=20)
    entry.insert(0, "Энд бичнэ үү...")    # VB: Text1.Text = "..."

    # ==========================================
    # 📋 Text (VB: TextBox — олон мөр, Multiline=True)
    # ==========================================
    tk.Label(
        window, text="📋 Text — Олон мөрт текст",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    text_box = tk.Text(
        window, height=3, font=("Arial", 10), bg="#313244", fg=FG,
        insertbackground=FG, relief="flat", width=50
    )
    text_box.pack(anchor="w", padx=20)
    text_box.insert("1.0", "Олон мөрт\nтекст бичиж\nболно...")

    # ==========================================
    # ☑️ Checkbutton (VB: CheckBox)
    # ==========================================
    tk.Label(
        window, text="☑️ Checkbutton — Сонголтын нүд",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    check_var1 = tk.BooleanVar(value=True)
    check_var2 = tk.BooleanVar(value=False)

    tk.Checkbutton(window, text="Python сурах", variable=check_var1,
                   font=("Arial", 10), fg=FG, bg=BG, selectcolor="#313244",
                   activebackground=BG).pack(anchor="w", padx=20)
    tk.Checkbutton(window, text="AI сурах", variable=check_var2,
                   font=("Arial", 10), fg=FG, bg=BG, selectcolor="#313244",
                   activebackground=BG).pack(anchor="w", padx=20)

    # ==========================================
    # 🔵 Radiobutton (VB: OptionButton)
    # ==========================================
    tk.Label(
        window, text="🔵 Radiobutton — Радио товч",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    radio_var = tk.StringVar(value="python")

    for text, value in [("Python 🐍", "python"), ("JavaScript 🟨", "js"), ("Rust 🦀", "rust")]:
        tk.Radiobutton(window, text=text, variable=radio_var, value=value,
                       font=("Arial", 10), fg=FG, bg=BG, selectcolor="#313244",
                       activebackground=BG).pack(anchor="w", padx=20)

    # ==========================================
    # 📜 Combobox (VB: ComboBox)
    # ==========================================
    tk.Label(
        window, text="📜 Combobox — Унадаг жагсаалт",
        font=("Arial", 12, "bold"), fg=ACCENT, bg=BG
    ).pack(anchor="w", padx=10, pady=(15, 5))

    combo = ttk.Combobox(
        window,
        values=["Улаанбаатар", "Дархан", "Эрдэнэт", "Чойбалсан"],
        font=("Arial", 10), width=30, state="readonly"
    )
    combo.pack(anchor="w", padx=20)
    combo.set("Хот сонгох...")           # VB: Combo1.Text = "..."

    window.mainloop()


# ============================================================
# 📌 ХЭСЭГ 3: Layout — Widget байрлуулалт
# ============================================================
"""
VB-д widget-ийг хулганаар чирж байрлуулдаг.
Python tkinter-д 3 арга бий:

1. pack()  — Дээрээс доош, зүүнээс баруун руу (хамгийн энгийн)
2. grid()  — Хүснэгт хэлбэрээр (VB-ийн grid шиг)
3. place() — x, y координатаар (VB-ийн шиг яг байрлал)

⚠️ Нэг Frame дотор pack() ба grid()-ийг ХОЛЬЖ БОЛОХГҮЙ!
"""

def example_3_grid_layout():
    """Grid layout — Бүртгэлийн форм (VB-тэй хамгийн адилхан!)"""

    window = tk.Tk()
    window.title("📝 Бүртгэлийн Форм — Grid Layout")
    window.geometry("450x400")
    window.configure(bg="#1e1e2e")

    BG = "#1e1e2e"
    FG = "#cdd6f4"
    INPUT_BG = "#313244"

    # Гарчиг
    tk.Label(
        window, text="📝 Хэрэглэгч Бүртгэх",
        font=("Arial", 18, "bold"), fg="#89b4fa", bg=BG
    ).grid(row=0, column=0, columnspan=2, pady=20)

    # --- Grid ашиглан form бүтээх ---
    # VB-ийн Properties цонхонд Left, Top тохируулдаг шиг
    # grid() нь row (мөр), column (багана) ашиглана

    labels = ["Нэр:", "И-мэйл:", "Нууц үг:", "Хот:", "Нас:"]
    entries = {}

    for i, label_text in enumerate(labels, start=1):
        # Label (зүүн тал)
        tk.Label(
            window, text=label_text,
            font=("Arial", 12), fg=FG, bg=BG
        ).grid(row=i, column=0, padx=(20, 10), pady=8, sticky="e")
        #                                                sticky="e" = баруун тийш зэрэгцүүлэх

        # Entry (баруун тал)
        entry = tk.Entry(
            window, font=("Arial", 12), bg=INPUT_BG, fg=FG,
            insertbackground=FG, relief="flat", width=25
        )
        entry.grid(row=i, column=1, padx=(0, 20), pady=8, sticky="w")

        # Нууц үг талбарын тохиргоо
        if label_text == "Нууц үг:":
            entry.config(show="●")     # VB: Text1.PasswordChar = "●"

        entries[label_text] = entry

    # --- Товчнууд ---
    btn_frame = tk.Frame(window, bg=BG)
    btn_frame.grid(row=len(labels) + 1, column=0, columnspan=2, pady=20)

    def on_register():
        """Бүртгэх товчны event handler"""
        # VB: Private Sub cmdRegister_Click()
        name = entries["Нэр:"].get()
        email = entries["И-мэйл:"].get()

        if not name or not email:
            messagebox.showwarning("⚠️ Анхааруулга", "Нэр, И-мэйл бөглөнө үү!")
            return

        messagebox.showinfo(
            "✅ Амжилттай!",
            f"Бүртгэл амжилттай!\n\n"
            f"Нэр: {name}\n"
            f"И-мэйл: {email}"
        )

    def on_clear():
        """Цэвэрлэх товчны event handler"""
        for entry in entries.values():
            entry.delete(0, tk.END)    # VB: Text1.Text = ""

    tk.Button(
        btn_frame, text="✅ Бүртгэх", font=("Arial", 12),
        bg="#a6e3a1", fg="#1e1e2e", relief="flat",
        padx=20, pady=5, cursor="hand2",
        command=on_register
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame, text="🗑️ Цэвэрлэх", font=("Arial", 12),
        bg="#f38ba8", fg="white", relief="flat",
        padx=20, pady=5, cursor="hand2",
        command=on_clear
    ).pack(side="left", padx=10)

    # --- Статус мөр (VB: StatusBar) ---
    status = tk.Label(
        window, text="🟢 Бэлэн", font=("Arial", 9),
        fg="#a6adc8", bg="#181825", anchor="w"
    )
    status.grid(row=len(labels) + 2, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    window.mainloop()


# ============================================================
# 📌 ХЭСЭГ 4: Event Handling (Үйл явдал зохицуулалт)
# ============================================================
"""
💡 VB-тэй харьцуулалт:

   VB:  Private Sub Button1_Click()
   Py:  button.config(command=my_function)

   VB:  Private Sub Form_KeyPress(KeyAscii As Integer)
   Py:  window.bind("<KeyPress>", my_function)

   VB:  Private Sub Timer1_Timer()
   Py:  window.after(1000, my_function)
"""

def example_4_events():
    """Event handling жишээ"""

    window = tk.Tk()
    window.title("🎮 Event Handling")
    window.geometry("500x500")
    window.configure(bg="#1e1e2e")

    BG = "#1e1e2e"
    FG = "#cdd6f4"

    # Гарчиг
    tk.Label(
        window, text="🎮 Event Handling",
        font=("Arial", 20, "bold"), fg="#89b4fa", bg=BG
    ).pack(pady=15)

    # --- Лог цонх (бүх үйл явдлыг харуулна) ---
    log_text = tk.Text(
        window, height=10, font=("Consolas", 10),
        bg="#313244", fg="#a6e3a1", insertbackground=FG,
        relief="flat", width=55
    )
    log_text.pack(padx=15, pady=5)

    def log(message):
        """Лог цонхонд мессеж нэмэх"""
        log_text.insert(tk.END, f"  {message}\n")
        log_text.see(tk.END)          # Автомат доош гүйлгэх

    # --- 1. Button click ---
    click_count = [0]                  # list ашиглах (closure дотор өөрчлөх боломжтой)

    def on_click():
        click_count[0] += 1
        log(f"🖱️ Товч дарлаа! (#{click_count[0]})")

    tk.Button(
        window, text="🖱️ Намайг дар!", font=("Arial", 12),
        bg="#89b4fa", fg="#1e1e2e", relief="flat",
        padx=15, pady=5, cursor="hand2", command=on_click
    ).pack(pady=10)

    # --- 2. Keyboard events ---
    # VB:  Private Sub Form_KeyPress(KeyAscii As Integer)
    def on_key(event):
        log(f"⌨️ Key: '{event.char}' (keysym: {event.keysym}, code: {event.keycode})")

    window.bind("<KeyPress>", on_key)  # Аливаа товч дарахад

    # Тодорхой товч:
    window.bind("<Return>", lambda e: log("⏎ Enter дарлаа!"))
    window.bind("<Escape>", lambda e: window.destroy())   # Escape = Хаах

    # --- 3. Mouse events ---
    # VB:  Private Sub Form_MouseMove(...)

    mouse_label = tk.Label(
        window, text="🖱️ Хулганыг энд хөдөлгө!",
        font=("Arial", 12), fg=FG, bg="#313244",
        width=40, height=3, relief="flat"
    )
    mouse_label.pack(pady=10)

    def on_mouse_move(event):
        mouse_label.config(text=f"🖱️ X: {event.x}, Y: {event.y}")

    def on_mouse_click(event):
        log(f"🖱️ Click: ({event.x}, {event.y})")

    def on_right_click(event):
        log(f"🖱️ Right click: ({event.x}, {event.y})")

    mouse_label.bind("<Motion>", on_mouse_move)        # Хулгана хөдлөх
    mouse_label.bind("<Button-1>", on_mouse_click)     # Зүүн товч
    mouse_label.bind("<Button-3>", on_right_click)     # Баруун товч

    # --- 4. Timer (VB: Timer control) ---
    time_label = tk.Label(
        window, text="⏰ 00:00:00",
        font=("Consolas", 16, "bold"), fg="#f9e2af", bg=BG
    )
    time_label.pack(pady=10)

    def update_clock():
        """Цагийг шинэчлэх — VB: Timer1_Timer()"""
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        time_label.config(text=f"⏰ {now}")
        window.after(1000, update_clock)   # 1 секунд дараа дахин дуудах
        # VB: Timer1.Interval = 1000

    update_clock()  # Эхлүүлэх

    log("🚀 Програм эхэллээ!")
    log("⌨️ Escape = Хаах")
    log("🖱️ Доорх хэсэгт хулгана хөдөлгөж, дарж үзээрэй")

    window.mainloop()


# ============================================================
# 📌 ХЭСЭГ 5: Тооцоолуур (Бодит төсөл!)
# ============================================================

def example_5_calculator():
    """🔢 Тооцоолуур — VB-ийн сонгодог төсөл!"""

    window = tk.Tk()
    window.title("🔢 Тооцоолуур")
    window.geometry("320x480")
    window.resizable(False, False)
    window.configure(bg="#1e1e2e")

    # --- Хувьсагчууд ---
    current_input = ""
    expression = ""

    # --- Дэлгэц (Display) ---
    display_frame = tk.Frame(window, bg="#1e1e2e")
    display_frame.pack(fill="x", padx=10, pady=(15, 5))

    # Илэрхийлэл (жижиг текст)
    expr_label = tk.Label(
        display_frame, text="",
        font=("Consolas", 12), fg="#a6adc8", bg="#1e1e2e",
        anchor="e"
    )
    expr_label.pack(fill="x")

    # Үр дүн (том текст)
    display_label = tk.Label(
        display_frame, text="0",
        font=("Consolas", 32, "bold"), fg="#cdd6f4", bg="#1e1e2e",
        anchor="e"
    )
    display_label.pack(fill="x")

    # --- Товчны функцүүд ---
    def press_number(num):
        nonlocal current_input
        current_input += str(num)
        display_label.config(text=current_input)

    def press_operator(op):
        nonlocal current_input, expression
        if current_input:
            expression += current_input + f" {op} "
            expr_label.config(text=expression)
            current_input = ""
            display_label.config(text="0")

    def press_equals():
        nonlocal current_input, expression
        if current_input and expression:
            full_expr = expression + current_input
            try:
                result = eval(full_expr)    # ⚠️ eval() — зөвхөн тооцоолуурт!
                display_label.config(text=str(result))
                expr_label.config(text=f"{full_expr} =")
                current_input = str(result)
                expression = ""
            except Exception as e:
                display_label.config(text="Алдаа!")
                current_input = ""
                expression = ""

    def press_clear():
        nonlocal current_input, expression
        current_input = ""
        expression = ""
        display_label.config(text="0")
        expr_label.config(text="")

    def press_backspace():
        nonlocal current_input
        current_input = current_input[:-1]
        display_label.config(text=current_input if current_input else "0")

    # --- Товчнууд (Grid layout) ---
    btn_frame = tk.Frame(window, bg="#1e1e2e")
    btn_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Товчны загвар
    button_config = {
        "font": ("Arial", 16),
        "relief": "flat",
        "cursor": "hand2",
        "width": 4,
        "height": 2,
    }

    # Товчнуудын хүснэгт [текст, мөр, багана, өнгө, команд]
    buttons = [
        ("C",  0, 0, "#f38ba8", "#1e1e2e", press_clear),
        ("⌫", 0, 1, "#fab387", "#1e1e2e", press_backspace),
        ("%",  0, 2, "#45475a", "#cdd6f4", lambda: press_operator("%")),
        ("÷",  0, 3, "#89b4fa", "#1e1e2e", lambda: press_operator("/")),
        ("7",  1, 0, "#313244", "#cdd6f4", lambda: press_number(7)),
        ("8",  1, 1, "#313244", "#cdd6f4", lambda: press_number(8)),
        ("9",  1, 2, "#313244", "#cdd6f4", lambda: press_number(9)),
        ("×",  1, 3, "#89b4fa", "#1e1e2e", lambda: press_operator("*")),
        ("4",  2, 0, "#313244", "#cdd6f4", lambda: press_number(4)),
        ("5",  2, 1, "#313244", "#cdd6f4", lambda: press_number(5)),
        ("6",  2, 2, "#313244", "#cdd6f4", lambda: press_number(6)),
        ("−",  2, 3, "#89b4fa", "#1e1e2e", lambda: press_operator("-")),
        ("1",  3, 0, "#313244", "#cdd6f4", lambda: press_number(1)),
        ("2",  3, 1, "#313244", "#cdd6f4", lambda: press_number(2)),
        ("3",  3, 2, "#313244", "#cdd6f4", lambda: press_number(3)),
        ("+",  3, 3, "#89b4fa", "#1e1e2e", lambda: press_operator("+")),
        ("±",  4, 0, "#313244", "#cdd6f4", lambda: None),
        ("0",  4, 1, "#313244", "#cdd6f4", lambda: press_number(0)),
        (".",  4, 2, "#313244", "#cdd6f4", lambda: press_number(".")),
        ("=",  4, 3, "#a6e3a1", "#1e1e2e", press_equals),
    ]

    for text, row, col, bg, fg, cmd in buttons:
        btn = tk.Button(
            btn_frame, text=text, bg=bg, fg=fg,
            activebackground=bg, command=cmd,
            **button_config
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    # Grid-ийн багана, мөрүүдийг тэнцүү тэлэх
    for i in range(5):
        btn_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        btn_frame.grid_columnconfigure(i, weight=1)

    # --- Гарын товчоор ажиллуулах ---
    def on_key(event):
        key = event.char
        if key.isdigit():
            press_number(int(key))
        elif key == ".":
            press_number(".")
        elif key == "+":
            press_operator("+")
        elif key == "-":
            press_operator("-")
        elif key == "*":
            press_operator("*")
        elif key == "/":
            press_operator("/")
        elif key == "\r":              # Enter
            press_equals()
        elif event.keysym == "BackSpace":
            press_backspace()
        elif event.keysym == "Escape":
            press_clear()

    window.bind("<Key>", on_key)

    window.mainloop()


# ============================================================
# 📌 ХЭСЭГ 6: MessageBox & Dialog
# ============================================================
"""
💡 VB-тэй харьцуулалт:

   VB:  MsgBox "Hello!", vbInformation, "Title"
   Py:  messagebox.showinfo("Title", "Hello!")

   VB:  MsgBox "Sure?", vbYesNo
   Py:  messagebox.askyesno("Title", "Sure?")

   VB:  InputBox("Enter name:")
   Py:  simpledialog.askstring("Title", "Enter name:")

   VB:  CommonDialog.ShowOpen
   Py:  filedialog.askopenfilename()
"""

def example_6_dialogs():
    """Бүх төрлийн Dialog цонхнууд"""
    from tkinter import simpledialog, filedialog, colorchooser

    window = tk.Tk()
    window.title("💬 Dialog-ууд")
    window.geometry("400x550")
    window.configure(bg="#1e1e2e")

    BG = "#1e1e2e"
    FG = "#cdd6f4"

    tk.Label(
        window, text="💬 Dialog Цонхнууд",
        font=("Arial", 18, "bold"), fg="#89b4fa", bg=BG
    ).pack(pady=15)

    result_label = tk.Label(
        window, text="Үр дүн энд харагдана...",
        font=("Arial", 11), fg="#a6e3a1", bg="#313244",
        wraplength=350, justify="left", padx=10, pady=10
    )
    result_label.pack(padx=15, pady=10, fill="x")

    def make_btn(text, command, color="#45475a"):
        tk.Button(
            window, text=text, font=("Arial", 11),
            bg=color, fg="white" if color != "#f9e2af" else "#1e1e2e",
            relief="flat", padx=15, pady=5,
            cursor="hand2", command=command
        ).pack(pady=3, padx=15, fill="x")

    # --- Info ---
    make_btn("ℹ️ Мэдээлэл (showinfo)", lambda: (
        messagebox.showinfo("ℹ️ Мэдээлэл", "Энэ бол мэдээллийн цонх!"),
        result_label.config(text="showinfo — OK дарлаа")
    ))

    # --- Warning ---
    make_btn("⚠️ Анхааруулга (showwarning)", lambda: (
        messagebox.showwarning("⚠️ Анхааруулга", "Болгоомжтой!"),
        result_label.config(text="showwarning — OK дарлаа")
    ), "#fab387")

    # --- Error ---
    make_btn("❌ Алдаа (showerror)", lambda: (
        messagebox.showerror("❌ Алдаа", "Ямар нэг зүйл буруу болсон!"),
        result_label.config(text="showerror — OK дарлаа")
    ), "#f38ba8")

    # --- Yes/No ---
    def ask_yn():
        answer = messagebox.askyesno("❓ Асуулт", "Python гоё юу?")
        result_label.config(text=f"askyesno → {answer}")

    make_btn("❓ Тийм/Үгүй (askyesno)", ask_yn, "#89b4fa")

    # --- Text input ---
    def ask_name():
        name = simpledialog.askstring("✏️ Оролт", "Таны нэрийг оруулна уу:")
        result_label.config(text=f"askstring → '{name}'")

    make_btn("✏️ Текст асуух (askstring)", ask_name, "#a6e3a1")

    # --- Number input ---
    def ask_age():
        age = simpledialog.askinteger("🔢 Тоо", "Насаа оруулна уу:", minvalue=1, maxvalue=150)
        result_label.config(text=f"askinteger → {age}")

    make_btn("🔢 Тоо асуух (askinteger)", ask_age, "#cba6f7")

    # --- File dialog ---
    def open_file():
        filepath = filedialog.askopenfilename(
            title="Файл сонгох",
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        result_label.config(text=f"Файл: {filepath}")

    make_btn("📂 Файл сонгох (askopenfilename)", open_file, "#f9e2af")

    # --- Color chooser ---
    def choose_color():
        color = colorchooser.askcolor(title="Өнгө сонгох")
        if color[1]:
            result_label.config(text=f"Өнгө: {color[1]}", bg=color[1])

    make_btn("🎨 Өнгө сонгох (askcolor)", choose_color, "#f5c2e7")

    window.mainloop()


# ============================================================
# 🎯 АЖИЛЛУУЛАХ ЖИШЭЭГ СОНГОХ
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║  🐍 Python GUI — Tkinter Хичээл 2.1             ║
║                                                  ║
║  Ямар жишээ ажиллуулах вэ?                      ║
║                                                  ║
║  1. 🪟  Энгийн цонх (Hello World)               ║
║  2. 📦  Бүх Widget-үүд                          ║
║  3. 📝  Grid Layout — Бүртгэлийн форм           ║
║  4. 🎮  Event Handling                           ║
║  5. 🔢  Тооцоолуур (Calculator)                 ║
║  6. 💬  Dialog цонхнууд                          ║
║  0. 🚪  Гарах                                    ║
╚══════════════════════════════════════════════════╝
    """)

    while True:
        choice = input("Сонголт (0-6): ").strip()

        match choice:
            case "1":
                example_1_basic_window()
            case "2":
                example_2_all_widgets()
            case "3":
                example_3_grid_layout()
            case "4":
                example_4_events()
            case "5":
                example_5_calculator()
            case "6":
                example_6_dialogs()
            case "0":
                print("👋 Баяртай!")
                break
            case _:
                print("⚠️ 0-6 хооронд сонгоно уу!")
