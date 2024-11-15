import json
import os 

class JsonIOManager:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        self.jsons_path = os.path.join(self.base_path, "jsons")
        self.config_path = os.path.join(self.jsons_path, "config.json")
        
        self.initial_config = {
            "file_PATH": {
                "target_path": "",
                "output_path": ""
            },
            "repeat_title": {} 
        }
        # 디렉토리가 없으면 생성
        self._init_structure()
    
    def _init_structure(self):
        if not os.path.exists(self.jsons_path):
            os.makedirs(self.jsons_path)
            print("jsons 디렉토리가 없습니다. 생성 중...")
            
        if not os.path.exists(self.config_path):
            print("config.json 파일이 없습니다. 생성 중...")
            self.write_json(self.config_path, self.initial_config)
            
    def read_json(self, file_path : str) -> dict:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return {}
        except Exception as e:
            print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return {}
    
    def write_json(self, file_path : str, data : dict) -> None:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2) # ensure_ascii=False : 한글 깨짐 방지, indent=2 : 들여쓰기 2칸
        except Exception as e:
            print(f"파일을 쓰는 중 오류가 발생했습니다: {e}")
