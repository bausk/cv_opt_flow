import cv2
import math
import os


class MP4VideoSlicer:
    def __init__(self, video_path, autoincrement=True, increment=None) -> None:
        capture_source = cv2.VideoCapture(video_path)
        self.video_fps: float = capture_source.get(cv2.CAP_PROP_FPS)
        self.total_frames: int = int(capture_source.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_width_px = int(capture_source.get(3))
        self.video_height_px = int(capture_source.get(4))
        self.capture_source = capture_source
        self.next_step_seconds = 0.0
        self.frame_count = 0
        self.autoincrement = autoincrement
        self.increment = increment

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.autoincrement:
            if self.increment is None:
                next_frame_count = self.frame_count + 1
            else:
                next_frame_count = self.frame_count + math.ceil(self.increment * self.video_fps)
        else:
            next_frame_count = self.frame_count + math.ceil(self.next_step_seconds * self.video_fps)

        if next_frame_count >= self.total_frames:
            self.cleanup()
            raise StopIteration

        if self.autoincrement and self.increment is None:
            # Reading frame one by one does not require setting CAP_PROP_POS_FRAMES
            ret, frame = self.capture_source.read()
        else:
            self.capture_source.set(cv2.CAP_PROP_POS_FRAMES, next_frame_count)
            ret, frame = self.capture_source.read()

        self.frame_count = next_frame_count
        return ret, frame
    
    def cleanup(self):
        self.capture_source.release()


class MP4VideoPreprocessor(MP4VideoSlicer):
    def process(self):
        print(self.video_width_px, self.video_fps, self.video_height_px)
        self.video_out = cv2.VideoWriter(
            'output.mp4',
            cv2.VideoWriter.fourcc(*'mp4v'),
            self.video_fps,
            (self.video_width_px, self.video_height_px)
        )

        path = f'outputs'
        folder = f'{self.video_width_px}x{self.video_height_px}'
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        os.chdir(path)
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        os.chdir(folder)        

        for ret, frame in self:
            if ret:
                self.video_out.write(frame)
                current_frame_time_seconds = self.frame_count / self.video_fps
                hours = int(current_frame_time_seconds // 3600)
                minutes = int((current_frame_time_seconds % 3600) // 60)
                seconds = int(current_frame_time_seconds % 60)
                milliseconds = int((current_frame_time_seconds - int(current_frame_time_seconds)) * 1000)
                filename = f'output_{self.video_width_px}x{self.video_height_px}_{hours:02d}_{minutes:02d}_{seconds:02d}_{milliseconds:03d}.jpg'
                cv2.imwrite(filename, frame)
        self.video_out.release()
