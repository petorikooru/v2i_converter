# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QTimeEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(732, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(732, 300))
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.VideoDisplay))
        MainWindow.setWindowIcon(icon)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(732, 300))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 732, 301))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 171, 16))
        self.selection_group = QGroupBox(self.frame)
        self.selection_group.setObjectName(u"selection_group")
        self.selection_group.setGeometry(QRect(10, 30, 711, 131))
        sizePolicy1.setHeightForWidth(self.selection_group.sizePolicy().hasHeightForWidth())
        self.selection_group.setSizePolicy(sizePolicy1)
        self.selection_group.setMouseTracking(False)
        self.formLayout = QFormLayout(self.selection_group)
        self.formLayout.setObjectName(u"formLayout")
        self.vid_label = QLabel(self.selection_group)
        self.vid_label.setObjectName(u"vid_label")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.vid_label)

        self.vid_button = QPushButton(self.selection_group)
        self.vid_button.setObjectName(u"vid_button")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.vid_button)

        self.vid_dir = QLabel(self.selection_group)
        self.vid_dir.setObjectName(u"vid_dir")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.vid_dir)

        self.line = QFrame(self.selection_group)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.line)

        self.out_label = QLabel(self.selection_group)
        self.out_label.setObjectName(u"out_label")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.out_label)

        self.out_button = QPushButton(self.selection_group)
        self.out_button.setObjectName(u"out_button")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.out_button)

        self.out_dir = QLabel(self.selection_group)
        self.out_dir.setObjectName(u"out_dir")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.out_dir)

        self.status_label = QLabel(self.frame)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setGeometry(QRect(10, 260, 711, 41))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_box = QGroupBox(self.frame)
        self.status_box.setObjectName(u"status_box")
        self.status_box.setGeometry(QRect(10, 210, 711, 50))
        sizePolicy1.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.status_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loading_bar = QProgressBar(self.status_box)
        self.loading_bar.setObjectName(u"loading_bar")
        self.loading_bar.setValue(0)

        self.horizontalLayout_3.addWidget(self.loading_bar)

        self.convert_button = QPushButton(self.status_box)
        self.convert_button.setObjectName(u"convert_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.convert_button.sizePolicy().hasHeightForWidth())
        self.convert_button.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.convert_button)

        self.quality_group = QGroupBox(self.frame)
        self.quality_group.setObjectName(u"quality_group")
        self.quality_group.setGeometry(QRect(450, 160, 271, 51))
        sizePolicy1.setHeightForWidth(self.quality_group.sizePolicy().hasHeightForWidth())
        self.quality_group.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.quality_group)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.quality_label = QLabel(self.quality_group)
        self.quality_label.setObjectName(u"quality_label")

        self.horizontalLayout_2.addWidget(self.quality_label)

        self.low_quality_box = QRadioButton(self.quality_group)
        self.low_quality_box.setObjectName(u"low_quality_box")

        self.horizontalLayout_2.addWidget(self.low_quality_box)

        self.medium_quality_box = QRadioButton(self.quality_group)
        self.medium_quality_box.setObjectName(u"medium_quality_box")

        self.horizontalLayout_2.addWidget(self.medium_quality_box)

        self.high_quality_box = QRadioButton(self.quality_group)
        self.high_quality_box.setObjectName(u"high_quality_box")

        self.horizontalLayout_2.addWidget(self.high_quality_box)

        self.configuration_group = QGroupBox(self.frame)
        self.configuration_group.setObjectName(u"configuration_group")
        self.configuration_group.setGeometry(QRect(10, 160, 441, 51))
        sizePolicy1.setHeightForWidth(self.configuration_group.sizePolicy().hasHeightForWidth())
        self.configuration_group.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.configuration_group)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.start_label = QLabel(self.configuration_group)
        self.start_label.setObjectName(u"start_label")

        self.horizontalLayout.addWidget(self.start_label)

        self.start_box = QTimeEdit(self.configuration_group)
        self.start_box.setObjectName(u"start_box")

        self.horizontalLayout.addWidget(self.start_box)

        self.end_label = QLabel(self.configuration_group)
        self.end_label.setObjectName(u"end_label")

        self.horizontalLayout.addWidget(self.end_label)

        self.end_box = QTimeEdit(self.configuration_group)
        self.end_box.setObjectName(u"end_box")

        self.horizontalLayout.addWidget(self.end_box)

        self.frame_label = QLabel(self.configuration_group)
        self.frame_label.setObjectName(u"frame_label")

        self.horizontalLayout.addWidget(self.frame_label)

        self.frame_box = QSpinBox(self.configuration_group)
        self.frame_box.setObjectName(u"frame_box")

        self.horizontalLayout.addWidget(self.frame_box)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Video to Image Converter!", None))
        self.selection_group.setTitle("")
        self.vid_label.setText(QCoreApplication.translate("MainWindow", u"Video path", None))
        self.vid_button.setText(QCoreApplication.translate("MainWindow", u"Change", None))
        self.vid_dir.setText(QCoreApplication.translate("MainWindow", u"No video file selected.", None))
        self.out_label.setText(QCoreApplication.translate("MainWindow", u"Output path", None))
        self.out_button.setText(QCoreApplication.translate("MainWindow", u"Change", None))
        self.out_dir.setText(QCoreApplication.translate("MainWindow", u"No output directory selected.", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"Hello ^o^/", None))
        self.status_box.setTitle("")
        self.convert_button.setText(QCoreApplication.translate("MainWindow", u"Convert!", None))
        self.quality_group.setTitle("")
        self.quality_label.setText(QCoreApplication.translate("MainWindow", u"Quality :", None))
        self.low_quality_box.setText(QCoreApplication.translate("MainWindow", u"Low", None))
        self.medium_quality_box.setText(QCoreApplication.translate("MainWindow", u"Medium", None))
        self.high_quality_box.setText(QCoreApplication.translate("MainWindow", u"High", None))
        self.configuration_group.setTitle("")
        self.start_label.setText(QCoreApplication.translate("MainWindow", u"Start :", None))
        self.end_label.setText(QCoreApplication.translate("MainWindow", u"End :", None))
        self.frame_label.setText(QCoreApplication.translate("MainWindow", u"Frame Skip : ", None))
    # retranslateUi

