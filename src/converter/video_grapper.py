import os
import gui.gui_manager as gui_manager

class VideoGrapper:
    def __init__(self,gui_instance):
        self.path_instance = gui_instance.path_instance
        self.gui_instance = gui_instance
        self.target_path = self.path_instance.get_path("target_path")
        
    def get_video_list(self) -> dict[str, list[str]]:
        print("\n=== 비디오 파일 검색 시작 ===")
        
        # 키워드 목록 가져오기
        keyword_list = [self.gui_instance.selected_file_name_listbox.get(i) 
                        for i in range(self.gui_instance.selected_file_name_listbox.size())]
        print(f"검색할 키워드 목록: {keyword_list}")
        
        # 키워드별 그룹 초기화
        video_groups = {keyword: [] for keyword in keyword_list}
        
        # 파일 검색
        print(f"\n대상 경로: {self.target_path}")
        for filename in os.listdir(self.target_path):
            for keyword in keyword_list:
                if keyword.lower() in filename.lower():
                    full_path = os.path.join(self.target_path, filename)
                    video_groups[keyword].append(full_path)
                    print(f"키워드 '{keyword}'에 매칭된 파일: {filename}")
        
        # 결과 요약
        print("\n=== 검색 결과 ===")
        for keyword, videos in video_groups.items():
            print(f"키워드 '{keyword}': {len(videos)}개 파일 발견")
            for video in videos:
                print(f"  - {os.path.basename(video)}")
        
        print("\n=== 비디오 파일 검색 완료 ===")
        return video_groups
        
        
        
