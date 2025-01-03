import json
import os 
import util 
from typing import Optional
from constants.config_constants import FILE_PATH

class JsonIOManager:
    def __init__(self):
        self.io = util.LogIOManager()
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
            self.io.log("jsons 디렉토리가 없습니다. 생성 중...")
            
        if not os.path.exists(self.config_path):
            self.io.log("config.json 파일이 없습니다. 생성 중...")
            self.write_json(self.config_path, self.initial_config)
            
    def isNonePath(self, path_name: str) -> bool:
        #target_path의 value가 없는지 확인
        """ with: 컨텍스트 매니저를 시작하는 키워드
                리소스를 자동으로 관리함
                블록이 끝나면 자동으로 파일을 닫음
            open(): 파일을 여는 함수
                self.config_path: 열려는 파일의 경로
                'r': read 모드 (읽기 전용)
                다른 모드들:
                'w': write (쓰기)
                'a': append (추가)
                'r+': read and write (읽기와 쓰기)
            as f: 열린 파일 객체를 f라는 변수에 저장해
        """
        with open(self.config_path, 'r', encoding="utf-8") as f:
            config = json.load(f) # 딕셔너리 형태로 파일 읽기
        #target_path의 value가 없는지 확인
        if config[FILE_PATH].get(path_name) == "":
            return True
        else:
            return False
            
    def read_json(self, file_path : str) -> dict:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.io.log(f"파일을 찾을 수 없습니다: {file_path}")
            return {}
        except Exception as e:
            self.io.log(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return {}
    
    def write_json(self, file_path : str, data : dict) -> None:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2) # ensure_ascii=False : 한글 깨짐 방지, indent=2 : 들여쓰기 2칸
        except Exception as e:
            self.io.log(f"파일을 쓰는 중 오류가 발생했습니다: {e}")
            
    def update_json(self, file_path: str, data: dict) -> None:
        try:
            existing_data = self.read_json(file_path)
            existing_data.update(data)
            self.write_json(file_path, existing_data)
            self.io.log(f"파일 업데이트 완료: {file_path}")
            
        except Exception as e:
            self.io.log(f"파일을 업데이트하는 중 오류가 발생했습니다: {e}")
            

    def save_path(self, path_name: str, path_value: str) -> None:
        """파일 경로를 config.json에 저장 (업데이트 방식)"""
        try:
            # 1. 파일 읽기 ('r+' 모드로 읽기+쓰기)
            with open(self.config_path, 'r+') as f:
                config = json.load(f)
            
                # 2. 특정 경로 값만 업데이트
                config[FILE_PATH][path_name] = path_value
                
                # 3. 파일 포인터를 처음으로 이동
                f.seek(0)
                
                # 4. 기존 내용 삭제
                f.truncate()
                
                # 5. 업데이트된 내용 쓰기
                json.dump(config, f, indent=2)
            
            self.io.log(f"경로 업데이트 완료: {path_name} = {path_value}")
            
        except Exception as e:
            self.io.log(f"경로 저장 중 오류 발생: {e}")

    def get_path(self, target_path: str, path_name: Optional[str] = None) -> str:
        """저장된 파일 경로 가져오기"""
        with open(self.config_path, 'r', encoding="utf-8") as f:
            config = json.load(f)

        if path_name is None:
            return config.get(target_path)
        else:
            return config[target_path].get(path_name)