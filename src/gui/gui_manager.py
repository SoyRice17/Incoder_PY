# 표준 라이브러리
import tkinter as tk

# 로컬 모듈
import util.init_path as path_manager
from gui.button_manager import ButtonManager
from gui.listbox_manager import ListboxManager
from gui.label_manager import LabelManager
from constants.config_constants import OUTPUT_PATH,TARGET_PATH
from constants.gui_constants import WINDOW_TITLE, WINDOW_SIZE
from constants.path_constants import DEFAULT_PATH

class GuiManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE) # 프로그램 제목
        self.root.geometry(WINDOW_SIZE)# 프로그램 창설정
        
        """ Note
            InitPATH모듈 인스턴스 생성
            isNonePath() = config.json의 key인 target_path의 값이 있는지 확인
            savePath(path_name,path_value) = path_name의 키를 찾고 해당 키에 path_value의 값을 추가
            getPath(path_name) = path_name의 값을 리턴
        """
        self.path_instance = path_manager.InitPath()
        """ Note
            ButtonManager모듈 인스턴스 생성
            refresh_file_list() = 파일 목록을 새로고침하는 메서드
            confirm_selcetion() = gui의 input_file_name_entry에 입력된 파일을 선택한 selected_file_name_listbox에 추가하는 메서드
            delete_selected_file_listbox() = gui의 selected_file_name_listbox에서 선택한 파일을 selected_file_name_listbox에서 삭제하는 메서드
        """
        self.button_manager = ButtonManager(self)
        """ Note
            ListboxManager모듈 인스턴스 생성
            delete_selected_file_name() = gui의 selected_file_name_listbox에서 더블클릭한 파일을 selected_file_name_listbox에서 삭제하는 메서드
            insert_input_file_name_entry() = gui의 file_listbox에서 더블클릭한 파일을 gui의 input_file_name_entry에 추가하는 메서드
        """
        self.listbox_manager = ListboxManager(self)
        """ Note
            LabelManager모듈 인스턴스 생성
            update_input_path_label() = gui의 input_path_label에 파일 경로를 설정하는 메서드
            update_output_path_label() = gui의 output_path_label에 출력 경로를 설정하는 메서드
        """
        self.label_manager = LabelManager(self)
        
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
        for widget in self.main_frame.winfo_children(): #main_frame의 모든 자식 객체를 리턴
            widget.destroy() # 모든 자식 객체를 제거
            
        if self.path_instance.isNonePath(TARGET_PATH): #config.json의 target_path 키의 값이 존재여부 판단
            self.show_path_screen() # 값이 없다면 값을 설정하는 스크린을 출력
        else:
            self.show_main_screen() # 값이 존재하면 메인 스크린 출력
    
    def show_loading_screen(self): # 메인화면에 많은 데이터가 가중될때 화면 출력이 지연되는 것을 방지해 로딩화면 출력
        # 현재 프레임 내용 제거
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        loading_label = tk.Label(self.main_frame, text="화면을 불러오는 중...", font=('Helvetica', 12))
        loading_label.pack(expand=True)
        self.loading_screen_active = True
        self.root.update()  # GUI 즉시 업데이트
    
    # FIX: 파일경로 시스템 필요없어짐 삭제 예정
    def show_path_screen(self):
        """ Note
            pack: 위젯을 컨테이너에 배치하는 메서드
            fill=tk.BOTH: 컨테이너를 부모 윈도우에 맞게 크기 조절
            expand=True: 컨테이너를 부모 윈도우에 맞게 크기 조절 
        """
        # 안내 문구 레이블 추가
        self.instruction_label = tk.Label(self.main_frame, text="파일디렉토리를 설정하세���") # Label: 텍스트 또는 이미지를 표시하는 위젯
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
        top_frame = tk.Frame(self.main_frame)
        bottom_frame = tk.Frame(self.main_frame)
        
        # 메인 GUI 구현
        top_frame = tk.Frame(self.main_frame)
        bottom_frame = tk.Frame(self.main_frame)
        top_left_frame = tk.LabelFrame(
            top_frame,
            text="파일 목록",
            font=('Helvetica', 10),
            relief=tk.RAISED
        )
        top_right_frame = tk.LabelFrame(
            top_frame,
            text="선택 파일 목록",
            font=('Helvetica', 10),
            relief=tk.RAISED
        )
        bottom_top_frame = tk.Frame(
            bottom_frame,
            relief=tk.RAISED,
            borderwidth=1
        )
        bottom_bottom_frame = tk.Frame(
            bottom_frame,
            relief=tk.RAISED,
            borderwidth=1
        )
        
        # 리스트박스 추가
        self.selected_file_name_listbox = tk.Listbox(
            top_right_frame,
            font=('Helvetica', 10),
        )
        self.selected_file_name_listbox.bind('<Double-Button-1>', self.listbox_manager.delete_selected_file_name)
        self.file_listbox = tk.Listbox(
            top_left_frame,
            font=('Helvetica', 10),
        )
        self.file_listbox.bind('<Double-Button-1>', self.listbox_manager.insert_input_file_name_entry)
        
        # 버튼 추가
        self.refresh_button = tk.Button(
            bottom_bottom_frame, 
            text="새로고침",
            command=self.button_manager.refresh_file_list
        )
        self.confirm_button = tk.Button(
            bottom_bottom_frame, 
            text="확인",
            command=self.button_manager.confirm_selection
        )
        self.delete_button = tk.Button(
            bottom_bottom_frame, 
            text="삭제",
            command=self.button_manager.delete_selected_file_listbox
        )
        self.execute_button = tk.Button(
            bottom_bottom_frame, 
            text="실행",
            #command=self.button_manager.execute_file_conversion
        )
        # 레이블 추가
        self.input_path_label = tk.Label(
            bottom_top_frame,
            text="파일 경로",
            font=('Helvetica', 10),
        )
        self.output_path_label = tk.Label(
            bottom_top_frame,
            text="출력 경로",
            font=('Helvetica', 10),
        )
        # 입력 필드 추가
        self.input_file_name_entry = tk.Entry(
            bottom_top_frame,
            font=('Helvetica', 10),
            
        )
        
        # 프레임 배치
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        top_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        top_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        bottom_top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        bottom_bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # 리스트박스 배치
        self.selected_file_name_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.file_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # 입력 필드와 버튼 배치
        self.input_file_name_entry.pack(side=tk.TOP, fill=tk.X, expand=True, pady=10)
        self.refresh_button.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=15)
        self.confirm_button.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=15)
        self.delete_button.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=15)
        self.execute_button.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=15)
        
        # 레이블 배치
        self.input_path_label.pack(side=tk.TOP, fill=tk.NONE, expand=False, padx=15)
        self.output_path_label.pack(side=tk.TOP, fill=tk.NONE, expand=False, padx=15)
        
        
        if self.path_instance.isNonePath(TARGET_PATH):
            self.label_manager.set_input_path_label()
        else:
            self.label_manager.update_input_path_label()
        
        if self.path_instance.isNonePath(OUTPUT_PATH):
            self.label_manager.set_output_path_label()
        else:
            self.label_manager.update_output_path_label()
            
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
