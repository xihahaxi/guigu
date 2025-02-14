import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import re
from PIL import Image, ImageTk
import json
import threading
import time
from datetime import datetime



class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("个人学习任务便签系统")
        self.tasks = []

        # 初始化主题
        self.themes = {
            "默认主题": {"bg": "#f0f0f0", "fg": "#000000"},
            "深色主题": {"bg": "#2b2b2b", "fg": "#ffffff"},
            "浅蓝主题": {"bg": "#e3f2fd", "fg": "#1e88e5"}
        }
        self.current_theme = "默认主题"
        self.bg_image = None

        # 设置界面
        self.setup_ui()
        self.apply_theme(self.current_theme)
        self.load_tasks()

        # 启动任务检查线程
        self.start_task_checking()



    def setup_ui(self):
        # 主界面框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 背景Canvas，用于放置背景图片
        self.canvas = tk.Canvas(self.main_frame, width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.place(relwidth=1, relheight=1)  # 背景画布覆盖整个窗口

        # 标题栏
        self.title_label = tk.Label(self.main_frame, text="个人学习任务便签系统", font=("Arial", 18, "bold"), pady=10)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 任务列表框
        self.task_listbox_frame = tk.Frame(self.main_frame)
        self.task_listbox_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.task_tree = ttk.Treeview(self.task_listbox_frame, columns=("Title", "Start Date", "End Date", "Status"), show="headings")
        self.task_tree.heading("Title", text="任务标题")
        self.task_tree.heading("Start Date", text="开始日期")
        self.task_tree.heading("End Date", text="截止日期")
        self.task_tree.heading("Status", text="状态")
        self.task_tree.grid(row=0, column=0, sticky="nsew")

        # 滚动条
        tree_scroll = ttk.Scrollbar(self.task_listbox_frame, orient="vertical", command=self.task_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.task_tree.configure(yscrollcommand=tree_scroll.set)

        # 操作按钮
        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        add_button = ttk.Button(button_frame, text="添加任务", command=self.add_task_window)
        add_button.grid(row=0, column=0, padx=5)

        delete_button = ttk.Button(button_frame, text="删除任务", command=self.delete_task)
        delete_button.grid(row=0, column=1, padx=5)

        complete_button = ttk.Button(button_frame, text="标记完成", command=self.mark_complete)
        complete_button.grid(row=0, column=2, padx=5)

        # 主题切换下拉菜单
        theme_label = tk.Label(self.main_frame, text="选择主题:")
        theme_label.grid(row=3, column=0, pady=5, sticky="w")
        self.theme_selector = ttk.Combobox(self.main_frame, values=list(self.themes.keys()), state="readonly")
        self.theme_selector.set(self.current_theme)
        self.theme_selector.grid(row=3, column=1, pady=5)
        self.theme_selector.bind("<<ComboboxSelected>>", self.change_theme)

        # 更换背景图片按钮
        bg_button = ttk.Button(self.main_frame, text="更换背景图片", command=self.change_background_image)
        bg_button.grid(row=4, column=0, columnspan=2, pady=5)



    def apply_theme(self, theme_name):
        theme = self.themes[theme_name]

        # 创建样式对象
        style = ttk.Style()

        if theme_name == "深色主题":
            self.root.configure(bg="#2e2e2e")  # 设置根窗口的背景颜色
            style.configure("Treeview",
                            background="#3e3e3e",
                            foreground="white",
                            rowheight=25,
                            fieldbackground="#3e3e3e")
            style.configure("Treeview.Heading",
                            background="#4e4e4e",
                            foreground="white")  # 设置标题文字颜色为白色
            self.task_tree.tag_configure("completed", background="#6e6e6e")
        else:
            self.root.configure(bg="white")  # 设置根窗口的背景颜色
            style.configure("Treeview",
                            background="white",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="white")
            style.configure("Treeview.Heading",
                            background="lightgray",
                            foreground="black")  # 设置标题文字颜色为黑色
            self.task_tree.tag_configure("completed", background="#e6e6e6")

        # 应用样式到 Treeview 组件
        self.task_tree.heading("Title", anchor="w")
        self.task_tree.heading("Start Date", anchor="center")
        self.task_tree.heading("End Date", anchor="center")
        self.task_tree.heading("Status", anchor="center")

        # 应用新的样式
        self.task_tree.configure(style="Treeview")
        self.title_label.configure(bg=theme["bg"], fg=theme["fg"])



    def add_task_window(self):
        # 添加任务窗口
        add_window = tk.Toplevel(self.root)
        add_window.title("添加任务")

        tk.Label(add_window, text="任务标题:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        title_entry = tk.Entry(add_window)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="开始日期 (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        start_entry = tk.Entry(add_window)
        start_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="截止日期 (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        end_entry = tk.Entry(add_window)
        end_entry.grid(row=2, column=1, padx=5, pady=5)



        def validate_date(date_str):
            """验证日期格式是否为 YYYY-MM-DD"""
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False



        def save_task():
            title = title_entry.get()
            start_date = start_entry.get()
            end_date = end_entry.get()
            if not title or not start_date or not end_date:
                messagebox.showwarning("输入错误", "所有字段都必须填写！")
                return
            if not validate_date(start_date):
                messagebox.showerror("日期格式错误", "开始日期格式应为 YYYY-MM-DD！")
                return
            if not validate_date(end_date):
                messagebox.showerror("日期格式错误", "截止日期格式应为 YYYY-MM-DD！")
                return
            task = (title, start_date, end_date, "未完成")
            self.tasks.append(task)
            self.update_task_list()
            self.save_tasks()
            add_window.destroy()

        save_button = ttk.Button(add_window, text="保存", command=save_task)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)



    def update_task_list(self):
        # 更新任务列表
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)

        for i, task in enumerate(self.tasks):
            tag = "even" if i % 2 == 0 else "odd"
            self.task_tree.insert("", "end", values=task, tags=(tag,))



    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_index = self.task_tree.index(selected_item)
            del self.tasks[task_index]
            self.update_task_list()
            self.save_tasks()



    def mark_complete(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_index = self.task_tree.index(selected_item)
            task = self.tasks[task_index]
            self.tasks[task_index] = task[:3] + ["已完成"]
            self.update_task_list()
            self.save_tasks()



    def change_theme(self, event=None):
        selected_theme = self.theme_selector.get()
        self.current_theme = selected_theme
        self.apply_theme(selected_theme)



    def change_background_image(self):
        # 选择并设置背景图像
        file_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.bg_image = Image.open(file_path)
            self.bg_image = self.bg_image.resize((self.root.winfo_width(), self.root.winfo_height()))
            self.bg_image = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")



    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)



    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
            self.update_task_list()
        except FileNotFoundError:
            self.tasks = []



    def start_task_checking(self):
        # 定期检查任务是否超时
        def check_for_overdue():
            while True:
                current_time = datetime.now()
                for i, task in enumerate(self.tasks):
                    end_date = datetime.strptime(task[2], "%Y-%m-%d")
                    if end_date < current_time and task[3] != "已完成":
                        self.tasks[i] = task[:3] + ["已超时"]
                self.update_task_list()
                self.save_tasks()
                time.sleep(10)

        task_check_thread = threading.Thread(target=check_for_overdue, daemon=True)
        task_check_thread.start()




if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
