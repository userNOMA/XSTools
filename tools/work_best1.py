import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("任务管理程序")

# 创建按钮
buttons = []
for i in range(5):
    button = tk.Button(root, text=f"按钮 {i + 1}")
    buttons.append(button)

# 初始化拖拽相关变量
drag_data = {"x": 0, "y": 0, "item": None}

# 鼠标左键按下时的处理函数
def on_button_press(event):
    drag_data["item"] = root.winfo_containing(event.x_root, event.y_root)
    if drag_data["item"] in buttons:
        drag_data["x"] = event.x
        drag_data["y"] = event.y

# 鼠标左键释放时的处理函数
def on_button_release(event):
    drag_data["item"] = None

# 鼠标拖动时的处理函数
def on_mouse_drag(event):
    if drag_data["item"] is not None:
        x, y = event.x_root - drag_data["x"], event.y_root - drag_data["y"]
        drag_data["item"].place(x=x, y=y)

# 绑定事件处理函数
for button in buttons:
    button.bind("<ButtonPress-1>", on_button_press)
    button.bind("<ButtonRelease-1>", on_button_release)

root.bind("<B1-Motion>", on_mouse_drag)

# 放置按钮
for i, button in enumerate(buttons):
    button.grid(row=i, column=0, padx=10, pady=5)

root.mainloop()
