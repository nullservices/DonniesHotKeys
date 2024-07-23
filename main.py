import socket
import keyboard
import tkinter as tk
from tkinter import ttk, simpledialog, colorchooser
import json
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

HOTKEYS_FILE = os.path.join(script_dir, 'hotkeys.json')
COMPUTERS_FILE = os.path.join(script_dir, 'computers.json')

MAX_BUTTONS_PER_ROW = 12
BUTTON_SIZE = 40  # Size in pixels for a square button
DEFAULT_BUTTON_COLOR = "#888888"

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

hotkeys = load_json(HOTKEYS_FILE).get('hotkeys', {})
computers = load_json(COMPUTERS_FILE).get('computers', {})

def send_key_combination(keys, pcs):
    for pc in pcs:
        ip = computers.get(pc)
        if ip:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, 65432))
                    s.sendall('+'.join(keys).encode())
            except ConnectionRefusedError:
                print(f"Connection to {pc} at {ip} was refused. Ensure the remote.py script is running on the target machine.")
            except Exception as e:
                print(f"An error occurred while connecting to {pc} at {ip}: {e}")

def setup_hotkeys(hotkeys):
    for key_combination, details in hotkeys.items():
        keyboard.add_hotkey(key_combination, lambda a=[details['key']], pcs=details['pcs']: send_key_combination(a, pcs))

def create_custom_hotbar(hotkeys):
    root = tk.Tk()
    root.title("Hotkeys Hotbar")
    root.configure(bg='#2e2e2e')
    root.attributes('-topmost', True)
    root.overrideredirect(True)

    def on_drag_start(event):
        root._drag_data = {"x": event.x, "y": event.y}

    def on_drag_motion(event):
        x = root.winfo_x() - root._drag_data["x"] + event.x
        y = root.winfo_y() - root._drag_data["y"] + event.y
        root.geometry(f"+{x}+{y}")

    def capture_key_combination(existing_details=None):
        key_combination = simpledialog.askstring("Input", "Enter key combination (e.g., shift+1):", initialvalue=existing_details.get('key_combination') if existing_details else "")
        action_key = simpledialog.askstring("Input", "Enter action key (e.g., 2):", initialvalue=existing_details.get('key') if existing_details else "")
        button_name = simpledialog.askstring("Input", "Enter button name:", initialvalue=existing_details.get('name') if existing_details else "")
        pcs = simpledialog.askstring("Input", "Enter target PCs (comma-separated, e.g., PC_A,PC_B):", initialvalue=",".join(existing_details.get('pcs')) if existing_details else "").split(',')
        pcs = [pc.strip() for pc in pcs]
        row = simpledialog.askinteger("Input", "Enter row number:", initialvalue=existing_details.get('row') if existing_details else 0)
        color = existing_details.get('color') if existing_details else DEFAULT_BUTTON_COLOR
        color = colorchooser.askcolor(color=color)[1]
        return key_combination, action_key, button_name, pcs, row, color

    def add_button():
        key_combination, action_key, button_name, pcs, row, color = capture_key_combination()
        if key_combination and action_key and button_name and pcs is not None and row is not None:
            hotkeys[key_combination] = {'key': action_key, 'name': button_name, 'pcs': pcs, 'row': row, 'color': color}
            update_hotbar()
            setup_hotkeys(hotkeys)
            adjust_window_size()
            save_json(HOTKEYS_FILE, {'hotkeys': hotkeys})

    def edit_button(key_combination):
        existing_details = hotkeys[key_combination]
        new_key_combination, action_key, button_name, pcs, row, color = capture_key_combination(existing_details)
        if new_key_combination and action_key and button_name and pcs is not None and row is not None:
            if new_key_combination != key_combination:
                del hotkeys[key_combination]
            hotkeys[new_key_combination] = {'key': action_key, 'name': button_name, 'pcs': pcs, 'row': row, 'color': color}
            update_hotbar()
            setup_hotkeys(hotkeys)
            adjust_window_size()
            save_json(HOTKEYS_FILE, {'hotkeys': hotkeys})

    def remove_button(key_combination):
        if key_combination in hotkeys:
            del hotkeys[key_combination]
            update_hotbar()
            adjust_window_size()
            save_json(HOTKEYS_FILE, {'hotkeys': hotkeys})

    def capture_computer():
        name = simpledialog.askstring("Input", "Enter computer name (e.g., PC_A):")
        ip = simpledialog.askstring("Input", "Enter computer IP address (e.g., 192.168.1.2):")
        return name, ip

    def add_computer():
        name, ip = capture_computer()
        if name and ip:
            computers[name] = ip
            save_json(COMPUTERS_FILE, {'computers': computers})

    def remove_computer(name):
        if name in computers:
            del computers[name]
            save_json(COMPUTERS_FILE, {'computers': computers})

    def show_context_menu(event, key_combination=None):
        context_menu = tk.Menu(root, tearoff=0, bg='#2e2e2e', fg='#ffffff')
        if key_combination:
            context_menu.add_command(label="Edit", command=lambda: edit_button(key_combination))
            context_menu.add_command(label="Remove", command=lambda: remove_button(key_combination))
        else:
            context_menu.add_command(label="Add Button", command=add_button)
        context_menu.add_separator()
        context_menu.add_command(label="Add Computer", command=add_computer)
        if computers:
            computer_submenu = tk.Menu(context_menu, tearoff=0, bg='#2e2e2e', fg='#ffffff')
            for name in computers.keys():
                computer_submenu.add_command(label=f"Remove {name}", command=lambda n=name: remove_computer(n))
            context_menu.add_cascade(label="Remove Computer", menu=computer_submenu)
        context_menu.add_separator()
        context_menu.add_command(label="Close", command=root.destroy)
        context_menu.post(event.x_root, event.y_root)

    def update_hotbar():
        button_positions = {}
        style = ttk.Style()
        for widget in frame.winfo_children():
            widget.destroy()
        for key_combination, details in hotkeys.items():
            button_text = f"{details['name']}"
            button_style = f"{key_combination}.TButton"
            style.configure(button_style, background=details.get('color', DEFAULT_BUTTON_COLOR), foreground='#000000', font=("Helvetica", 8), borderwidth=1, relief="flat", anchor='center', justify='center')
            style.map(button_style, background=[('active', details.get('color', DEFAULT_BUTTON_COLOR))])
            button = ttk.Button(frame, text=button_text, style=button_style, command=lambda a=[details['key']], pcs=details['pcs']: send_key_combination(a, pcs))
            button.grid(row=details['row'], column=button_positions.get(details['row'], 0), padx=1, pady=1, sticky='nsew')
            button.config(width=BUTTON_SIZE)
            button.bind("<Button-3>", lambda event, key_comb=key_combination: show_context_menu(event, key_comb))
            button_positions[details['row']] = button_positions.get(details['row'], 0) + 1

    def adjust_window_size():
        max_row = max(details['row'] for details in hotkeys.values()) + 1 if hotkeys else 1
        max_col = max(len([key for key, details in hotkeys.items() if details['row'] == row]) for row in range(max_row)) + 1
        new_height = BUTTON_SIZE * max_row
        new_width = BUTTON_SIZE * max_col
        root.geometry(f"{new_width}x{new_height}")

    root.bind("<ButtonPress-1>", on_drag_start)
    root.bind("<B1-Motion>", on_drag_motion)
    root.bind("<Button-3>", show_context_menu)

    frame = tk.Frame(root, bg='#2e2e2e')
    frame.pack(expand=True, fill='both')
    frame.grid_columnconfigure(tuple(range(MAX_BUTTONS_PER_ROW)), weight=1)
    frame.grid_rowconfigure(tuple(range(10)), weight=1)

    update_hotbar()
    adjust_window_size()
    root.geometry("+300+300")
    root.mainloop()

if __name__ == "__main__":
    setup_hotkeys(hotkeys)
    create_custom_hotbar(hotkeys)
