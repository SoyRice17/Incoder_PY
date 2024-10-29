import tkinter as tk
import util.initPATH as path_manager
from constants.gui_constants import WINDOW_TITLE, WINDOW_SIZE
from constants.path_constants import DEFAULT_PATH

class GuiManager:
    def __init__(self):
        self.root = tk.Tk() #Tk: 파이썬 GUI 프로그램의 기본 윈도우 객체
        self.root.title(WINDOW_TITLE)  # 윈도우 제목
        self.root.geometry(WINDOW_SIZE)  # 윈도우 크기
        
        self.path_instance = path_manager.InitPATH()  # InitPATH 인스턴스 생성
        
        if self.path_instance.isNonePath(): # target_path의 value(경로)가 없는지 확인
            self.init_path()
        else:
            self.init_gui()
        
    def init_path(self):
        # 메인 프레임
        main_frame = tk.Frame(self.root) #Frame: 윈도우 내에서 다른 위젯을 배치하는 컨테이너
        main_frame.pack(fill=tk.BOTH, expand=True) 
        """ pack: 위젯을 컨테이너에 배치하는 메서드
            fill=tk.BOTH: 컨테이너를 부모 윈도우에 맞게 크기 조절
            expand=True: 컨테이너를 부모 윈도우에 맞게 크기 조절"""
        
        # 안내 문구 레이블 추가
        self.instruction_label = tk.Label(main_frame, text="파일디렉토리를 설정하세요") # Label: 텍스트 또는 이미지를 표시하는 위젯
        self.instruction_label.pack(pady=10) #pack: 위젯을 컨테이너에 배치하는 메서드 , pady=10: 위젯과 컨테이너 사이의 여백
        
        # 텍스트 박스 추가
        self.text_box = tk.Text(main_frame, height=3, width=50) # Text: 여러 줄의 텍스트를 표시하고 입력할 수 있는 위젯
        self.text_box.pack(pady=10) #pack: 위젯을 컨테이너에 배치하는 메서드 , pady=10: 위젯과 컨테이너 사이의 여백
        
        # 기본 경로 출력
        self.text_box.insert(tk.END, DEFAULT_PATH) #insert: 텍스트 박스에 텍스트를 삽입하는 메서드 , tk.END: 텍스트 박스의 끝에 텍스트를 삽입   
        
        # 버튼 추가
        save_button = tk.Button(main_frame, text="저장", command=self.save_target_path)
        save_button.pack(pady=10)
        
        # 상태 표시 레이블 추가
        self.status_label = tk.Label(main_frame, text="")
        self.status_label.pack(pady=10)
        
    def save_target_path(self):
        # 텍스트 박스에서 경로 가져오기
        path_value = self.text_box.get("1.0", tk.END).strip() #get: 텍스트 박스에서 텍스트를 가져오는 메서드 , "1.0": 텍스트 박스의 첫 번째 줄의 첫 번째 문자 , tk.END: 텍스트 박스의 끝 , strip(): 문자열의 양쪽 끝에서 공백 문자를 제거하는 메서드
        
        # 경로 저장
        self.path_instance.save_path("target_path", path_value)
        
        # 상태 업데이트
        self.status_label.config(text="경로가 저장되었습니다!") #config: 위젯의 속성을 설정하는 메서드
        
        # 잠시 후 메인 GUI로 전환
        self.root.after(1500, self.switch_to_main_gui) #after: 지정된 시간 후에 함수를 호출하는 메서드 , 1500: 1.5초 , self.switch_to_main_gui: 메인 GUI로 전환하는 메서드
        
    def switch_to_main_gui(self):
        # 현재 프레임의 모든 위젯 제거
        for widget in self.root.winfo_children(): #winfo_children(): 윈도우에 있는 모든 위젯을 반환하는 메서드  
            widget.destroy() # 모든 위젯 제거
        
        # 메인 GUI 초기화
        self.init_gui()
        
    def init_gui(self):
        # 메인 GUI 구현
        pass  # 여기에 메인 GUI 코드 구현
        
    def run(self):
        self.root.mainloop() #mainloop: 윈도우 이벤트 루프를 시작하는 메서드

if __name__ == "__main__":
    gui = GuiManager()
    gui.run()
