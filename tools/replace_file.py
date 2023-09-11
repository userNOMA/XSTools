import tkinter as tk
from tkinter import filedialog
import re
import os


def replace_content(files, old_text, new_text):
    for file in files:
        with open(file, 'r', encoding='UTF-8') as f:
            content = f.read()

        content = content.replace(old_text, new_text)

        with open(file, 'w', encoding='UTF-8') as f:
            f.write(content)


def replace_content1(files, old_text, new_text):
    for file in files:
        with open(file, 'r', encoding='UTF-8') as f:
            content = f.read()

        pattern = r"<评审材料设备表>.*?</评审材料设备表>"
        content = re.sub(pattern, "", content, flags=re.DOTALL)

        with open(file, 'w', encoding='UTF-8') as f:
            f.write(content)


def select_files():
    files = filedialog.askopenfilenames(filetypes=[("all files", "*")])
    file_list.config(state='normal')
    file_list.delete(1.0, tk.END)
    for file in files:
        file_list.insert(tk.END, file + '\n')
    file_list.config(state='disabled')


def replace():
    files = file_list.get(1.0, tk.END).strip().split('\n')
    old_text = old_text_entry.get()
    new_text = new_text_entry.get()

    replace_content(files, old_text, new_text)
    # replace_content1(files, old_text, new_text)

    tk.messagebox.showinfo("替换完成", "文件替换完成")


# 创建主窗口
root = tk.Tk()
root.title("文件内容替换工具")

# 创建选择文件按钮
select_files_button = tk.Button(root, text="选择文件", command=select_files)
select_files_button.pack(pady=10)

# 显示文件列表的文本框
file_list = tk.Text(root, height=5, width=40)
file_list.pack()

# 输入指定内容的文本框
old_text_label = tk.Label(root, text="指定内容:")
old_text_label.pack()
old_text_entry = tk.Entry(root)
old_text_entry.pack()

# 输入替换内容的文本框
new_text_label = tk.Label(root, text="替换内容:")
new_text_label.pack()
new_text_entry = tk.Entry(root)
new_text_entry.pack()

# 创建替换按钮
replace_button = tk.Button(root, text="开始替换", command=replace)
replace_button.pack(pady=10)

root.mainloop()
