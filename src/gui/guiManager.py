import tkinter as tk
import tkinter.ttk as ttk
import util.initPATH as path_manager
from gui.buttonManager import ButtonManager
from gui.listboxManager import ListboxManager
from constants.gui_constants import WINDOW_TITLE, WINDOW_SIZE
from constants.path_constants import DEFAULT_PATH

class GuiManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        self.path_instance = path_manager.InitPATH()
        self.button_manager = ButtonManager(self)
        self.listbox_manager = ListboxManager(self)
        
        # 메인 프레임 생성 (모든 화면이 공유)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 초기 화면 설정
        self.show_appropriate_screen()
        
        self.loading_screen_active = False  # 로딩 화면 상태 추적용
    
    def show_appropriate_screen(self):
        # 로딩 화면 표시
        self.show_loading_screen()
        
        # 현재 프레임 내용 제거
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        if self.path_instance.isNonePath():
            self.show_path_screen()
        else:
            self.show_main_screen()
    
    def show_loading_screen(self):
        # 현재 프레임 내용 제거
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        loading_label = tk.Label(self.main_frame, text="화면을 불러오는 중...", font=('Helvetica', 12))
        loading_label.pack(expand=True)
        self.loading_screen_active = True
        self.root.update()  # GUI 즉시 업데이트
    
    def show_path_screen(self):
        """pack: 위젯을 컨테이너에 배치하는 메서드
            fill=tk.BOTH: 컨테이너를 부모 윈도우에 맞게 크기 조절
            expand=True: 컨테이너를 부모 윈도우에 맞게 크기 조절 """
        
        # 안내 문구 레이블 추가
        self.instruction_label = tk.Label(self.main_frame, text="파일디렉토리를 설정하세요") # Label: 텍스트 또는 이미지를 표시하는 위젯
        self.instruction_label.pack(pady=10) #pack: 위젯을 컨테이너에 배치하는 메서드 , pady=10: 위젯과 컨테이너 사이의 여백
        
        # 텍스트 박스 추가
        self.text_box = tk.Text(self.main_frame, height=3, width=50) # Text: 여러 줄의 텍스트를 표시하고 입력할 수 있는 위젯
        self.text_box.pack(pady=10) #pack: 위젯을 컨테이너에 배치하는 메서드 , pady=10: 위젯과 컨테이너 사이의 여백
        
        # 기본 경로 출력
        self.text_box.insert(tk.END, DEFAULT_PATH) #insert: 텍스트 박스에 텍스트를 삽입하는 메서드 , tk.END: 텍스트 박스의 끝에 텍스트를 삽입   
        
        # 버튼 추가
        save_button = tk.Button(self.main_frame, text="저장", command=self.save_target_path)
        save_button.pack(pady=10)
        
        # 상태 표시 레이블 추가
        self.status_label = tk.Label(self.main_frame, text="")
        self.status_label.pack(pady=10)
    
    def show_main_screen(self):
        # 기존 init_gui의 내용
        top_frame = tk.Frame(self.main_frame)
        bottom_frame = tk.Frame(self.main_frame)
        
        # 메인 GUI 구현
        top_frame = tk.Frame(self.main_frame)
        bottom_frame = tk.Frame(self.main_frame)
        top_left_frame = tk.Frame(top_frame)
        top_right_frame = tk.Frame(top_frame)
        
        #separator = tk.Frame(top_frame, height=2, bg="gray")
        #separator_bottom = tk.Frame(bottom_frame, height=2, bg="gray")
        
        self.selected_file_name_listbox = tk.Listbox(top_right_frame)
        self.selected_file_name_listbox.bind('<Double-Button-1>', self.listbox_manager.delete_selected_file_name)
        self.file_listbox = tk.Listbox(top_left_frame)
        self.file_listbox.bind('<Double-Button-1>', self.listbox_manager.insert_input_file_name_entry)
        self.refresh_button = tk.Button(
            bottom_frame, 
            text="새로고침",
            command=self.button_manager.refresh_file_list
        )
        
        self.input_file_name_entry = tk.Entry(bottom_frame)
        self.confirm_button = tk.Button(
            bottom_frame, 
            text="확인",
            command=self.button_manager.confirm_selcetion
        )
        self.delete_button = tk.Button(
            bottom_frame, 
            text="삭제",
            command=self.button_manager.delete_selected_file_listbox
        )
        self.execute_button = tk.Button(
            bottom_frame, 
            text="실행",
            #command=self.button_manager.execute_file_conversion
        )
        
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        top_frame.pack(fill=tk.BOTH, expand=True)
        top_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        top_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        
        self.selected_file_name_listbox.pack(fill=tk.BOTH, expand=True)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.input_file_name_entry.pack(fill=tk.X, pady=10, expand=True)
        self.refresh_button.pack(side=tk.LEFT, padx=15)
        self.confirm_button.pack(side=tk.LEFT, padx=15)
        self.delete_button.pack(side=tk.LEFT, padx=15)
        self.execute_button.pack(side=tk.LEFT, padx=15)
        
        self.button_manager.refresh_file_list()
        
    def save_target_path(self):
        # 텍스트 박스에서 경로 가져오기
        path_value = self.text_box.get("1.0", tk.END).strip() #get: 텍스트 박스에서 텍스트를 가져오는 메서드 , "1.0": 텍스트 박스의 첫 번째 줄의 첫 번째 문자 , tk.END: 텍스트 박스의 끝 , strip(): 문자열의 양쪽 끝에서 공백 문자를 제거하는 메서드
        
        # 경로 저장
        self.path_instance.save_path("target_path", path_value)
        
        # 상태 업데이트
        self.status_label.config(text="경로가 저장되었습니다!") #config: 위젯의 속성을 설정하는 메서드
        
        # 잠시 후 메인 GUI로 전환
        self.root.after(1500, self.show_appropriate_screen) #after: 지정된 시간 후에 함수를 호출하는 메서드 , 1500: 1.5초 , self.show_appropriate_screen: 적절한 화면으로 전환하는 메서드
        
    def run(self):
        self.root.mainloop() #mainloop: 윈도우 이벤트 루프를 시작하는 메서드

if __name__ == "__main__":
    gui = GuiManager()
    gui.run()
