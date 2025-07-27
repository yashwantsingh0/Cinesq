# video_player.py (QtMultimedia-based)
import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QSlider,
                             QFileDialog, QHBoxLayout, QShortcut, QListWidget, QApplication, QStyle, QMainWindow,
                             QAction, QMenu)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Import the modular menubar
from player.menubar import create_menu_bar

class CinesqPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinesq Player")
        self.setAcceptDrops(True)
        self.setMinimumSize(800, 500)

        # Apply dark theme with gradient background
        self.apply_dark_theme()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Media player and video output
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # Playback controls
        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.toggle_play)

        self.stopButton = QPushButton()
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.clicked.connect(self.stop_video)

        self.forwardButton = QPushButton("▶▶")
        self.forwardButton.clicked.connect(lambda: self.seek(10000))

        self.rewindButton = QPushButton("◀◀")
        self.rewindButton.clicked.connect(lambda: self.seek(-10000))

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.media_player.setVolume)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 1000)
        self.positionSlider.sliderMoved.connect(self.set_position)

        # Playlist
        self.playlist = QListWidget()
        self.playlist.setMaximumHeight(100)
        self.playlist.itemDoubleClicked.connect(self.play_selected_video)
        self.recent_files = []

        # Timer to update position
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_ui)

        # Layouts
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.rewindButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(QLabel("Volume"))
        controlLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.positionSlider)
        layout.addLayout(controlLayout)
        layout.addWidget(self.playlist)

        central_widget.setLayout(layout)

        # Signals
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_range)
        self.media_player.stateChanged.connect(self.update_button)

        # Shortcuts
        QShortcut(QKeySequence("Space"), self).activated.connect(self.toggle_play)
        QShortcut(QKeySequence("Right"), self).activated.connect(lambda: self.seek(5000))
        QShortcut(QKeySequence("Left"), self).activated.connect(lambda: self.seek(-5000))

        # Add modular menu bar
        menu_bar = create_menu_bar(self)
        self.setMenuBar(menu_bar)
        
        # Find existing View menu and add theme toggle
        view_menu = None
        for action in menu_bar.actions():
            if action.text() == "View":
                view_menu = action.menu()
                break
        
        if view_menu:
            toggle_theme_action = QAction("Toggle Light/Dark", self)
            toggle_theme_action.triggered.connect(self.toggle_theme)
            view_menu.addAction(toggle_theme_action)
        else:
            print("Warning: 'View' menu not found. Theme toggle not added.")


        self.is_dark_theme = True

    def apply_dark_theme(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor("#2c2c2c"))
        gradient.setColorAt(1.0, QColor("#1e1e1e"))
        brush = QBrush(gradient)
        palette.setBrush(QPalette.Window, brush)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#121212"))
        palette.setColor(QPalette.Text, Qt.white)
        self.setPalette(palette)

    def apply_light_theme(self):
        self.setPalette(QApplication.style().standardPalette())

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def toggle_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop_video(self):
        self.media_player.stop()

    def set_position(self, position):
        duration = self.media_player.duration()
        self.media_player.setPosition(int(duration * (position / 1000.0)))

    def update_ui(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            pos = self.media_player.position()
            dur = self.media_player.duration()
            if dur > 0:
                self.positionSlider.setValue(int((pos / dur) * 1000))

    def update_slider(self, position):
        if self.media_player.duration() > 0:
            self.positionSlider.setValue(int((position / self.media_player.duration()) * 1000))

    def update_range(self, duration):
        self.positionSlider.setValue(0)

    def update_button(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.timer.start()
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()

    def seek(self, ms):
        self.media_player.setPosition(self.media_player.position() + ms)

    def open_file(self, path=None):
        if not path:
            file, _ = QFileDialog.getOpenFileName(self, "Open Video")
        else:
            file = path

        if file:
            url = QUrl.fromLocalFile(file)
            self.media_player.setMedia(QMediaContent(url))
            self.media_player.play()
            if file not in self.recent_files:
                self.recent_files.append(file)
                self.playlist.addItem(os.path.basename(file))

    def play_selected_video(self, item):
        index = self.playlist.row(item)
        if 0 <= index < len(self.recent_files):
            self.open_file(self.recent_files[index])

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.open_file(url.toLocalFile())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = CinesqPlayer()
    player.show()
    sys.exit(app.exec_())

