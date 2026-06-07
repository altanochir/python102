import tkinter as tk


def main():
    window = tk.Tk()
    window.title("Тооны машин")
    window.geometry("420x520")
    window.resizable(False, False)
    window.configure(bg="#1e1e2e")

    # --- Хувьсагчууд ---
    expression = ""
    current = ""

    # --- Дэлгэц ---
    expr_label = tk.Label(window, text="", font=("Consolas", 14), fg="#a6adc8", bg="#1e1e2e", anchor="e")
    expr_label.pack(fill="x", padx=15, pady=(20, 0))

    display = tk.Label(window, text="0", font=("Consolas", 36, "bold"), fg="#cdd6f4", bg="#1e1e2e", anchor="e")
    display.pack(fill="x", padx=15, pady=(0, 10))

    # --- Товчны функцүүд ---
    def press_num(n):
        nonlocal current
        if n == "." and "." in current:
            return
        if current == "0" and n != ".":
            current = str(n)
        else:
            current += str(n)
        display.config(text=current if current else "0")

    def press_op(op):
        nonlocal current, expression
        if current:
            expression += current + f" {op} "
            expr_label.config(text=expression)
            current = ""
            display.config(text="0")
        elif expression:
            expression = expression[:-3] + f" {op} "
            expr_label.config(text=expression)

    def press_eq():
        nonlocal current, expression
        if current:
            full = expression + current
        else:
            full = expression.strip()
        
        if full:
            try:
                # Хөрвүүлэх (× -> *, ÷ -> /, − -> -)
                eval_expr = full.replace("×", "*").replace("÷", "/").replace("−", "-")
                result = str(eval(eval_expr))
                if result.endswith(".0"):
                    result = result[:-2]
                display.config(text=result)
                expr_label.config(text=f"{full} =")
                current = result
                expression = ""
            except Exception:
                display.config(text="Алдаа")
                current = ""
                expression = ""

    def press_clear():
        nonlocal current, expression
        current = ""
        expression = ""
        display.config(text="0")
        expr_label.config(text="")

    def press_back():
        nonlocal current
        current = current[:-1]
        display.config(text=current if current else "0")

    def press_toggle_sign():
        nonlocal current
        if current:
            if current.startswith("-"):
                current = current[1:]
            else:
                current = "-" + current
            display.config(text=current)

    # --- Товчнууд (Grid) ---
    btn_frame = tk.Frame(window, bg="#1e1e2e")
    btn_frame.pack(fill="both", expand=True, padx=10, pady=5)

    buttons = [
        ("C",  "#f38ba8", press_clear),
        ("⌫", "#fab387", press_back),
        ("%",  "#45475a", lambda: press_op("%")),
        ("÷",  "#89b4fa", lambda: press_op("÷")),
        ("7",  "#313244", lambda: press_num("7")),
        ("8",  "#313244", lambda: press_num("8")),
        ("9",  "#313244", lambda: press_num("9")),
        ("×",  "#89b4fa", lambda: press_op("×")),
        ("4",  "#313244", lambda: press_num("4")),
        ("5",  "#313244", lambda: press_num("5")),
        ("6",  "#313244", lambda: press_num("6")),
        ("−",  "#89b4fa", lambda: press_op("−")),
        ("1",  "#313244", lambda: press_num("1")),
        ("2",  "#313244", lambda: press_num("2")),
        ("3",  "#313244", lambda: press_num("3")),
        ("+",  "#89b4fa", lambda: press_op("+")),
        ("±",  "#313244", press_toggle_sign),
        ("0",  "#313244", lambda: press_num("0")),
        (".",  "#313244", lambda: press_num(".")),
        ("=",  "#a6e3a1", press_eq),
    ]

    for i, (text, bg, cmd) in enumerate(buttons):
        row, col = divmod(i, 4)
        fg = "#1e1e2e" if bg != "#313244" and bg != "#45475a" else "#cdd6f4"
        btn = tk.Button(
            btn_frame, text=text, font=("Arial", 18), bg=bg, fg=fg,
            activebackground=bg, relief="flat", cursor="hand2",
            width=4, height=2, command=cmd
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    for i in range(5):
        btn_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        btn_frame.grid_columnconfigure(i, weight=1)

    window.mainloop()


if __name__ == "__main__":
    main()
