import os
import converter.video_grapper as video_grapper
from constants.config_constants import TARGET_PATH, FILE_PATH

class ButtonManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.path_instance = self.gui_instance.path_instance
        self.video_grapper = video_grapper.VideoGrapper(gui_instance)
        
    def refresh_file_list(self) -> None:
        target_path = self.path_instance.get_path(FILE_PATH,TARGET_PATH)
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
        self.add_video_list(self.video_grapper.get_video_list(input_name))
        self.gui_instance.input_file_name_entry.delete(0, 'end')
        
    
    def add_video_list(self, video_list: dict[str, list[str]]) -> None:
        self.gui_instance.selected_file_name_listbox.delete(0, 'end')
        for keyword, videos in video_list.items():
            if videos == [] or videos == None:
                self.gui_instance.selected_file_name_listbox.insert('end', f"{keyword}")
            elif videos:
                self.gui_instance.selected_file_name_listbox.insert('end', keyword)
                for video in videos:
                    self.gui_instance.selected_file_name_listbox.insert('end', f"    ㄴ {video}")
        
    def delete_selected_file_listbox(self) -> None:
        delete_name = self.gui_instance.input_file_name_entry.get()
        if not delete_name:
            return
        
        for i in range(self.gui_instance.selected_file_name_listbox.size()):
            if self.gui_instance.selected_file_name_listbox.get(i) == delete_name:
                self.gui_instance.selected_file_name_listbox.delete(i)
                break
        self.gui_instance.input_file_name_entry.delete(0, 'end')
        