# 표준 라이브러리
import tkinter as tk
from tkinter import ttk
# 로컬 모듈
import util
from gui.button_manager import ButtonManager
from gui.listbox_manager import ListboxManager
from gui.label_manager import LabelManager
from converter import VideoEncoder,VideoGrapper
from constants.config_constants import OUTPUT_PATH,TARGET_PATH
from constants.gui_constants import WINDOW_TITLE, WINDOW_SIZE


class GuiManager:
    """GUI 애플리케이션의 메인 매니저 클래스
    
    이 클래스는 애플리케이션의 전체 GUI를 관리하며, 화면 전환과 위젯 관리를 담당합니다.
    Tkinter의 이벤트 루프 특성에 따라, 화면 갱신은 현재 실행 중인 메서드가 완전히 종료된 후 발생합니다.
    
    Attributes:
        root (tk.Tk): 메인 윈도우 객체
        main_frame (tk.Frame): 모든 화면이 표시되는 기본 프레임
        json_io_manager (JsonIOManager): JSON 파일 입출력 관리자
        io (LogIOManager): 로깅 관리자
        button_manager (ButtonManager): 버튼 이벤트 관리자
        listbox_manager (ListboxManager): 리스트박스 이벤트 관리자
        label_manager (LabelManager): 레이블 관리자
    """
    
    def __init__(self):
        """GuiManager 초기화
        
        모든 필요한 매니저 객체들을 생성하고 기본 GUI 설정을 수행합니다.
        """
        # JsonIOManager 먼저 초기화
        self.path_instance = util.JsonIOManager()
        self.io = util.LogIOManager()
        
        # GUI 기본 설정
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # 매니저 객체들 초기화
        self.button_manager = ButtonManager(self)
        self.video_grapper = VideoGrapper(self)
        # 나머지 매니저 초기화
        self.listbox_manager = ListboxManager(self)
        self.label_manager = LabelManager(self)
        
        # 메인 프레임 생성
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 초기 화면 설정
        self.show_appropriate_screen()
        
        self.loading_screen_active = False
    
    def show_appropriate_screen(self):
        """화면 전환을 관리하는 메서드
        
        로딩 화면을 표시한 후, 메인 화면 초기화를 시작합니다.
        로딩 화면은 root.update()를 통해 즉시 표시되며,
        initialize_main_screen에서 모든 초기화가 완료된 후 메인 화면으로 전환됩니다.
        """
        # 로딩 화면 표시
        self.show_loading_screen()
            
        self.initialize_main_screen()
    
    def show_loading_screen(self):
        """로딩 화면을 표시
        
        현재 화면을 지우고 로딩 메시지와 진행바를 표시합니다.
        root.update()를 통해 화면을 즉시 갱신하여 로딩 화면이 보이도록 합니다.
        이 화면은 메인 화면의 모든 초기화가 완료될 때까지 유지됩니다.
        """
        # 현재 프레임 내용 제거
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        self.loading_label = tk.Label(self.main_frame, text="화면을 불러오는 중...", font=('Helvetica', 12))
        self.loading_label.pack(expand=True)
        
        self.progress = ttk.Progressbar(self.main_frame, length=200, mode='determinate')
        self.progress.pack(expand=True)
    
        self.loading_screen_active = True
    
    def update_loading_progress(self, value, text):
        self.progress['value'] = value
        self.loading_label['text'] = text
        self.root.update()
    
    def create_frames(self):
        """GUI의 기본 프레임 구조를 생성
        
        프레임 객체들을 메모리에 생성합니다.
        생성되는 프레임:
        - top_frame: 파일 목록 영역
        - bottom_frame: 로그 및 버튼 영역
        - top_left_frame: 파일 목록
        - top_right_frame: 선택된 파일 목록
        """
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
        """GUI에 필요한 모든 위젯을 생성
        
        생성되는 위젯들:
        - 리스트박스 (파일 목록, 선택된 파일 목록)
        - 스크롤바
        - 버튼들 (새로고침, 확인, 삭제, 실행)
        - 레이블 (경로 표시)
        - 텍스트 영역 (로그 출력)
        """
        #로그 출력 Text 위젯 추가
        self.log_text = tk.Text(
            self.bottom_top_frame, 
            height=10, 
            state='disabled',
            font=('Helvetica', 10)
        )
        # io 초기화
        self.io.initialize_gui(self.log_text, self.root)
        self.io.switch_to_gui()
        
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
        """생성된 프레임들을 화면에 배치
        
        pack() 메서드로 프레임들의 위치와 크기를 설정합니다.
        """
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
        """생성된 위젯들을 각 프레임에 배치
        
        pack() 메서드를 사용하여 위젯들의 위치와 크기를 설정합니다.
        """
        # 로그 출력 Text 위젯 배치
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
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
    
    def initialize_main_screen(self):
        """메인 화면 초기화를 수행
        
        GUI 구성 요소들을 생성하고 필요한 데이터를 로드합니다.
        진행 상황을 로딩 화면에 표시하며, 모든 초기화가 완료되면
        show_main_screen을 호출하여 실제 화면 전환을 수행합니다.
        
        진행 순서:
        1. 프레임 생성 (20%)
        2. 위젯 생성 (40%)
        3. 경로 설정 (60%)
        4. 파일 목록 로드 (80%)
        5. 초기화 완료 (100%)
        """
        try:
            self.update_loading_progress(20, "프레임 생성 중...")
            self.create_frames()
            self.update_loading_progress(40, "위젯 생성 중...")
            self.create_widgets()
            
            self.update_loading_progress(60, "경로 설정 중...")
            # 경로 설정
            if self.path_instance.isNonePath(TARGET_PATH):
                self.label_manager.set_input_path_label()
            else:
                self.label_manager.update_input_path_label()
            
            if self.path_instance.isNonePath(OUTPUT_PATH):
                self.label_manager.set_output_path_label()
            else:
                self.label_manager.update_output_path_label()
                
            self.update_loading_progress(80, "파일 목록 로드 중...")
            # 파일 목록 새로고침
            self.button_manager.refresh_file_list()
            
            self.update_loading_progress(100, "초기화 완료")
            # execute_button에 직접 메서드 연결
            self.execute_button.config(command=self.execute_video_encoding)
            self.root.after(500, self.show_main_screen)
            
        except Exception as e:
            self.io.log(f"초기화 오류: {e}")
            tk.messagebox.showerror("초기화 오류", f"초기화 중 오류가 발생했습니다: {e}")
    
    def show_main_screen(self):
        """메인 화면을 표시
        
        initialize_main_screen에서 생성된 GUI 구성 요소들을 화면에 배치합니다.
        이 메서드는 모든 초기화가 완료된 후 호출되며,
        로딩 화면의 위젯들을 제거하고 메인 화면의 위젯들을 배치합니다.
        
        Note: 이 메서드는 initialize_main_screen에서 root.after()를 통해 호출됩니다.
        """
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
        if hasattr(self, 'progress'):
            self.progress.destroy()
        self.place_frames()
        self.place_widgets()
        self.button_manager.add_video_list(self.video_grapper.get_video_list())
    
    def show_encoding_progress(self):
        """인코딩 진행 상황을 표시하는 창을 생성"""
        self.encoding_window = tk.Toplevel(self.root)
        self.encoding_window.title("인코딩 진행 중...")
        self.encoding_window.geometry("300x150")
        
        self.encoding_label = tk.Label(self.encoding_window, text="인코딩 진행 중...", font=('Helvetica', 10))
        self.encoding_label.pack(pady=10)
        
        self.encoding_progress = ttk.Progressbar(self.encoding_window, length=200, mode='determinate')
        self.encoding_progress.pack(pady=10)

    def update_encoding_progress(self, value, text):
        """인코딩 진행 상황 업데이트"""
        if hasattr(self, 'encoding_progress'):
            self.encoding_progress['value'] = value
            self.encoding_label['text'] = text
            self.encoding_window.update()

    def close_encoding_progress(self):
        """인코딩 진행 창 닫기"""
        if hasattr(self, 'encoding_window'):
            self.encoding_window.destroy()
    
    def execute_video_encoding(self):
        """비디오 인코딩 실행
        
        선택된 파일들에 대해 VideoEncoder를 생성하고 인코딩을 시작합니다.
        """
        # 실행 버튼을 누를 때마다 새로운 VideoEncoder 인스턴스 생성
        video_encoder = VideoEncoder(self)
        video_encoder.encode()
    
    def run(self):
        """GUI 애플리케이션 실행
        
        Tkinter의 메인 이벤트 루프를 시작합니다.
        이벤트 루프는 사용자 입력을 처리하고 화면을 갱신하는
        무한 루프로 동작합니다.
        """
        self.root.mainloop() #mainloop: 윈도우 이벤트 루프를 시작하는 메서드

if __name__ == "__main__":
    gui = GuiManager()
    gui.run()
