from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import os, sys
import ffmpeg

from ui_form import Ui_Form
from video_processing import VideoProcessing

class MainController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Default Settings
        self.video_path     = None
        self.output_path    = None
        self.frame_leap     = 10
        self.quality        = 2 # Medium
        self.video_duration = 0
        self.ui.progress_bar.setValue(0)

        # Connect the buttons into variables and functions
        self.ui.input_button.clicked.connect(self.select_video_path)
        self.ui.output_button.clicked.connect(self.select_dir_path)
        self.ui.leap_box.valueChanged.connect(self.select_frame_leap)
        self.ui.convert_button.clicked.connect(self.convert)
        self.ui.convert_button.setEnabled(False) # Disable the button if user hasn't select the video yet

        # Quality settings radio button
        self.quality_settings = QButtonGroup(self)
        self.quality_settings.setExclusive(True)
        quality_buttons = [
            (self.ui.quality_low,   1),
            (self.ui.quality_medium,2),
            (self.ui.quality_high,  3),
        ]
        # Create the buttons
        for button, id in quality_buttons:
            self.quality_settings.addButton(button, id)
        # Enable the default setting
        self.quality_settings.button(self.quality).setChecked(True)

        # Timestamp
        for box in [self.ui.start_box, self.ui.end_box]:
            box.setDisplayFormat("hh:mm:ss")         
            box.setTime(QTime(0, 0, 0))             
            box.setMinimumTime(QTime(0, 0, 0))       
            box.setMaximumTime(QTime(9999, 59, 59))  
        self.ui.start_box.timeChanged.connect(self.check_time)
        self.ui.end_box.timeChanged.connect(self.check_time)

        # Connect Frame Leap Box
        self.ui.leap_box.valueChanged.connect(self.select_frame_leap)
        self.ui.leap_box.setRange(1, 1000)
        self.ui.leap_box.setValue(10)

        # Disable convert button initially
        self.ui.convert_button.setEnabled(False)

    def select_video_path(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select a Video File",
            "", "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*)"
        )
        if path:
            self.video_path = path
            self.ui.input_label.setText(self.video_path)
            self.enable_convert()

            # Get the duration of the video
            self.default_duration(path)

    def select_dir_path(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory"
        )
        if path:
            self.output_path = path
            self.ui.output_label.setText(self.output_path)
            self.enable_convert()
    
    def select_frame_leap(self, value):
        self.frame_leap = value

    def default_duration(self, path):
        # Set end time as the the duration of the video
        try:
            probe = ffmpeg.probe(self.video_path)
            duration = float(probe['format'].get('duration', 0))

            # Fallback to video_stream
            video_stream = None
            if duration == 0:
                # Fallback to video stream duration if available
                video_stream = next(
                    (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                    None
                )
                if video_stream and 'duration' in video_stream:
                    duration = float(video_stream['duration'])
                
            # If video extraction failed
            if duration == 0:
                 QMessageBox.critical(self, "Error", "Unfortunately, we are unable to retrive the duration")
                 return

            # Store duration as integer instead of float
            self.video_duration = int(round(duration))

            # Update the timestamp boxes
            h = self.video_duration // 3600
            m = (self.video_duration % 3600) // 60
            s = self.video_duration % 60
            timestamp = QTime(h,m,s)

            self.ui.end_box.setTime(timestamp)
            self.ui.end_box.setMaximumTime(timestamp)
            self.ui.start_box.setMaximumTime(timestamp)

        except ffmpeg.Error as e:
            QMessageBox.critical(
                self, "FFmpeg Error",
                f"An error occurred while probing the video:\n{e.stderr.decode()}"
            )
            self.ui.end_box.setTime(QTime(0, 0, 0))
            self.ui.end_box.setMaximumTime(QTime(9999, 59, 59))  # Reset to default maximum

        except Exception as e:
            QMessageBox.critical(
                self, "Unknown Error",
                f"An unexpected error occurred:\n{str(e)}"
            )
            self.ui.end_box.setTime(QTime(0, 0, 0))
            self.ui.end_box.setMaximumTime(QTime(9999, 59, 59))  # Reset to default maximum

    def check_time(self, qtime):
        self.start_time = self.retrive_time(self.ui.start_box)
        end_time = self.retrive_time(self.ui.end_box)

        if self.start_time > end_time:
            QMessageBox.warning(
                self, "Invalid Time Range",
                "Please set the start time below the end time."
            )
            self.ui.start_box.setTime(self.ui.end_box.time())
        elif end_time < self.start_time:
            QMessageBox.warning(
                self, "Invalid Time Range",
                "Please set the end time above the start time."
            )
            self.ui.end_box.setTime(self.ui.start_box.time())

    def retrive_time(self, box):
        qtime = box.time()
        total_seconds = (qtime.hour() * 3600) + (qtime.minute() * 60) + qtime.second()
        return total_seconds

    def enable_convert(self):
        if self.video_path and self.output_path:
            self.ui.convert_button.setEnabled(True)
        else:
            self.ui.convert_button.setEnabled(False)

    def disable_input(self):
        self.ui.convert_button.setEnabled(False)
        self.ui.input_button.setEnabled(False)
        self.ui.output_button.setEnabled(False)
        self.ui.quality_low.setEnabled(False)
        self.ui.quality_medium.setEnabled(False)
        self.ui.quality_high.setEnabled(False)
        self.ui.start_box.setEnabled(False)
        self.ui.end_box.setEnabled(False)
        self.ui.leap_box.setEnabled(False) 

    def enable_input(self):
        self.ui.convert_button.setEnabled(True)
        self.ui.input_button.setEnabled(True)
        self.ui.output_button.setEnabled(True)
        self.ui.quality_low.setEnabled(True)
        self.ui.quality_medium.setEnabled(True)
        self.ui.quality_high.setEnabled(True)
        self.ui.start_box.setEnabled(True)
        self.ui.end_box.setEnabled(True)
        self.ui.leap_box.setEnabled(True) 

    def convert(self):
        # Check quality setting
        if self.ui.quality_low.isChecked():
            self.quality = 10
        elif self.ui.quality_medium.isChecked():
            self.quality = 5
        else: #quality_high
            self.quality = 2

        # Reset loading bar
        self.ui.progress_bar.setValue(0)

        # Disable any further input
        self.disable_input()
        
        # Run the actual program
        self.run = VideoProcessing(
            self.video_path,
            self.output_path,
            self.start_time,
            self.video_duration,
            self.frame_leap,
            self.quality,
        )
        
        self.run.progress_percentage.connect(self.progress_percentage)
        self.run.finished.connect(self.enable_input)
        self.run.start()

    def progress_percentage(self, progress):
        self.ui.progress_bar.setValue(progress)
    
    def closeEvent(self, event):
        if hasattr(self, 'run') and self.run.isRunning():
            self.run.stop()
            self.run.wait()
        event.accept()