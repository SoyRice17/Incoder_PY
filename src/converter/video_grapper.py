import os
import gui.gui_manager as gui_manager

class VideoGrapper:
    def __init__(self,gui_instance):
        self.path_instance = gui_instance.path_instance
        self.gui_instance = gui_instance
        self.target_path = self.path_instance.get_path("target_path")
        
    def get_video_list(self) -> dict[str, list[str]]:
        keyword_list = [self.gui_instance.selected_file_name_listbox.get(i) 
                        for i in range(self.gui_instance.selected_file_name_listbox.size())]
        
        video_groups = {keyword: [] for keyword in keyword_list}
        
        for filename in os.listdir(self.target_path):
            for keyword in keyword_list:
                if keyword.lower() in filename.lower():
                    full_path = os.path.join(self.target_path, filename)
                    video_groups[keyword].append(full_path)
        
        return video_groups
        
        
        
