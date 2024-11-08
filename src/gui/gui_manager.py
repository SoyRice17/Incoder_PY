# 표준 라이브러리
import tkinter as tk

# 로컬 모듈
import util.init_path as path_manager
from gui.button_manager import ButtonManager
from gui.listbox_manager import ListboxManager
from gui.label_manager import LabelManager
from converter.video_encoder import VideoEncoder
from constants.config_constants import OUTPUT_PATH,TARGET_PATH
from constants.gui_constants import WINDOW_TITLE, WINDOW_SIZE

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
            
        self.show_main_screen() # 값이 존재하면 메인 스크린 출력
    
    def show_loading_screen(self): # 메인화면에 많은 데이터가 가중될때 화면 출력이 지연되는 것을 방지해 로딩화면 출력
        # 현재 프레임 내용 제거
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        loading_label = tk.Label(self.main_frame, text="화면을 불러오는 중...", font=('Helvetica', 12))
        loading_label.pack(expand=True)
        self.loading_screen_active = True
        self.root.update()  # GUI 즉시 업데이트
    
    def create_frames(self):
        self.top_frame = tk.Frame(self.main_frame)
        self.bottom_frame = tk.Frame(self.main_frame)
        self.top_left_frame = tk.LabelFrame(
            self.top_frame,
            text="파일 목록",
            font=('Helvetica', 10),
            relief=tk.RAISED
        )
        self.top_right_frame = tk.LabelFrame(
            self.top_frame,
            text="선택 파일 목록",
            font=('Helvetica', 10),
            relief=tk.RAISED
        )
        self.bottom_top_frame = tk.Frame(
            self.bottom_frame,
            relief=tk.RAISED,
            borderwidth=1
        )
        self.button_frame = tk.Frame(
            self.bottom_frame,
            height=100,
            relief=tk.RAISED,
            borderwidth=1
        )
    
    def create_widgets(self):
        #스크롤바 생성
        self.selected_file_name_scrollbar = tk.Scrollbar(self.top_right_frame)
        self.file_listbox_scrollbar = tk.Scrollbar(self.top_left_frame)
        
        # 리스트박스 추가
        self.selected_file_name_listbox = tk.Listbox(
            self.top_right_frame,
            font=('Helvetica', 10),
            yscrollcommand=self.selected_file_name_scrollbar.set
        )
        self.selected_file_name_listbox.bind('<Double-Button-1>', self.listbox_manager.delete_selected_file_name)
        self.file_listbox = tk.Listbox(
            self.top_left_frame,
            font=('Helvetica', 10),
            yscrollcommand=self.file_listbox_scrollbar.set
        )
        self.file_listbox.bind('<Double-Button-1>', self.listbox_manager.insert_input_file_name_entry)
        
        # 스크롤바 설정
        self.file_listbox_scrollbar.config(command=self.file_listbox.yview)
        self.selected_file_name_scrollbar.config(command=self.selected_file_name_listbox.yview)
        
        # 버튼 추가
        self.refresh_button = tk.Button(
            self.button_frame, 
            text="새로고침",
            command=self.button_manager.refresh_file_list
        )
        self.confirm_button = tk.Button(
            self.button_frame, 
            text="확인",
            command=self.button_manager.confirm_selection
        )
        self.delete_button = tk.Button(
            self.button_frame, 
            text="삭제",
            command=self.button_manager.delete_selected_file_listbox
        )
        self.execute_button = tk.Button(
            self.button_frame, 
            text="실행"
        )
        # 레이블 추가
        self.input_path_label = tk.Label(
            self.bottom_top_frame,
            text="파일 경로",
            font=('Helvetica', 10),
            anchor=tk.W
        )
        self.output_path_label = tk.Label(
            self.bottom_top_frame,
            text="출력 경로",
            font=('Helvetica', 10),
            anchor=tk.W
        )
        # 입력 필드 추가
        self.input_file_name_entry = tk.Entry(
            self.bottom_top_frame,
            font=('Helvetica', 10),
            
        )
    
    def place_frames(self):
        # 프레임 배치
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.top_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.top_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.bottom_top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        self.button_frame.pack_propagate(False)
    
    def place_widgets(self):
        # 리스트박스 배치
        self.selected_file_name_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        #스크롤바 배치
        self.selected_file_name_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 레이블 배치
        self.input_path_label.pack(side=tk.TOP, fill=tk.X, expand=False, padx=15)
        self.output_path_label.pack(side=tk.TOP, fill=tk.X, expand=False, padx=15)
        
        # 입력 필드와 버튼 배치
        self.input_file_name_entry.pack(side=tk.TOP, fill=tk.X, expand=True, pady=10)
        self.refresh_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
        self.confirm_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
        self.execute_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
    
    def show_main_screen(self):
        self.create_frames()
        self.create_widgets()
        self.place_frames()
        self.place_widgets()
        
        # 경로 설정
        if self.path_instance.isNonePath(TARGET_PATH):
            self.label_manager.set_input_path_label()
        else:
            self.label_manager.update_input_path_label()
        
        if self.path_instance.isNonePath(OUTPUT_PATH):
            self.label_manager.set_output_path_label()
        else:
            self.label_manager.update_output_path_label()
        
        # 파일 목록 새로고침
        self.button_manager.refresh_file_list()
        
        # execute_button에 직접 메서드 연결
        self.execute_button.config(command=self.execute_video_encoding)

    def execute_video_encoding(self):
        # 실행 버튼을 누를 때마다 새로운 VideoEncoder 인스턴스 생성
        video_encoder = VideoEncoder(self)
        video_encoder.encode()
    
    def run(self):
        self.root.mainloop() #mainloop: 윈도우 이벤트 루프를 시작하는 메서드

if __name__ == "__main__":
    gui = GuiManager()
    gui.run()
