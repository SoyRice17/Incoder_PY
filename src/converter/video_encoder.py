import os
import ffmpeg
import util
import converter.video_grapper as video_grapper
from constants.config_constants import FILE_PATH


class VideoEncoder:
    def __init__(self, gui_instance):
        self.io = util.LogIOManager()
        self.path_instance = util.JsonIOManager()
        self.input_path = self.path_instance.get_path(FILE_PATH,"target_path")
        self.output_path = self.path_instance.get_path(FILE_PATH,"output_path")
        self.video_grapper = video_grapper.VideoGrapper(gui_instance)
        self.video_groups = self.video_grapper.get_video_list()

    
    def encode(self):
        # video_file_list가 dictionary 형태이므로 각 키워드별로 처리
        for keyword, videos in self.video_groups.items():
            if not videos:  # 비디오 목록이 비어있으면 스킵
                continue
                
            try:
                # 각 키워드별로 새로운 input.txt 생성
                with open('input.txt', 'w', encoding='utf-8') as f:
                    for video in videos:
                        # 경로의 특수문자 처리
                        escaped_path = video.replace("'", "'\\''")
                        f.write(f"file '{escaped_path}'\n")
                
                # 출력 파일 경로 설정
                output_file = os.path.join(self.output_path, f"{keyword}_combined.mp4")
                
                # ffmpeg 명령 설정
                stream = ffmpeg.input('input.txt', f='concat', safe=0)
                stream = ffmpeg.output(stream, output_file, c='copy')
                
                # 디버그용 명령어 출력
                self.io.log(f"== 비디오 병합 시작 == \n 키워드 : {keyword}")
                self.io.log(f"FFmpeg command: {' '.join(ffmpeg.compile(stream))}")
                
                # 실행
                ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
                self.io.log(f"== 비디오 병합 완료 == \n 키워드 : {keyword}")
                
            except ffmpeg.Error as e:
                self.io.log(f"== 비디오 병합 에러 == \n 키워드 : {keyword} \n 에러 : {str(e)}")
                # 여기에 에러 처리 로직 추가 가능
                
            except Exception as e:
                self.io.log(f"== 비디오 병합 예외 == \n 키워드 : {keyword} \n 에러 : {str(e)}")
                
            finally:
                # 임시 파일 삭제
                if os.path.exists('input.txt'):
                    os.remove('input.txt')