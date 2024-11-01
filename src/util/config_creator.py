import os
import json
class ConfigCreator:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        self.initial_config = {
            "file_PATH": {
                "target_path": ""
            },
            "repeat_title": {}
        }
    def create_config(self):
        if os.path.exists(self.config_path):
            return True
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)  # 디렉토리가 없으면 생성
            with open(self.config_path, "w") as f:
                json.dump(self.initial_config, f, indent=2)
            return True
        except Exception as e:
            print(f"설정 파일 생성 중 오류 발생: {str(e)}")
            return False
        


