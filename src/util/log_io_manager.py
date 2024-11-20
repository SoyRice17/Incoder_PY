import tkinter as tk
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional , override

class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass
    
    @abstractmethod
    def clear_log(self) -> None:
        pass
    
class ConsoleLogger(Logger):
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='log.txt'
        )
        
    @override
    def log(self, message: str) -> None:
        print(message)
        logging.info(message)
        
    @override
    def clear_log(self) -> None:
        with open('log.txt', 'w') as f:
            f.write(f"log cleared at {datetime.now()}")
        for _ in range(10):
            print()
            

class GuiLogger(Logger):
    def __init__(self, widget: tk.Text, root: tk.Tk):
        self.log_text = widget
        self.root = root
        
    @override
    def log(self, message: str) -> None:
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.yview(tk.END)
        self.root.update()
        
    @override
    def clear_log(self) -> None:
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.root.update()

class LogIOManager():
    _instance = None
    _logger: Optional[Logger] = None
    _widget: Optional[tk.Text] = None
    _root: Optional[tk.Tk] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._logger = ConsoleLogger()
        return cls._instance
    
    @classmethod
    def initialize_gui(cls, widget: tk.Text, root: tk.Tk) -> None:
        cls._widget = widget
        cls._root = root
    
    @classmethod
    def switch_to_gui(cls) -> None:
        cls._logger = GuiLogger(cls._widget, cls._root)
        
    @classmethod
    def switch_to_console(cls) -> None:
        cls._logger = ConsoleLogger()
    
    @classmethod
    def log(cls, message: str) -> None:
        cls._logger.log(message)
        
    @classmethod
    def clear_log(cls) -> None:
        cls._logger.clear_log()