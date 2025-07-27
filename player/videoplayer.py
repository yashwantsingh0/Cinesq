# player/videoplayer.py
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QStackedLayout, QLabel, QFileDialog, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from player.titlebar import TitleBar

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMinimumSize(800, 500)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        self.layout.addWidget(self.title_bar)

        # Placeholder for video area
        self.layout.addStretch()

        self.setLayout(self.layout)
