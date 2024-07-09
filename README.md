# Donnies HotKeys

Donnies HotKeys is a Python-based tool that allows you to send key presses from a main PC to multiple remote PCs. It supports setting up custom hotkeys that can be directed to specific PCs, making it ideal for managing multiple game clients or applications simultaneously.

## Features

- Define custom hotkeys to be sent to specific PCs.
- GUI hotbar for easy hotkey management.
- Supports both Windows 10 and Windows 11.
- Allows for editing and removing hotkeys dynamically.

## Requirements

- Python 3.6 or higher
- `pynput` library
- `keyboard` library
- `tkinter` library (included with Python)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/DonniesHotKeys.git
    cd DonniesHotKeys
    ```

2. Install the required libraries:

    ```bash
    pip install pynput keyboard
    ```

## Usage

### On the Remote PCs

1. Run the `remote.py` script on each remote PC that will receive key presses:

    ```bash
    python remote.py
    ```

### On the Main PC

1. Run the `main.py` script on the main PC to manage and send key presses:

    ```bash
    python main.py
    ```

### Configuration

- Update the `REMOTE_PC_IPS` dictionary in `main.py` with the IP addresses of your remote PCs.
- Customize the `hotkeys` dictionary in `main.py` with your desired key combinations and target PCs.

### Example Hotkey Configuration

```python
hotkeys = {
    'shift+1': {'key': '2', 'name': 'Pet Attack', 'pcs': ['PC_A', 'PC_B']},
    'shift+2': {'key': '3', 'name': 'Pet Back', 'pcs': ['PC_A', 'PC_B']},
    'shift+f': {'key': 'f', 'name': 'Follow', 'pcs': ['PC_A', 'PC_B']},
    'shift+8': {'key': '8', 'name': 'Stand', 'pcs': ['PC_A', 'PC_B']},
    'shift+9': {'key': '9', 'name': 'Sit/Stand', 'pcs': ['PC_A', 'PC_B']},
    'ctrl+1': {'key': '1', 'name': 'Multi-Example', 'pcs': ['PC_A', 'PC_B']}
}
```

### Running the Scripts
- Ensure both the scripts and the game client are running with administrative privileges.
- Run the remote.py script on each remote PC.
- Run the main.py script on the main PC.
