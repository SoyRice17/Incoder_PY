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
        self.config = util.ConfigManager().config  # 설정 가져오기
        self.encoding_settings = self.config["setting"]  # 인코딩 설정 가져오기
    
    def encode(self):
        total_videos = sum(len(videos) for videos in self.video_groups.items())
        processed_videos = 0
        
        self.gui_instance.show_encoding_progress()
        
        try:
            for keyword, videos in self.video_groups.items():
                if not videos:
                    continue
                    
                try:
                    # 입력 파일 목록 작성 시 로그 추가
                    self.io.log(f"== 비디오 목록 작성 시작 == \n 키워드: {keyword}")
                    with open('input.txt', 'w', encoding='utf-8') as f:
                        for video in videos:
                            escaped_path = video.replace("'", "'\\''")
                            f.write(f"file '{escaped_path}'\n")
                            self.io.log(f"추가된 비디오: {escaped_path}")
                    
                    output_file = os.path.join(self.output_path, f"{keyword}_combined.mp4")
                    self.io.log(f"출력 파일 경로: {output_file}")
                    
                    # ffmpeg 명령 설정
                    stream = ffmpeg.input('input.txt', f='concat', safe=0)
                    stream = ffmpeg.output(stream, output_file,
                        vcodec='libx264',
                        r=self.encoding_settings['frame_rate'],
                        s=self.encoding_settings['resolution'],
                        crf=self.encoding_settings['crf']
                    )
                    
                    # ffmpeg 명령 로깅
                    ffmpeg_cmd = ' '.join(ffmpeg.get_args(stream))
                    self.io.log(f"== FFmpeg 명령어 ==\n{ffmpeg_cmd}")
                    
                    self.io.log(f"== 비디오 인코딩 시작 == \n 키워드: {keyword}")
                    self.io.log(f"설정값: {self.encoding_settings}")
                    
                    # ffmpeg 실행 시 stderr 캡처
                    process = ffmpeg.run_async(stream, 
                        pipe_stdout=True, 
                        pipe_stderr=True,
                        overwrite_output=True
                    )
                    
                    # 진행 상황 모니터링
                    while process.poll() is None:
                        if process.stderr:
                            line = process.stderr.readline()
                            if line:
                                self.io.log(f"FFmpeg 출력: {line.decode().strip()}")
                                
                        current_progress = (processed_videos / total_videos) * 100
                        self.gui_instance.update_encoding_progress(
                            current_progress,
                            f"인코딩 중: {keyword} ({processed_videos + 1}/{total_videos})"
                        )
                        time.sleep(0.1)
                    
                    # 프로세스 완료 대기 및 출력 수집
                    stdout, stderr = process.communicate()
                    
                    # 성공 여부 확인 및 에러 처리
                    if process.returncode == 0:
                        processed_videos += len(videos)
                        self.io.log(f"== 비디오 인코딩 완료 == \n 키워드: {keyword}")
                    else:
                        error_message = stderr.decode() if stderr else "알 수 없는 에러"
                        self.io.log(f"== FFmpeg 실행 실패 ==\n{error_message}")
                        raise ffmpeg.Error(stdout, stderr)  # communicate()에서 받은 stderr 사용
                    
                except ffmpeg.Error as e:
                    self.io.log(f"== FFmpeg 에러 == \n 키워드: {keyword}")
                    error_message = e.stderr.decode() if e.stderr else str(e)
                    self.io.log(f"FFmpeg 에러 메시지: {error_message}")
                    
                except Exception as e:
                    self.io.log(f"== 예외 발생 == \n 키워드: {keyword} \n 에러: {str(e)}")
                    
        finally:
            if os.path.exists('input.txt'):
                os.remove('input.txt')  # 임시 파일 정리
            self.gui_instance.close_encoding_progress()