from util import LogIOManager 
from util import JsonIOManager 
from converter import VideoGrapper 
from gui import ButtonManager 

class ListboxManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.logger = LogIOManager()
        self.json = JsonIOManager()
        self.grapper = VideoGrapper(self.gui_instance)
        self.button = ButtonManager(self.gui_instance)
        
    def delete_selected_file_name(self, event) -> None:
        try:
            # 선택된 항목이 있는지 먼저 확인
            selected_indices = self.gui_instance.selected_file_name_listbox.curselection()
            if not selected_indices:  # 선택된 항목이 없으면
                return
            
            delete_name = self.gui_instance.selected_file_name_listbox.get(selected_indices[0])
            if not delete_name:
                return
            
            if "ㄴ" not in delete_name:  # 문자열 내에 "ㄴ"이 포함되어 있는지 확인
                self.gui_instance.selected_file_name_listbox.delete(selected_indices[0])
                self.json.remove_keyword(delete_name)
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
