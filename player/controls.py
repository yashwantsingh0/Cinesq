# player/controls.py

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


class PlayerControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)

        # ─── Time Labels + Seek Slider ─────────────
        self.time_left = QLabel("00:00")
        self.time_right = QLabel("00:00")

        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 1000)
        self.seek_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.seek_slider.setToolTip("Seek through video")

        seek_layout = QHBoxLayout()
        seek_layout.addWidget(self.time_left)
        seek_layout.addWidget(self.seek_slider)
        seek_layout.addWidget(self.time_right)

        # ─── Playback Buttons ─────────────
        self.rewind_button = QPushButton()
        self.rewind_button.setIcon(QIcon("assets/icons/rewind.svg"))
        self.rewind_button.setIconSize(QSize(20, 20))
        self.rewind_button.setToolTip("Rewind 10 seconds")

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("assets/icons/play.svg"))
        self.play_button.setIconSize(QSize(24, 24))
        self.play_button.setToolTip("Play / Pause")

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("assets/icons/stop.svg"))
        self.stop_button.setIconSize(QSize(20, 20))
        self.stop_button.setToolTip("Stop playback")

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon("assets/icons/forward.svg"))
        self.forward_button.setIconSize(QSize(20, 20))
        self.forward_button.setToolTip("Forward 10 seconds")

        # ─── Volume Controls ─────────────
        self.volume_icon = QPushButton()
        self.volume_icon.setIcon(QIcon("assets/icons/volume.svg"))
        self.volume_icon.setIconSize(QSize(20, 20))
        self.volume_icon.setToolTip("Mute / Unmute")
        self.volume_icon.setFlat(True)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setToolTip("Adjust volume")

        # ─── Fullscreen ─────────────
        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(QIcon("assets/icons/fullscreen.svg"))
        self.fullscreen_button.setIconSize(QSize(20, 20))
        self.fullscreen_button.setToolTip("Toggle fullscreen mode")

        # ─── Layout ─────────────
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        control_layout.setContentsMargins(10, 0, 10, 0)

        control_layout.addWidget(self.rewind_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.forward_button)
        control_layout.addStretch()
        control_layout.addWidget(self.volume_icon)
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.fullscreen_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.addLayout(seek_layout)
        layout.addLayout(control_layout)

        self.setLayout(layout)

    def set_playing(self, playing: bool):
        icon_name = "pause.svg" if playing else "play.svg"
        self.play_button.setIcon(QIcon(f"assets/icons/{icon_name}"))
