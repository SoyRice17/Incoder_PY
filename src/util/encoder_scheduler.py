import time
import threading
from datetime import datetime
from converter import VideoEncoder
from util import LogIOManager, ConfigManager

class EncoderScheduler:
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.io = LogIOManager()
        self.config_manager = ConfigManager()
        self.is_running = False
        self.scheduler_thread = None
        
    def start_scheduler(self, interval_minutes: int):
        """스케줄러 시작"""
        if self.is_running:
            self.io.log("스케줄러가 이미 실행 중입니다.")
            return
            
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, args=(interval_minutes,))
        self.scheduler_thread.daemon = True  # 메인 프로그램 종료시 같이 종료
        self.scheduler_thread.start()
        self.io.log(f"스케줄러가 시작되었습니다. 간격: {interval_minutes}분")
        
    def stop_scheduler(self):
        """스케줄러 중지"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        self.io.log("스케줄러가 중지되었습니다.")
        
    def _scheduler_loop(self, interval_minutes: int):
        """스케줄러 메인 루프"""
        while self.is_running:
            try:
                self.io.log(f"\n=== 예약 인코딩 시작 (시간: {datetime.now()}) ===")
                encoder = VideoEncoder(self.gui_instance)
                encoder.encode()
                self.io.log(f"다음 인코딩까지 {interval_minutes}분 대기...")
                
                # interval_minutes 동안 대기 (1초 단위로 체크하며 중단 가능)
                for _ in range(interval_minutes * 60):
                    if not self.is_running:
                        return
                    time.sleep(1)
                    
            except Exception as e:
                self.io.log(f"스케줄러 실행 중 오류 발생: {e}")
                time.sleep(60)  # 오류 발생시 1분 대기