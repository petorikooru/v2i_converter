# QT things
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ui_form import Ui_MainWindow  # Assuming you have a UI file

# The conversion part (using ffmpeg)
import ffmpeg
import threading
import os
import sys

class VideoProcessing(QThread):
    """
    Worker thread for converting video to images using FFmpeg.
    """
    progress_signal = Signal(int)  # Emitted to update the progress bar
    status_signal = Signal(str)    # Emitted to update the status label

    def __init__(
        self, video_path, output_dir, start_time, end_time,
        frame_skip, quality, parent=None
    ):
        super().__init__(parent)
        self.video_path = video_path
        self.output_dir = output_dir
        self.start_time = start_time  # in seconds
        self.end_time = end_time      # in seconds
        self.frame_skip = frame_skip
        self.quality = quality
        self.is_running = True        # To handle thread termination

    def run(self):
        """
        Executes the FFmpeg command to extract frames from the video.
        """
        try:
            # Ensure output directory exists
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            # Define output pattern (using JPEG format)
            output_pattern = os.path.join(self.output_dir, "frame_%04d.jpg")

            # Get video information using ffmpeg.probe
            probe = ffmpeg.probe(self.video_path)

            # Retrieve duration from the format section
            duration = float(probe['format'].get('duration', 0))

            if duration == 0:
                # Fallback to video stream duration if available
                video_stream = next(
                    (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                    None
                )
                if video_stream and 'duration' in video_stream:
                    duration = float(video_stream['duration'])

            if duration == 0:
                self.status_signal.emit("Unable to retrieve video duration.")
                return

            # Validate the provided time range
            if self.start_time < 0 or self.end_time > duration or self.start_time >= self.end_time:
                self.status_signal.emit("Invalid time range specified.")
                return

            # Calculate the duration for frame extraction
            total_extract_duration = self.end_time - self.start_time

            # Calculate the FPS after frame skipping
            # Retrieve FPS from format if possible, else from video stream
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                None
            )
            if not video_stream:
                self.status_signal.emit("No video stream found.")
                return

            avg_frame_rate = video_stream.get('avg_frame_rate', '0/0')
            try:
                num, den = map(int, avg_frame_rate.split('/'))
                fps = num / den if den != 0 else 0
            except Exception:
                fps = 0

            if fps == 0:
                # Fallback to r_frame_rate
                r_frame_rate = video_stream.get('r_frame_rate', '0/0')
                try:
                    num, den = map(int, r_frame_rate.split('/'))
                    fps = num / den if den != 0 else 0
                except Exception:
                    fps = 0

            if fps == 0:
                self.status_signal.emit("Invalid FPS detected.")
                return

            extracted_fps = fps / self.frame_skip
            if extracted_fps <= 0:
                self.status_signal.emit("Frame skip value is too high.")
                return

            # Quality settings mapping (Lower qscale means higher quality)
            quality_mapping = {
                'Low': 10,
                'Medium': 5,
                'High': 2
            }
            qscale = quality_mapping.get(self.quality, 5)

            # Start FFmpeg process to extract frames with progress
            # Using -progress pipe:1 to get progress info on stdout
            process = (
                ffmpeg
                .input(self.video_path, ss=self.start_time, t=total_extract_duration)
                .filter('fps', fps=extracted_fps)
                .output(
                    output_pattern,
                    format='image2',
                    vcodec='mjpeg',
                    qscale=qscale
                )
                .global_args('-loglevel', 'quiet')  # Suppress unnecessary logs
                .global_args('-progress', 'pipe:1')  # Output progress info to stdout
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )

            # Calculate total frames for progress estimation
            total_extract_frames = int(extracted_fps * total_extract_duration)

            while True:
                if not self.is_running:
                    process.terminate()
                    self.status_signal.emit("Conversion cancelled.")
                    return

                # Read a line from stdout for progress
                line = process.stdout.readline().decode('utf-8').strip()
                if not line:
                    break

                # Parse progress information
                if line.startswith('frame='):
                    try:
                        frame_number = int(line.split('frame=')[1])
                        progress = int((frame_number / total_extract_frames) * 100)
                        progress = min(progress, 100)  # Cap at 100%
                        self.progress_signal.emit(progress)
                    except (IndexError, ValueError):
                        continue

                elif line == 'progress=end':
                    break

            # Wait for FFmpeg to finish processing
            process.wait()

            if process.returncode == 0:
                # Emit completion status
                self.status_signal.emit("Conversion completed successfully.")
                self.progress_signal.emit(100)
            else:
                # Emit error status signal
                self.status_signal.emit("Error during conversion.")
                print(f"FFmpeg exited with code {process.returncode}")

        except ffmpeg.Error as e:
            # Emit error status signal
            self.status_signal.emit("Error during conversion.")
            print(f"FFmpeg error: {e.stderr.decode()}")

        except Exception as e:
            # Catch any other exceptions
            self.status_signal.emit("Error during conversion.")
            print(f"Unexpected error: {str(e)}")

class MainWindow(QMainWindow):
    """
    Main application window.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize variables
        self.video_path = None
        self.output_dir = None
        self.frame_skip = 10
        self.quality = 'Medium'  # Default quality
        self.video_duration = 0  # Store video duration in seconds

        # Connect buttons to methods
        self.ui.vid_button.clicked.connect(self.select_video_path)
        self.ui.out_button.clicked.connect(self.select_out_dir)
        self.ui.convert_button.clicked.connect(self.convert_to_image)

        # Initialize spin boxes for start and end times
        for box in [self.ui.start_box, self.ui.end_box]:
            box.setDisplayFormat("hh:mm:ss")          # Display format as HH:MM:SS
            box.setTime(QTime(0, 0, 0))               # Initialize to 00:00:00
            box.setMinimumTime(QTime(0, 0, 0))        # Minimum time
            box.setMaximumTime(QTime(9999, 59, 59))   # Temporary maximum; will update after video selection
            box.setAlignment(Qt.AlignRight)

        self.ui.frame_box.setRange(1, 1000)
        self.ui.frame_box.setValue(10)  # Default to process every 10th frame

        # Setup radio buttons for quality
        self.quality_group = QButtonGroup(self)
        self.quality_group.addButton(self.ui.low_quality_box, 1)      # Low
        self.quality_group.addButton(self.ui.medium_quality_box, 2)   # Medium
        self.quality_group.addButton(self.ui.high_quality_box, 3)     # High
        self.quality_group.setExclusive(True)
        self.quality_group.button(2).setChecked(True)  # Default to Medium

        # Connect valueChanged signals for validation
        self.ui.start_box.timeChanged.connect(self.validate_start_time)
        self.ui.end_box.timeChanged.connect(self.validate_end_time)

        # Connect frame_box
        self.ui.frame_box.valueChanged.connect(self.update_frame_skip)

        # Disable the convert button initially
        self.ui.convert_button.setEnabled(False)

    def validate_start_time(self, qtime):
        """
        Ensure that the start_time <= end_time.
        """
        start_time = self.get_time_in_seconds(self.ui.start_box)
        end_time = self.get_time_in_seconds(self.ui.end_box)
        if start_time > end_time:
            # Adjust end_time to match start_time or reset start_time
            QMessageBox.warning(
                self, "Invalid Time Range",
                "Start time cannot exceed end time."
            )
            # Optionally, reset start_time to end_time
            self.ui.start_box.setTime(self.ui.end_box.time())

    def validate_end_time(self, qtime):
        """
        Ensure that the end_time >= start_time and does not exceed video duration.
        """
        end_time = self.get_time_in_seconds(self.ui.end_box)
        start_time = self.get_time_in_seconds(self.ui.start_box)
        if end_time < start_time:
            QMessageBox.warning(
                self, "Invalid Time Range",
                "End time cannot be less than start time."
            )
            # Optionally, reset end_time to start_time
            self.ui.end_box.setTime(self.ui.start_box.time())
        elif end_time > self.video_duration:
            QMessageBox.warning(
                self, "Invalid Time Range",
                "End time cannot exceed video duration."
            )
            # Reset end_time to video duration
            total_seconds = self.video_duration
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            qtime = QTime(hours, minutes, seconds)
            self.ui.end_box.setTime(qtime)

    def get_time_in_seconds(self, time_edit):
        """
        Converts a QTime object to total seconds.
        """
        qtime = time_edit.time()
        total_seconds = qtime.hour() * 3600 + qtime.minute() * 60 + qtime.second()
        return total_seconds

    def update_frame_skip(self, value):
        """
        Update the frame skip value.
        """
        self.frame_skip = value

    def select_video_path(self):
        """
        Select the video file and set end_box to video duration.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a Video File",
            "", "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*)"
        )
        if file_path:
            self.video_path = file_path
            self.ui.vid_dir.setText(file_path)
            self.enable_convert_button()

            # Retrieve video duration
            try:
                probe = ffmpeg.probe(self.video_path)

                # Retrieve duration from the format section
                duration = float(probe['format'].get('duration', 0))

                # Initialize video_stream to None
                video_stream = None

                if duration == 0:
                    # Fallback to video stream duration if available
                    video_stream = next(
                        (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                        None
                    )
                    if video_stream and 'duration' in video_stream:
                        duration = float(video_stream['duration'])

                if duration == 0:
                    QMessageBox.critical(self, "Error", "Unable to retrieve video duration.")
                    self.ui.end_box.setTime(QTime(0, 0, 0))
                    self.ui.end_box.setMaximumTime(QTime(9999, 59, 59))  # Reset to default maximum
                    return

                # Store video duration
                self.video_duration = int(round(duration))

                # Convert duration to QTime
                total_seconds = self.video_duration
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60

                # Cap hours to the QTime maximum (23 hours, 59 minutes, 59 seconds)
                if hours > 23:
                    hours = 23
                    minutes = 59
                    seconds = 59

                # Create QTime object
                qtime = QTime(hours, minutes, seconds)

                # Set end_box's value and maximum time
                self.ui.end_box.setTime(qtime)
                self.ui.end_box.setMaximumTime(qtime)

                # Set start_box's maximum time to end_box's value
                self.ui.start_box.setMaximumTime(qtime)

                # If start_box's current value exceeds end_box, adjust it
                if self.get_time_in_seconds(self.ui.start_box) > self.video_duration:
                    self.ui.start_box.setTime(qtime)

                # Update status label
                total_minutes = self.video_duration // 60
                remaining_seconds = self.video_duration % 60
                self.ui.status_label.setText(f"Video Duration: {total_minutes}m {remaining_seconds}s")

            except ffmpeg.Error as e:
                QMessageBox.critical(
                    self, "FFmpeg Error",
                    f"An error occurred while probing the video:\n{e.stderr.decode()}"
                )
                self.ui.end_box.setTime(QTime(0, 0, 0))
                self.ui.end_box.setMaximumTime(QTime(9999, 59, 59))  # Reset to default maximum
            except Exception as e:
                QMessageBox.critical(
                    self, "Error",
                    f"An unexpected error occurred:\n{str(e)}"
                )
                self.ui.end_box.setTime(QTime(0, 0, 0))
                self.ui.end_box.setMaximumTime(QTime(9999, 59, 59))  # Reset to default maximum
        else:
            self.ui.vid_dir.setText("No video file selected.")

    def select_out_dir(self):
        """
        Select the output directory.
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.ui.out_dir.setText(dir_path)
            self.enable_convert_button()
        else:
            self.ui.out_dir.setText("No output directory selected.")

    def enable_convert_button(self):
        """
        Enable the convert button if both file and directory are selected.
        """
        if self.video_path and self.output_dir:
            self.ui.convert_button.setEnabled(True)
        else:
            self.ui.convert_button.setEnabled(False)

    def convert_to_image(self):
        """
        Start the video-to-image conversion process.
        """
        # Retrieve start and end times from QTimeEdit
        start_time = self.get_time_in_seconds(self.ui.start_box)
        end_time = self.get_time_in_seconds(self.ui.end_box)

        # Validate time inputs
        if start_time >= end_time:
            QMessageBox.warning(
                self, "Invalid Time Range",
                "Start time must be less than end time."
            )
            return

        # Get quality from radio buttons
        selected_id = self.quality_group.checkedId()
        quality_mapping = {
            1: 'Low',
            2: 'Medium',
            3: 'High'
        }
        quality = quality_mapping.get(selected_id, 'Medium')

        # Update the status label to inform the user about the processing
        self.ui.status_label.setText(
            f"Processing video..."
        )
        self.ui.loading_bar.setValue(0)  # Reset the progress bar

        # Disable the convert button and input fields during processing
        self.ui.convert_button.setEnabled(False)
        self.ui.vid_button.setEnabled(False)
        self.ui.out_button.setEnabled(False)
        self.ui.low_quality_box.setEnabled(False)
        self.ui.medium_quality_box.setEnabled(False)
        self.ui.high_quality_box.setEnabled(False)
        self.ui.start_box.setEnabled(False)
        self.ui.end_box.setEnabled(False)
        self.ui.frame_box.setEnabled(False)

        # Start the background processing in a separate thread
        self.worker = VideoProcessing(
            video_path=self.video_path,
            output_dir=self.output_dir,
            start_time=start_time,
            end_time=end_time,
            frame_skip=self.frame_skip,
            quality=quality
        )
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.status_signal.connect(self.update_status)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.start()

    def update_progress(self, progress):
        """
        Update the progress bar based on the conversion progress.
        """
        self.ui.loading_bar.setValue(progress)

    def update_status(self, status):
        """
        Update the status label with the current status.
        """
        self.ui.status_label.setText(status)

    def on_conversion_finished(self):
        """
        Re-enable the UI elements after conversion is done.
        """
        self.ui.convert_button.setEnabled(True)
        self.ui.vid_button.setEnabled(True)
        self.ui.out_button.setEnabled(True)
        self.ui.low_quality_box.setEnabled(True)
        self.ui.medium_quality_box.setEnabled(True)
        self.ui.high_quality_box.setEnabled(True)
        self.ui.start_box.setEnabled(True)
        self.ui.end_box.setEnabled(True)
        self.ui.frame_box.setEnabled(True)

        # Inform the user about the completion
        QMessageBox.information(
            self, "Conversion Finished",
            "The video has been successfully converted to images."
        )

    def closeEvent(self, event):
        """
        Handle the window close event to ensure the worker thread is terminated.
        """
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()
