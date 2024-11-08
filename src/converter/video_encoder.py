import ffmpeg
import util.init_path as path
import converter.video_grapper as video_grapper


class VideoEncoder:
    def __init__(self,gui_instance):
        self.path_instance = path.InitPath()
        self.input_path = self.path_instance.get_path("target_path")
        self.output_path = self.path_instance.get_path("output_path")
        self.video_grapper_instance = video_grapper.VideoGrapper(gui_instance)
        self.video_file_list = self.video_grapper_instance.get_video_list()
    
    def encode(self):
        with open('input.txt', 'w') as f:
            for video in self.video_file_list:
                f.write(f"file '{video}'\n")
    
        # 영상 합치기
        stream = ffmpeg.input('input.txt', f='concat', safe=0)
        stream = ffmpeg.output(stream, self.output_path, c='copy')
        ffmpeg.run(stream)