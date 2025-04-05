import tkinter as tk
from tkinter import messagebox
import re

# Dialog window for configuring game mode and connection settings
class ConfigDialog:
    def __init__(self, master):
        self.master = master
        master.title("Game Configuration")

        self.result = None

        # --- Game Mode Selection ---
        self.mode_label = tk.Label(master, text="Select Game Mode:")
        self.mode_label.pack()

        self.game_mode = tk.StringVar(value="single")
        self.single_player_rb = tk.Radiobutton(master, text="Single Player", variable=self.game_mode, value="single", command=self.update_field_visibility)
        self.local_2p_rb = tk.Radiobutton(master, text="2 Players Local", variable=self.game_mode, value="local_2p", command=self.update_field_visibility)
        self.network_rb = tk.Radiobutton(master, text="Network Game", variable=self.game_mode, value="network", command=self.update_field_visibility)

        self.single_player_rb.pack()
        self.local_2p_rb.pack()
        self.network_rb.pack()

        # --- IP Address Input ---
        self.ip_label = tk.Label(master, text="Server IP:")
        self.ip_entry = tk.Entry(master, fg='grey', validate='key')
        self.ip_entry.insert(0, "127.0.0.1")  # Default value
        self.ip_entry.bind("<FocusIn>", self.clear_ip_placeholder)
        self.ip_entry.bind("<FocusOut>", self.restore_ip_placeholder)
        self.ip_entry['validatecommand'] = (master.register(self.validate_ip_char), '%P')

        # --- Port Input ---
        self.port_label = tk.Label(master, text="Port:")
        self.port_entry = tk.Entry(master, fg='grey', validate='key')
        self.port_entry.insert(0, "12345")  # Default value
        self.port_entry.bind("<FocusIn>", self.clear_port_placeholder)
        self.port_entry.bind("<FocusOut>", self.restore_port_placeholder)
        self.port_entry['validatecommand'] = (master.register(self.validate_port_char), '%P')

        # --- Confirm Button ---
        self.confirm_button = tk.Button(master, text="Start Game", command=self.validate_inputs)
        self.confirm_button.pack(pady=10)

        # Initial field visibility
        self.update_field_visibility()

    # Show/hide IP/port fields based on selected game mode
    def update_field_visibility(self):
        mode = self.game_mode.get()

        self.ip_label.pack_forget()
        self.ip_entry.pack_forget()
        self.port_label.pack_forget()
        self.port_entry.pack_forget()

        if mode == "local_2p":
            self.port_label.pack()
            self.port_entry.pack()
        elif mode == "network":
            self.ip_label.pack()
            self.ip_entry.pack()
            self.port_label.pack()
            self.port_entry.pack()

    # --- Placeholder management ---
    def clear_ip_placeholder(self, event):
        if self.ip_entry.get() == "127.0.0.1":
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.config(fg='black')

    def restore_ip_placeholder(self, event):
        if self.ip_entry.get() == "":
            self.ip_entry.insert(0, "127.0.0.1")
            self.ip_entry.config(fg='grey')

    def clear_port_placeholder(self, event):
        if self.port_entry.get() == "12345":
            self.port_entry.delete(0, tk.END)
            self.port_entry.config(fg='black')

    def restore_port_placeholder(self, event):
        if self.port_entry.get() == "":
            self.port_entry.insert(0, "12345")
            self.port_entry.config(fg='grey')

    # --- Input validation ---
    def validate_ip_char(self, value):
        # Only allow digits and dots (valid IP format)
        return re.fullmatch(r'[0-9.]*', value) is not None

    def validate_port_char(self, value):
        # Only allow numeric port, max 5 digits
        return re.fullmatch(r'\d{0,5}', value) is not None

    def validate_inputs(self):
        mode = self.game_mode.get()
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        # Validate IP if needed
        if mode == "network":
            ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
            if not re.match(ip_pattern, ip):
                messagebox.showerror("Invalid Input", "Please enter a valid IP address.")
                return

        # Validate port
        if mode in ["local_2p", "network"]:
            if not port.isdigit() or not (1 <= int(port) <= 65535):
                messagebox.showerror("Invalid Input", "Please enter a valid port number (1-65535).")
                return

        # Build result based on mode
        config_data = {"mode": mode, "ip": None, "port": None}

        if mode == "network":
            config_data["ip"] = ip
            config_data["port"] = int(port)
        elif mode == "local_2p":
            config_data["port"] = int(port)

        self.result = config_data
        self.master.destroy()

# Opens the config dialog window and returns selected values
def get_config():
    root = tk.Tk()
    root.geometry("300x300+600+200")  # Size + center placement
    dialog = ConfigDialog(root)
    root.mainloop()
    return dialog.result

# Dialog to choose from where to load saved game state
def select_save_source():
    class SaveSourceDialog:
        def __init__(self, master):
            self.master = master
            master.title("Select Save Source")
            self.selected = None

            tk.Label(master, text="Select source to load game state:").pack(pady=10)

            self.var = tk.StringVar(value="json")
            tk.Radiobutton(master, text="JSON", variable=self.var, value="json").pack(anchor="w", padx=20)
            tk.Radiobutton(master, text="XML", variable=self.var, value="xml").pack(anchor="w", padx=20)
            tk.Radiobutton(master, text="MongoDB", variable=self.var, value="mongo").pack(anchor="w", padx=20)

            tk.Button(master, text="Continue", command=self.set_and_close).pack(pady=10)

        def set_and_close(self):
            self.selected = self.var.get()
            self.master.destroy()

    root = tk.Tk()
    root.geometry("250x200+600+300")
    dialog = SaveSourceDialog(root)
    root.mainloop()
    return dialog.selected

