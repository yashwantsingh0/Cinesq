import os
import json
from PyQt5.QtCore import QObject, pyqtSignal

CONFIG_DIR = os.path.expanduser("~/.config/cinesq")
PLAYLIST_FILE = os.path.join(CONFIG_DIR, "playlist.json")

class Playlist(QObject):
    changed = pyqtSignal()
    index_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.files = []
        self.current_index = -1

    def add(self, path):
        if path not in self.files:
            self.files.append(path)
            self.changed.emit()

    def all_files(self):
        return self.files

    def clear(self):
        self.files.clear()
        self.current_index = -1
        self.changed.emit()

    def current(self):
        if 0 <= self.current_index < len(self.files):
            return self.files[self.current_index]
        return None

    def set_index(self, index):
        if 0 <= index < len(self.files):
            self.current_index = index
            self.index_changed.emit(index)

    def save(self):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(PLAYLIST_FILE, 'w') as f:
                json.dump(self.files, f)
        except Exception as e:
            print(f"[Playlist] Failed to save: {e}")

    def load(self):
        try:
            if os.path.exists(PLAYLIST_FILE):
                with open(PLAYLIST_FILE, 'r') as f:
                    self.files = json.load(f)
                self.current_index = -1
                self.changed.emit()
        except Exception as e:
            print(f"[Playlist] Failed to load: {e}")
