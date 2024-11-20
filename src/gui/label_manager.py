import os
from constants.config_constants import TARGET_PATH, OUTPUT_PATH,FILE_PATH
from tkinter import simpledialog

class LabelManager:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager
        self.path_instance = self.gui_manager.path_instance
        
    def update_input_path_label(self):
        input_path = self.path_instance.get_path(FILE_PATH,TARGET_PATH)
        self.gui_manager.input_path_label.config(text=f"파일 경로: {input_path}")
        
    def update_output_path_label(self):
        output_path = self.path_instance.get_path(FILE_PATH,OUTPUT_PATH)
        self.gui_manager.output_path_label.config(text=f"출력 경로: {output_path}")
    
    def set_input_path_label(self):
        input_path = simpledialog.askstring("파일 경로", "파일 경로를 입력하세요:")
        if input_path:
            self.path_instance.save_path(TARGET_PATH, input_path)
            self.gui_manager.input_path_label.config(text=f"파일 경로: {input_path}")
        
    def set_output_path_label(self):
        output_path = simpledialog.askstring("출력 경로", "출력 경로를 입력하세요:")
        if output_path:
            self.path_instance.save_path(OUTPUT_PATH, output_path)
            self.gui_manager.output_path_label.config(text=f"출력 경로: {output_path}")
        
