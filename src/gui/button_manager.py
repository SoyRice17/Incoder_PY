import os
from constants.config_constants import TARGET_PATH

class ButtonManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.path_instance = self.gui_instance.path_instance
    
    def refresh_file_list(self) -> None:
        target_path = self.path_instance.get_path(TARGET_PATH)
        if not target_path:
            return
        file_list = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
        file_list.sort()
        
        self.gui_instance.file_listbox.delete(0, 'end')
        for file_name in file_list:
            self.gui_instance.file_listbox.insert('end', file_name)
    
    def confirm_selection(self) -> None:
        input_name = self.gui_instance.input_file_name_entry.get()
        if not input_name:
            return
        self.gui_instance.selected_file_name_listbox.insert('end', input_name)
        self.gui_instance.input_file_name_entry.delete(0, 'end')
        
    def delete_selected_file_listbox(self) -> None:
        delete_name = self.gui_instance.input_file_name_entry.get()
        if not delete_name:
            return
        
        for i in range(self.gui_instance.selected_file_name_listbox.size()):
            if self.gui_instance.selected_file_name_listbox.get(i) == delete_name:
                self.gui_instance.selected_file_name_listbox.delete(i)
                break
        self.gui_instance.input_file_name_entry.delete(0, 'end')
        
    def execute_file_conversion(self) -> None:
        file_dir_list = []
        pass
