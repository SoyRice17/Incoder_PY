import json
import os
from constants.config_constants import CONFIG_FILE, FILE_PATH, TARGET_PATH


class InitPath:
    def __init__(self):
        """ __file__:
            현재 파일: /Users/.../shanaMacro/src/util/init_path.py
            ↓ dirname 한 번
            /Users/.../shanaMacro/src/util
            ↓ dirname 한 번 더
            /Users/.../shanaMacro/src
            ↓ config.json 결합
            /Users/.../shanaMacro/src/config.json"""
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG_FILE)
    
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
        with open(self.config_path, 'r') as f:
            config = json.load(f) # 딕셔너리 형태로 파일 읽기
        #target_path의 value가 없는지 확인
        if config[FILE_PATH].get(path_name) == "":
            return True
        else:
            return False
        
    def save_path(self, path_name: str, path_value: str) -> None:
        #파일 경로를 config.json에 저장
        with open(self.config_path, 'r+') as f:
            config = json.load(f)
            config[FILE_PATH][path_name] = path_value
            
            f.seek(0) # 파일 포인터를 파일의 처음으로 이동
            f.truncate() # 파일의 나머지 부분을 삭제
            json.dump(config, f, indent=2) # 딕셔너리를 파일에 쓰기
            
    def get_path(self, path_name: str) -> str:
        """저장된 파일 경로 가져오기"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
            
        return config[FILE_PATH].get(path_name)
