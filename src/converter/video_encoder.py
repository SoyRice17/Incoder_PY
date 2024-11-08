import os
import ffmpeg
import util.init_path as path
import converter.video_grapper as video_grapper


class VideoEncoder:
    def __init__(self, gui_instance):
        self.path_instance = path.InitPath()
        self.input_path = self.path_instance.get_path("target_path")
        self.output_path = self.path_instance.get_path("output_path")
        self.video_grapper_instance = video_grapper.VideoGrapper(gui_instance)
        self.video_file_list = self.video_grapper_instance.get_video_list()
    
    def encode(self):
        # video_file_list가 dictionary 형태이므로 각 키워드별로 처리
        for keyword, videos in self.video_file_list.items():
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
                print(f"Processing {keyword} videos...")
                print(f"FFmpeg command: {' '.join(ffmpeg.compile(stream))}")
                
                # 실행
                ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
                print(f"Successfully combined videos for keyword: {keyword}")
                
            except ffmpeg.Error as e:
                print(f"FFmpeg error occurred for {keyword}: {str(e)}")
                # 여기에 에러 처리 로직 추가 가능
                
            except Exception as e:
                print(f"Unexpected error occurred for {keyword}: {str(e)}")
                
            finally:
                # 임시 파일 삭제
                if os.path.exists('input.txt'):
                    os.remove('input.txt')