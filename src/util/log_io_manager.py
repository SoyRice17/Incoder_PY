
import tkinter as tk

class LogIOManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.log_text = gui_instance.log_text
        
    def log(self, message: str) -> None:
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.yview(tk.END)
        self.gui_instance.root.update()
        
    def clear_log(self) -> None:
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.gui_instance.root.update()
