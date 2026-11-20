import cv2
from pathlib import Path


class VideoLoader:
    """Load a video, expose metadata, and extract sampled frames."""

    def __init__(self, video_path):
        self.video_path = Path(video_path)
        if not self.video_path.is_file():
            raise FileNotFoundError(f"Video file not found: {self.video_path}")

        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            self.cap.release()
            raise ValueError(f"Unable to open video: {self.video_path}")

        self.fps = float(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.total_frames / self.fps if self.fps > 0 else 0.0

    def get_metadata(self):
        return {
            "filename": self.video_path.name,
            "fps": self.fps,
            "total_frames": self.total_frames,
            "width": self.width,
            "height": self.height,
            "duration": self.duration,
        }

    def extract_frames(self, output_dir="data/frames", frame_interval=30, max_frames=None):
        if frame_interval < 1:
            raise ValueError("frame_interval must be >= 1")
        if max_frames is not None and max_frames < 1:
            raise ValueError("max_frames must be >= 1 when provided")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        extracted = 0
        frame_index = 0
        while True:
            success, frame = self.cap.read()
            if not success:
                break

            if frame_index % frame_interval == 0:
                filename = output_path / f"frame_{frame_index:06d}.jpg"
                if not cv2.imwrite(str(filename), frame):
                    raise IOError(f"Could not save frame: {filename}")
                extracted += 1
                if max_frames is not None and extracted >= max_frames:
                    break
            frame_index += 1

        return extracted

    def release(self):
        if getattr(self, "cap", None) is not None:
            self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
