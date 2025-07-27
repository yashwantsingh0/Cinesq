import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog, QShortcut, QListWidget, QApplication,
    QMainWindow, QAction, QMenu, QMenuBar
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from player.controls import PlayerControls
from player.menubar import create_menu_bar


class CinesqPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinesq Player")
        self.setAcceptDrops(True)
        self.setMinimumSize(800, 500)

        self.is_dark_theme = True
        self.is_fullscreen = False
        self.playlist_visible = False

        self.load_dark_qss()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ─── Media Player ─────────────
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # ─── Player Controls ─────────
        self.controls = PlayerControls(self)
        self.controls.play_button.clicked.connect(self.toggle_play)
        self.controls.stop_button.clicked.connect(self.stop_video)
        self.controls.rewind_button.clicked.connect(lambda: self.seek(-10000))
        self.controls.forward_button.clicked.connect(lambda: self.seek(10000))
        self.controls.volume_slider.valueChanged.connect(self.media_player.setVolume)
        self.controls.seek_slider.sliderMoved.connect(self.set_position)
        self.controls.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # ─── Playlist (hidden by default) ─────────
        self.playlist = QListWidget()
        self.playlist.setMaximumHeight(100)
        self.playlist.setVisible(False)
        self.playlist.itemDoubleClicked.connect(self.play_selected_video)
        self.recent_files = []

        # ─── Layout ─────────────
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.controls)
        layout.addWidget(self.playlist)
        central_widget.setLayout(layout)

        # ─── Signals ─────────────
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_range)
        self.media_player.stateChanged.connect(self.update_button)

        # ─── Shortcuts ─────────────
        QShortcut(QKeySequence("Space"), self).activated.connect(self.toggle_play)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.exit_fullscreen)

        # ─── Menu Bar ─────────────
        menu_bar = create_menu_bar(self)
        self.setMenuBar(menu_bar)

        # Add Playlist toggle to File menu
        file_menu = menu_bar.actions()[0].menu()
        toggle_playlist_action = QAction("Show Playlist", self, checkable=True)
        toggle_playlist_action.triggered.connect(self.toggle_playlist)
        file_menu.addAction(toggle_playlist_action)

        # Add theme toggle
        view_menu = next((a.menu() for a in menu_bar.actions() if a.text() == "View"), None)
        if view_menu:
            toggle_theme = QAction("Toggle Light/Dark", self)
            toggle_theme.triggered.connect(self.toggle_theme)
            view_menu.addAction(toggle_theme)

    # ────── Theme/QSS ──────────
    def load_dark_qss(self):
        try:
            with open("themes/vlc_dark.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Failed to load theme: {e}")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.load_dark_qss()
        else:
            self.setStyleSheet("")  # fallback to light

    # ────── Playback ───────────
    def toggle_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.controls.set_playing(False)
        else:
            self.media_player.play()
            self.controls.set_playing(True)

    def stop_video(self):
        self.media_player.stop()
        self.controls.set_playing(False)

    def seek(self, ms):
        self.media_player.setPosition(self.media_player.position() + ms)

    def set_position(self, pos):
        dur = self.media_player.duration()
        self.media_player.setPosition(int(dur * (pos / 1000.0)))

    def update_slider(self, pos):
        dur = self.media_player.duration()
        if dur > 0:
            self.controls.seek_slider.setValue(int((pos / dur) * 1000))
            ps = pos // 1000
            ds = dur // 1000
            self.controls.time_left.setText(f"{ps // 60:02}:{ps % 60:02}")
            self.controls.time_right.setText(f"{ds // 60:02}:{ds % 60:02}")

    def update_range(self, dur):
        self.controls.seek_slider.setValue(0)

    def update_button(self, state):
        self.controls.set_playing(state == QMediaPlayer.PlayingState)

    # ────── Playlist ───────────
    def open_file(self, path=None):
        if not path:
            file, _ = QFileDialog.getOpenFileName(self, "Open Video")
        else:
            file = path
        if file:
            url = QUrl.fromLocalFile(file)
            self.media_player.setMedia(QMediaContent(url))
            self.media_player.play()
            self.controls.set_playing(True)
            if file not in self.recent_files:
                self.recent_files.append(file)
                self.playlist.addItem(os.path.basename(file))

    def play_selected_video(self, item):
        idx = self.playlist.row(item)
        if 0 <= idx < len(self.recent_files):
            self.open_file(self.recent_files[idx])

    def toggle_playlist(self, visible):
        self.playlist.setVisible(visible)
        self.playlist_visible = visible

    # ────── Fullscreen + Context Menu ───────────
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.exit_fullscreen()
        else:
            self.menuBar().hide()
            self.controls.hide()
            self.showFullScreen()
            self.is_fullscreen = True

    def exit_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.menuBar().show()
            self.controls.show()
            self.is_fullscreen = False

    def contextMenuEvent(self, event):
        if not self.isFullScreen():
            return
        menu = QMenu(self)
        menu.addAction("Pause", self.toggle_play)
        menu.addAction("Stop", self.stop_video)
        menu.addSeparator()
        menu.addAction("Leave Fullscreen", self.exit_fullscreen)
        menu.addAction("Open Media", self.open_file)
        menu.addAction("Quit", self.close)
        menu.exec_(event.globalPos())

    # ────── Drag & Drop ────────
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
