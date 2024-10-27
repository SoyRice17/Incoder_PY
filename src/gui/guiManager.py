import tkinter as tk

class GuiManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("샤나인코더 매크로")
        self.root.geometry("800x600")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 프레임
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #"파일디렉토리를 설정하세요" 텍스트 출력
        self.text_box.insert(tk.END, "파일디렉토리를 설정하세요")
        
        # 텍스트 박스 추가
        self.text_box = tk.Text(main_frame, height=10, width=50)
        self.text_box.pack(pady=10)
        
        # 버튼 추가
        start_button = tk.Button(main_frame, text="시작", command=self.start_macro)
        start_button.pack(pady=10)
        
        # 레이블 추가
        self.status_label = tk.Label(main_frame, text="대기 중...")
        self.status_label.pack(pady=10)
        
    def start_macro(self):
        # 매크로 시작 로직
        self.status_label.config(text="매크로 실행 중...")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GuiManager()
    gui.run()
