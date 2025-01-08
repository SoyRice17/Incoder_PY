import os
from constants.config_constants import TARGET_PATH, OUTPUT_PATH,FILE_PATH
from tkinter import simpledialog
from util import ConfigManager

class LabelManager:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager
        self.config_manager = ConfigManager()
        
    def update_input_path_label(self):
        input_path = self.config_manager.config["file_PATH"]["target_path"]
        self.gui_manager.input_path_label.config(text=f"파일 경로: {input_path}")
        
    def update_output_path_label(self):
        output_path = self.config_manager.config["file_PATH"]["output_path"]
        self.gui_manager.output_path_label.config(text=f"출력 경로: {output_path}")
        
    def update_setting_value_label(self):
        setting_value = self.config_manager.config["setting"]
        self.gui_manager.setting_value_label.config(
            text=f"설정 값: codec: {setting_value['codec']}, resolution: {setting_value['resolution']}, crf: {setting_value['crf']}, frame_rate: {setting_value['frame_rate']}, bit_rate: {setting_value['bit_rate']}")
    
    def set_input_path_label(self):
        input_path = simpledialog.askstring("파일 경로", "파일 경로를 입력하세요:")
        if input_path:
            self.config_manager.config["file_PATH"]["target_path"] = input_path
            self.config_manager.save_config()
            self.gui_manager.input_path_label.config(text=f"파일 경로: {input_path}")
        
    def set_output_path_label(self):
        output_path = simpledialog.askstring("출력 경로", "출력 경로를 입력하세요:")
        if output_path:
            self.config_manager.config["file_PATH"]["output_path"] = output_path
            self.config_manager.save_config()
            self.gui_manager.output_path_label.config(text=f"출력 경로: {output_path}")
        