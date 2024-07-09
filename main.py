#main.py
import socket
import keyboard
import threading
import tkinter as tk
from tkinter import ttk, simpledialog

REMOTE_PC_IPS = {
    'PC_A': '192.168.1.2',
    'PC_B': '192.168.1.3'
}
REMOTE_PC_PORT = 65432

hotkeys = {
    'shift+1': {'key': '2', 'name': 'Pet Attack', 'pcs': ['PC_A', 'PC_B']},
    'shift+2': {'key': '3', 'name': 'Pet Back', 'pcs': ['PC_A', 'PC_B']},
    'shift+f': {'key': 'f', 'name': 'Follow', 'pcs': ['PC_A', 'PC_B']},
    'shift+8': {'key': '8', 'name': 'Stand', 'pcs': ['PC_A', 'PC_B']},
    'shift+9': {'key': '9', 'name': 'Sit/Stand', 'pcs': ['PC_A', 'PC_B']},
    'ctrl+1': {'key': '1', 'name': 'Multi-Example', 'pcs': ['PC_A', 'PC_B']}
}

def send_key_combination(keys, pcs):
    for pc in pcs:
        ip = REMOTE_PC_IPS[pc]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, REMOTE_PC_PORT))
            s.sendall('+'.join(keys).encode())

def setup_hotkeys(hotkeys):
    for key_combination, details in hotkeys.items():
        keyboard.add_hotkey(key_combination, lambda a=[details['key']], pcs=details['pcs']: send_key_combination(a, pcs))

def create_custom_hotbar(hotkeys):
    root = tk.Tk()
    root.title("Hotkeys Hotbar")
    root.geometry("400x40")
    root.configure(bg='#2e2e2e')
    root.attributes('-topmost', True)
    root.overrideredirect(True)  

    def on_drag_start(event):
        root._drag_data = {"x": event.x, "y": event.y}

    def on_drag_motion(event):
        x = root.winfo_x() - root._drag_data["x"] + event.x
        y = root.winfo_y() - root._drag_data["y"] + event.y
        root.geometry(f"+{x}+{y}")

    def capture_key_combination():
        key_combination = simpledialog.askstring("Input", "Enter key combination (e.g., shift+1):")
        action_key = simpledialog.askstring("Input", "Enter action key (e.g., 2):")
        button_name = simpledialog.askstring("Input", "Enter button name:")
        pcs = simpledialog.askstring("Input", "Enter target PCs (comma-separated, e.g., PC_A,PC_B):").split(',')
        pcs = [pc.strip() for pc in pcs]
        return key_combination, action_key, button_name, pcs

    def add_button():
        key_combination, action_key, button_name, pcs = capture_key_combination()
        if key_combination and action_key and button_name and pcs:
            hotkeys[key_combination] = {'key': action_key, 'name': button_name, 'pcs': pcs}
            update_hotbar()
            setup_hotkeys(hotkeys)
            adjust_window_width()

    def edit_button(key_combination):
        new_key_combination, action_key, button_name, pcs = capture_key_combination()
        if new_key_combination and action_key and button_name and pcs:
            if new_key_combination != key_combination:
                del hotkeys[key_combination]
            hotkeys[new_key_combination] = {'key': action_key, 'name': button_name, 'pcs': pcs}
            update_hotbar()
            setup_hotkeys(hotkeys)
            adjust_window_width()

    def remove_button(key_combination):
        if key_combination in hotkeys:
            del hotkeys[key_combination]
            update_hotbar()
            adjust_window_width()

    def show_context_menu(event, key_combination=None):
        context_menu = tk.Menu(root, tearoff=0, bg='#2e2e2e', fg='#ffffff')
        if key_combination:
            context_menu.add_command(label="Edit", command=lambda: edit_button(key_combination))
            context_menu.add_command(label="Remove", command=lambda: remove_button(key_combination))
        else:
            context_menu.add_command(label="Add Button", command=add_button)
        context_menu.add_separator()
        context_menu.add_command(label="Close", command=root.destroy)
        context_menu.post(event.x_root, event.y_root)

    def update_hotbar():
        for widget in frame.winfo_children():
            widget.destroy()
        col = 0
        for key_combination, details in hotkeys.items():
            button_text = f"{details['name']}"
            button = ttk.Button(frame, text=button_text, command=lambda a=[details['key']], pcs=details['pcs']: send_key_combination(a, pcs))
            button.grid(row=0, column=col, padx=1, pady=1, sticky='nsew')
            button.configure(style="Hotbar.TButton", width=3)
            button.bind("<Button-3>", lambda event, key_comb=key_combination: show_context_menu(event, key_comb))
            col += 1
        # Add a placeholder button
        placeholder = ttk.Label(frame, text="", width=3)
        placeholder.grid(row=0, column=col, padx=1, pady=1, sticky='nsew')
        placeholder.bind("<Button-3>", show_context_menu)

    def adjust_window_width():
        new_width = max(400, 45 * (len(hotkeys) + 1))
        root.geometry(f"{new_width}x40")

    root.bind("<ButtonPress-1>", on_drag_start)
    root.bind("<B1-Motion>", on_drag_motion)
    root.bind("<Button-3>", show_context_menu)

    style = ttk.Style()
    style.configure("Hotbar.TButton", background='#888888', foreground='#000000', font=("Helvetica", 8), borderwidth=0, relief="flat")
    style.map("Hotbar.TButton", background=[('active', '#aaaaaa')])

    frame = tk.Frame(root, bg='#2e2e2e')
    frame.pack(expand=True, fill='both')
    frame.grid_columnconfigure(tuple(range(len(hotkeys) + 1)), weight=1)
    frame.grid_rowconfigure(0, weight=1)

    update_hotbar()
    adjust_window_width()
    root.mainloop()

if __name__ == "__main__":
    setup_hotkeys(hotkeys)
    create_custom_hotbar(hotkeys)
