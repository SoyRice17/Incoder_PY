import json
import os
from constants.config_constants import CONFIG_FILE, FILE_PATH, TARGET_PATH


class InitPATH:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG_FILE)
    
    def isNonePath(self) -> bool:
        """target_path의 value가 없는지 확인"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
            
        if config[FILE_PATH].get(TARGET_PATH) == "":
            return True
        else:
            return False
        
    def save_path(self, path_name: str, path_value: str) -> None:
        """파일 경로를 config.json에 저장"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
            
        config[FILE_PATH][path_name] = path_value
            
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
                
    def get_path(self, path_name: str) -> str:
        """저장된 파일 경로 가져오기"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
            
        return config[FILE_PATH].get(path_name)
