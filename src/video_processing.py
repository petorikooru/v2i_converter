from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget

import os
import ffmpeg
import threading

from ui_form import Ui_Form

class VideoProcessing(QThread, QWidget):
    # Update progress bar
    progress_percentage = pyqtSignal(int)

    def __init__ (
        self,
        video_path,
        output_path,
        start_time,
        video_duration,
        frame_leap,
        quality,
        parent=None
    ):
        super().__init__(parent)
        # Redefine things (idk if it is necessary)
        self.video_path     = video_path
        self.output_path    = output_path
        self.start_time     = start_time
        self.video_duration = video_duration
        self.frame_leap     = frame_leap
        self.quality        = quality
        
        # Handle thread elimination
        self.is_running = True

    def fps_calc(self):
        # Probing the video file
        probe = ffmpeg.probe(self.video_path)
        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
            None
        )

        # Find the average fps
        fps = video_stream.get('avg_frame_rate', '0/0')
        try:
            num, den = map(int, avg_frame_rate.split('/'))
            fps = num / den if den != 0 else 0
        except Exception:
            fps = 0
            
        # Fallback to r frame rate
        if fps == 0:
            r_frame_rate = video_stream.get('r_frame_rate', '0/0')
            try:
                num, den = map(int, r_frame_rate.split('/'))
                fps = num / den if den != 0 else 0
            except Exception:
                fps = 0
        
        # If the fps is still not detected
        if fps == 0:
            QMessageBox.warning(
                self, "FFmpeg error!",
                "Invalid FPS detected."
            )
            return 0
        else:
            return fps

    def update_progress(self, process, fps):
        total_frames = int(fps * self.video_duration)

        while True:
            # If the process get terminated
            if not self.is_running:
                QMessageBox.warning(
                    self, "Conversion Error!",
                    "Conversion is terminated"
                )
                return
            
            # Read the progress from FFmpeg
            line = process.stdout.readline().decode('utf-8').strip()
            if not line:
                break

            # Process the information into progress bar
            if line.startswith('frame='):
                try:
                    ith_frame = int(line.split('frame=')[1])
                    progress = int((ith_frame / total_frames) * 100)
                    progress = min(progress, 100)  # Cap at 100%
                    self.progress_percentage.emit(progress)
                except (IndexError, ValueError):
                    continue
            elif line == 'progress=end':
                break

    def run(self):
        try:
            # Output filename
            filename = os.path.join(self.output_path, "frame_%04d.jpg")

            # Calculate FPS for frame leaping
            raw_fps = self.fps_calc()
            if raw_fps == 0:
                return

            # Processed FPS
            fps = raw_fps / self.frame_leap
            if fps <= 0:
                QMessageBox.warning(
                    self, "FFmpeg error!",
                    "Frame leap value is too high."
                )
                return

            # Start the actual actual program
            process = (
                ffmpeg
                .input(self.video_path, ss=self.start_time, t=self.video_duration)
                .filter('fps', fps=fps)
                .output(
                    filename,
                    format='image2',
                    vcodec='mjpeg',
                    qscale=self.quality
                )
                .global_args('-progress', 'pipe:1')  # Share the progresst
                .run_async(pipe_stdout=True, pipe_stderr=True)                
            )
            
            # Update progress bar
            self.update_progress(process, fps)
            process.wait()

            # Check whether the conversion is successfull or not
            if process.returncode == 0:
                self.progress_percentage.emit(100) 
                QMessageBox.information(
                    None, "Conversion Finished!!!",
                    "The video has been successfully converted into images :D"
                )
            else: 
                QMessageBox.critical(
                    None, "Conversion Error!",
                    f"FFmpeg exited with code {process.returncode}"
                )
        
        except ffmpeg.Error as e:
                QMessageBox.critical(
                    None, "Conversion Error!",
                    f"FFmpeg exited with code {e.stderr.decode()}"
                )
        
        except Exception as e:
                QMessageBox.critical(
                    None, "Unexpected Error!",
                    f"FFmpeg exited with code {str(e)}"
                )

