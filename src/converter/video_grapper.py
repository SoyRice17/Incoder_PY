import ffmpeg
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
            print(f"검사 중인 파일: {filename}")  # 디버깅용
            for keyword in keyword_list:
                print(f"  키워드 '{keyword}' 검사 중")  # 디버깅용
                if keyword.lower() in filename.lower():
                    print(f"  매치 발견: {filename} - {keyword}")  # 디버깅용
                    full_path = os.path.join(self.target_path, filename)
                    video_groups[keyword].append(full_path)
        
        # 결과 출력
        for keyword, files in video_groups.items():
            print(f"\n{keyword}에 대한 파일들:")
            for file in files:
                print(f"  - {file}")
        
        return video_groups
        
        
        
