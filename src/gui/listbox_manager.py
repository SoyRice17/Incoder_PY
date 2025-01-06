from util import LogIOManager 
from converter import VideoGrapper 
from gui import ButtonManager 
from util.config_manager import ConfigManager

class ListboxManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.logger = LogIOManager()
        self.grapper = VideoGrapper(self.gui_instance)
        self.button = ButtonManager(self.gui_instance)
        self.config_manager = ConfigManager()
        
    def delete_selected_file_name(self, event) -> None:
        try:
            selected_indices = self.gui_instance.selected_file_name_listbox.curselection()
            if not selected_indices:
                return
            
            delete_name = self.gui_instance.selected_file_name_listbox.get(selected_indices[0])
            if not delete_name:
                return
            
            if "ㄴ" not in delete_name:
                self.gui_instance.selected_file_name_listbox.delete(selected_indices[0])
                # ConfigManager 사용
                keywords = self.config_manager.config.get("repeat_title", {}).get("keywords", [])
                if delete_name in keywords:
                    keywords.remove(delete_name)
                    self.config_manager.config["repeat_title"] = {"keywords": keywords}
                    self.config_manager.save_config()
                self.button.add_video_list(self.grapper.get_video_list())
            else:
                self.logger.log(f"{delete_name} 경로는 삭제할 수 없습니다.")
        except Exception as e:
            self.logger.log(f"삭제 중 오류가 발생했습니다: {e}")

    def insert_input_file_name_entry(self, event) -> None:
        try:
            input_name = self.gui_instance.file_listbox.get(self.gui_instance.file_listbox.curselection())
            self.gui_instance.input_file_name_entry.insert(0, input_name)
        except Exception as e:
            self.logger.log(f"입력 중 오류가 발생했습니다: {e}")
