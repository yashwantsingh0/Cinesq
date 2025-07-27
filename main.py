# ──────────────────────────────────────────────────────────────
#  Cinesq - Video Player
#  Entry point for launching the application
#  Author: Yashwant Singh
#  License: MIT
# ──────────────────────────────────────────────────────────────

import sys
import signal
from PyQt5.QtWidgets import QApplication
from player.video_player import CinesqPlayer
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

if __name__ == '__main__':
    # Handle Ctrl+C in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Create app instance
    app = QApplication(sys.argv)
    app.setApplicationName("Cinesq Player")
    app.setWindowIcon(QIcon("assets/icons/app.svg"))
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    # Launch player
    player = CinesqPlayer()
    player.resize(1000, 600)
    player.show()

    # Run main loop
    sys.exit(app.exec_())
