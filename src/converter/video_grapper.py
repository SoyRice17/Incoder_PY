import os
import util
from typing import Optional
from constants.config_constants import FILE_PATH
from util.config_manager import ConfigManager

class VideoGrapper:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.io = util.LogIOManager()
        self.config_manager = ConfigManager()
        
        # config에서 데이터 가져오기
        self.target_path = self.config_manager.config.get(FILE_PATH, {}).get("target_path", "")
        self.keyword_list = self.config_manager.config.get("repeat_title", {}).get("keywords", [])
        if not self.keyword_list:
            self.keyword_list = []
        
    def get_video_list(self, input_keyword: Optional[str] = None) -> dict[str, list[str]]:
        self.io.log("\n=== 비디오 파일 검색 시작 ===")
        
        if (not self.keyword_list) and input_keyword is None:
            self.io.log("키워드가 없습니다.")
            return {}
        
        if input_keyword and input_keyword not in self.keyword_list:
            self.keyword_list.append(input_keyword)
            self.io.log(f"검색할 키워드 목록: {self.keyword_list}")
            
        # 키워드별 그룹 초기화
        video_groups = {keyword: [] for keyword in self.keyword_list}
        
        # 파일 검색
        if not self.target_path:
            self.io.log("대상 경로가 설정되지 않았습니다.")
            return {}
            
        self.io.log(f"\n대상 경로: {self.target_path}")
        for filename in os.listdir(self.target_path):
            for keyword in self.keyword_list:
                if keyword.lower() in filename.lower():
                    full_path = os.path.join(self.target_path, filename)
                    video_groups[keyword].append(full_path)
                    self.io.log(f"키워드 '{keyword}'에 매칭된 파일: {filename}")
        
        # 결과 요약
        self.io.log("\n=== 검색 결과 ===")
        for keyword, videos in video_groups.items():
            self.io.log(f"키워드 '{keyword}': {len(videos)}개 파일 발견")
            
        # 설정 저장
        self.config_manager.config["repeat_title"] = {"keywords": self.keyword_list}
        self.config_manager.save_config()
        
        return video_groups
        
        
        
