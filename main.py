# ──────────────────────────────────────────────────────────────
#  Cinesq - Video Player
#  Entry point for launching the application
#  Author: Yashwant Singh
#  License: MIT
# ──────────────────────────────────────────────────────────────

# main.py
import sys
from PyQt5.QtWidgets import QApplication
from player.video_player import CinesqPlayer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = CinesqPlayer()
    player.show()
    sys.exit(app.exec_())

