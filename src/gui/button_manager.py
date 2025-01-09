import os
from util import LogIOManager
from constants.config_constants import TARGET_PATH, FILE_PATH
from converter.video_grapper import VideoGrapper
from util.config_manager import ConfigManager

class ButtonManager:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.path_instance = self.gui_instance.path_instance
        self.logger = LogIOManager()
        self.video_grapper = VideoGrapper(gui_instance)
        self.config_manager = ConfigManager()
    
    def refresh_file_list(self) -> None:
        target_path = self.path_instance.get_path(FILE_PATH, TARGET_PATH)
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
            if not videos:
                self.gui_instance.selected_file_name_listbox.insert('end', f"{keyword}")
            else:
                self.gui_instance.selected_file_name_listbox.insert('end', keyword)
                for video in videos:
                    self.gui_instance.selected_file_name_listbox.insert('end', f"    ㄴ {video}")
        
    def delete_selected_file_listbox(self) -> None:
        try:
            # 엔트리에서 입력값 가져오기
            delete_name = self.gui_instance.input_file_name_entry.get().strip()
            if not delete_name:
                return
            
            # 리스트박스의 모든 항목을 순회하면서 일치하는 항목 찾기
            items = self.gui_instance.selected_file_name_listbox.get(0, 'end')
            for idx, item in enumerate(items):
                if item == delete_name and "ㄴ" not in item:
                    self.gui_instance.selected_file_name_listbox.delete(idx)
                    # ConfigManager 사용
                    keywords = self.config_manager.config.get("repeat_title", {}).get("keywords", [])
                    if delete_name in keywords:
                        keywords.remove(delete_name)
                        self.config_manager.config["repeat_title"] = {"keywords": keywords}
                        self.config_manager.save_config()
                    self.add_video_list(self.video_grapper.get_video_list())
                    self.gui_instance.input_file_name_entry.delete(0, 'end')  # 엔트리 초기화
                    return
                    
            self.logger.log(f"'{delete_name}' 항목을 찾을 수 없습니다.")
            
        except Exception as e:
            self.logger.log(f"삭제 중 오류가 발생했습니다: {e}")
    
    def save_setting(self) -> None:
        try:
            self.codec = self.gui_instance.codec_combobox.get()
            self.resolution = self.gui_instance.resolution_combobox.get()
            self.crf = self.gui_instance.crf_entry.get()
            self.frame_rate = self.gui_instance.frame_rate_entry.get()
            
            self.config_manager.config["setting"]["codec"] = self.codec
            self.config_manager.config["setting"]["resolution"] = self.resolution
            self.config_manager.config["setting"]["crf"] = self.crf
            self.config_manager.config["setting"]["frame_rate"] = self.frame_rate
            
            self.config_manager.save_config()
            self.gui_instance.close_setting_screen()
            
            self.logger.log("설정이 저장되었습니다.")
        except Exception as e:
            self.logger.log(f"설정 저장 중 오류가 발생했습니다: {e}")
        
        