import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QSlider, QHBoxLayout, QVBoxLayout, QFileDialog, QAction
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTime, QTimer


class CinesqPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinesq")
        self.setGeometry(100, 100, 960, 540)

        # Media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        # Buttons
        self.play_button = QPushButton("⏵")
        self.play_button.clicked.connect(self.toggle_play)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.time_label = QLabel("00:00 / 00:00")

        # Layouts
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(10, 5, 10, 10)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.position_slider)
        control_layout.addWidget(self.time_label)

        video_layout = QVBoxLayout()
        video_layout.addWidget(self.video_widget)
        video_layout.addLayout(control_layout)

        widget = QWidget()
        widget.setLayout(video_layout)
        self.setCentralWidget(widget)

        # Set video output
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)

        # Menu
        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open Video", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.play_button.setText("⏸")
            self.media_player.play()

    def toggle_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("⏵")
        else:
            self.media_player.play()
            self.play_button.setText("⏸")

    def update_position(self, position):
        self.position_slider.setValue(position)
        duration = self.media_player.duration()
        if duration > 0:
            current_time = QTime(0, 0, 0).addMSecs(position)
            total_time = QTime(0, 0, 0).addMSecs(duration)
            self.time_label.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")

    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = CinesqPlayer()
    player.show()
    sys.exit(app.exec_())

