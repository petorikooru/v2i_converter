# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from controller import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.setWindowTitle("Video to Image Converter")
    widget.show()
    sys.exit(app.exec())
