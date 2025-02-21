import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("简易计算器")
        self.expression = ""
        
        self.create_ui()
        self.setup_bindings()

    def create_ui(self):
        # 显示区域
        self.display = ttk.Entry(self.root, width=20, font=('Arial', 16), justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # 按钮布局
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            ttk.Button(self.root, text=text, command=lambda t=text: self.on_button_click(t))\
                .grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        # 清除按钮
        ttk.Button(self.root, text='C', command=self.clear)\
            .grid(row=5, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

    def setup_bindings(self):
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear())

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        else:
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)

    def calculate(self):
        try:
            result = eval(self.expression)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.expression = ""
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "错误")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()