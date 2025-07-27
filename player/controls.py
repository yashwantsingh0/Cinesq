# player/controls.py

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt


class PlayerControls(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)

        self.play_button = QPushButton("▶")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setValue(50)

        self.time_label = QLabel("00:00 / 00:00")
        self.seek_slider = QSlider(Qt.Horizontal)

        self.fullscreen_button = QPushButton("⛶")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.addWidget(self.play_button)
        layout.addWidget(self.seek_slider)
        layout.addWidget(self.time_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.fullscreen_button)

        self.setLayout(layout)
