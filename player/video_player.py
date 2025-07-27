# video_player.py

import os
import sys
import subprocess
import json
import gi

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QShortcut,
    QMenu, QMenuBar, QAction, QMessageBox
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, GstVideo

from player.controls import PlayerControls
from player.menubar import create_menu_bar
from player.playlist import Playlist

Gst.init(None)

CONFIG_DIR = os.path.expanduser("~/.config/cinesq")
RECENT_FILE = os.path.join(CONFIG_DIR, "recent.json")

class CinesqPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinesq Player")
        self.setAcceptDrops(True)
        self.setMinimumSize(800, 500)

        self.is_dark_theme = True
        self.is_fullscreen = False
        self.playlist_visible = False
        self.recent_files = self.load_recent_files()

        self.load_dark_qss()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # GStreamer pipeline
        self.pipeline = Gst.ElementFactory.make("playbin", "player")
        self.video_widget = QWidget()
        self.video_window_id = None

        # Player controls
        self.controls = PlayerControls(self)
        self.controls.play_button.clicked.connect(self.toggle_play)
        self.controls.stop_button.clicked.connect(self.stop_video)
        self.controls.rewind_button.clicked.connect(lambda: self.seek(-10))
        self.controls.forward_button.clicked.connect(lambda: self.seek(10))
        self.controls.volume_slider.valueChanged.connect(self.set_volume)
        self.controls.seek_slider.sliderMoved.connect(self.set_position)
        self.controls.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # Playlist
        self.playlist_model = Playlist()
        self.playlist_widget = QListWidget()
        self.playlist_widget.setMaximumHeight(100)
        self.playlist_widget.setVisible(False)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected_video)
        self.playlist_model.changed.connect(self.refresh_playlist_view)
        self.playlist_model.index_changed.connect(self.play_index)



        # Timer for position updates
        self.timer = self.startTimer(500)

        # Connect video output
        self.connect_video_sink()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.controls)
        layout.addWidget(self.playlist_widget)
        central_widget.setLayout(layout)

        # Shortcuts
        QShortcut(QKeySequence("Space"), self).activated.connect(self.toggle_play)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.exit_fullscreen)
        QShortcut(QKeySequence("Up"), self).activated.connect(lambda: self.adjust_volume(5))
        QShortcut(QKeySequence("Down"), self).activated.connect(lambda: self.adjust_volume(-5))

        # Menu bar
        menu_bar = create_menu_bar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.actions()[0].menu()
        playlist_menu = QMenu("Playlist", self)
        file_menu.addMenu(playlist_menu)

        toggle_playlist_action = QAction("Show Playlist", self, checkable=True)
        toggle_playlist_action.triggered.connect(self.toggle_playlist)
        playlist_menu.addAction(toggle_playlist_action)

        playlist_menu.addSeparator()
        playlist_menu.addAction("Clear Playlist", self.playlist_model.clear)
        playlist_menu.addAction("Save Playlist...", self.playlist_model.save)
        playlist_menu.addAction("Load Playlist...", self.playlist_model.load)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        file_menu.addAction(about_action)

        view_menu = next((a.menu() for a in menu_bar.actions() if a.text() == "View"), None)
        if view_menu:
            toggle_theme = QAction("Toggle Light/Dark", self)
            toggle_theme.triggered.connect(self.toggle_theme)
            view_menu.addAction(toggle_theme)

        # Timer for position updates
        self.timer = self.startTimer(500)

        # Connect video output
        self.connect_video_sink()

    def connect_video_sink(self):
        self.video_sink = Gst.ElementFactory.make("gtksink", None)
        if self.video_sink:
            self.pipeline.set_property("video-sink", self.video_sink)
            widget = self.video_sink.props.widget
            if widget:
                widget.set_parent_window(self.video_widget.winId())
                layout = QVBoxLayout(self.video_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(widget)

    def load_subtitle(self):
        print("Load subtitle triggered (not implemented yet).")

    def connect_video_sink(self):
        # Use the VideoOverlay interface to embed video into our Qt widget
        overlay = self.pipeline.get_property("video-sink")
        if isinstance(overlay, GstVideo.VideoOverlay):
            # WinId works on both X11 and Wayland (Qt translates appropriately)
            overlay.set_window_handle(int(self.video_widget.winId()))
        else:
            print("[VideoSink] Sink does not support VideoOverlay embedding")
        

    def disable_subtitle(self):
        print("Disable subtitle triggered (not implemented yet).")

    def adjust_sub_delay(self, ms):
        print(f"Adjust subtitle delay by {ms} ms (not implemented yet).")

    def adjust_sub_font(self, delta):
        print(f"Adjust subtitle font size by {delta} (not implemented yet).")

    def load_dark_qss(self):
        try:
            with open("themes/vlc_dark.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Failed to load theme: {e}")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.setStyleSheet(self.load_dark_qss() if self.is_dark_theme else "")

    def system_file_dialog(self, title="Select File", file_filter="*.*"):
        try:
            cmd = ["zenity", "--file-selection", "--title", title, "--file-filter", f"{file_filter} | {file_filter}"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception as e:
            print(f"[FileDialog] Error: {e}")
            return None

    def show_about(self):
        QMessageBox.information(self, "About Cinesq", (
            "<b>Cinesq Player</b><br><br>"
            "A sleek, native video player built with PyQt and GStreamer.<br><br>"
            "<b>Features:</b><ul>"
            "<li>GNOME-native file picker using Zenity</li>"
            "<li>Dark/light mode toggle</li>"
            "<li>Minimal fullscreen playback</li>"
            "<li>Playlist and recent files support</li>"
            "<li>Keyboard shortcuts: Space (play/pause), Up/Down (volume), Esc (fullscreen)</li>"
            "<li>Internal subtitle support via GStreamer</li>"
            "<li>Drag-and-drop file support</li>"
            "</ul>"
        ))

    def toggle_play(self):
        state = self.pipeline.get_state(1).state
        if state == Gst.State.PLAYING:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.controls.set_playing(False)
        else:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.controls.set_playing(True)

    def stop_video(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.controls.set_playing(False)

    def set_volume(self, value):
        self.pipeline.set_property("volume", value / 100.0)

    def adjust_volume(self, delta):
        current = self.pipeline.get_property("volume")
        self.set_volume(min(max((current * 100) + delta, 0), 100))

    def seek(self, seconds):
        success = self.pipeline.seek_simple(
            Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            self.pipeline.query_position(Gst.Format.TIME)[1] + seconds * Gst.SECOND
        )
        if not success:
            print("[Seek] Failed")

    def set_position(self, pos):
        dur = self.pipeline.query_duration(Gst.Format.TIME)[1]
        self.pipeline.seek_simple(
            Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            int(pos / 1000 * dur)
        )

    def timerEvent(self, _):
        success, pos = self.pipeline.query_position(Gst.Format.TIME)
        success_dur, dur = self.pipeline.query_duration(Gst.Format.TIME)
        if success and success_dur and dur:
            p = pos / dur if dur > 0 else 0
            self.controls.seek_slider.setValue(int(p * 1000))
            self.controls.time_left.setText(f"{pos // Gst.SECOND // 60:02}:{(pos // Gst.SECOND) % 60:02}")
            self.controls.time_right.setText(f"{dur // Gst.SECOND // 60:02}:{(dur // Gst.SECOND) % 60:02}")

    def load_recent_files(self):
        try:
            if os.path.exists(RECENT_FILE):
                with open(RECENT_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[Recent] Failed to load: {e}")
        return []

    def save_recent_files(self):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(RECENT_FILE, 'w') as f:
                json.dump(self.recent_files[-10:], f)
        except Exception as e:
            print(f"[Recent] Failed to save: {e}")

    def open_file(self, path=None):
        if not path:
            file = self.system_file_dialog("Open Media", "*.mp4 *.mkv *.avi *.webm")
        else:
            file = path
        if file:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline.set_property("uri", Gst.filename_to_uri(file))
            self.pipeline.set_state(Gst.State.PLAYING)
            self.controls.set_playing(True)
            self.playlist_model.add(file)
            if file not in self.recent_files:
                self.recent_files.append(file)
                self.recent_files = self.recent_files[-10:]
                self.save_recent_files()

    def refresh_playlist_view(self):
        self.playlist_widget.clear()
        for file in self.playlist_model.all_files():
            self.playlist_widget.addItem(os.path.basename(file))

    def play_selected_video(self, item):
        index = self.playlist_widget.row(item)
        self.playlist_model.set_index(index)

    def play_index(self, index):
        path = self.playlist_model.current()
        if path:
            self.open_file(path)

    def toggle_playlist(self, visible):
        self.playlist_widget.setVisible(visible)
        self.playlist_visible = visible

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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.open_file(url.toLocalFile())


if __name__ == "__main__":
    GObject.threads_init()
    app = QApplication(sys.argv)
    player = CinesqPlayer()
    player.show()
    sys.exit(app.exec_())
