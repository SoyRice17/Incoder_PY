import os
import ffmpeg
import util
import converter.video_grapper as video_grapper
from constants.config_constants import FILE_PATH
import time


class VideoEncoder:
    def __init__(self, gui_instance):
        self.io = util.LogIOManager()
        self.path_instance = util.JsonIOManager()
        self.input_path = self.path_instance.get_path(FILE_PATH,"target_path")
        self.output_path = self.path_instance.get_path(FILE_PATH,"output_path")
        self.video_grapper = video_grapper.VideoGrapper(gui_instance)
        self.video_groups = self.video_grapper.get_video_list()
        self.gui_instance = gui_instance
    
    def encode(self):
        total_videos = sum(len(videos) for videos in self.video_groups.items())
        processed_videos = 0
        
        self.gui_instance.show_encoding_progress()
        
        try:
            for keyword, videos in self.video_groups.items():
                if not videos:
                    continue
                    
                try:
                    with open('input.txt', 'w', encoding='utf-8') as f:
                        for video in videos:
                            escaped_path = video.replace("'", "'\\''")
                            f.write(f"file '{escaped_path}'\n")
                    
                    output_file = os.path.join(self.output_path, f"{keyword}_combined.mp4")
                    
                    # ffmpeg 명령 설정
                    stream = ffmpeg.input('input.txt', f='concat', safe=0)
                    stream = ffmpeg.output(stream, output_file, c='copy')
                    
                    self.io.log(f"== 비디오 병합 시작 == \n 키워드 : {keyword}")
                    
                    # ffmpeg 실행 시 progress 콜백 추가
                    process = ffmpeg.run_async(stream, 
                        pipe_stdout=True, 
                        pipe_stderr=True
                    )
                    
                    # 진행 상황 모니터링
                    while process.poll() is None:
                        # 현재 키워드 그룹의 진행률 계산
                        current_progress = (processed_videos / total_videos) * 100
                        self.gui_instance.update_encoding_progress(
                            current_progress,
                            f"인코딩 중: {keyword} ({processed_videos + 1}/{total_videos})"
                        )
                        time.sleep(0.1)  # CPU 부하 방지
                    
                    process.wait()
                    
                    processed_videos += len(videos)
                    self.io.log(f"== 비디오 병합 완료 == \n 키워드 : {keyword}")
                    
                except ffmpeg.Error as e:
                    self.io.log(f"== 비디오 병합 에러 == \n 키워드 : {keyword} \n 에러 : {str(e)}")
                    
                except Exception as e:
                    self.io.log(f"== 비디오 병합 예외 == \n 키워드 : {keyword} \n 에러 : {str(e)}")
                    
        finally:
            self.gui_instance.close_encoding_progress()