# ──────────────────────────────────────────────────────────────
#  Cinesq - Video Player
#  Entry point for launching the application
#  Author: Yashwant Singh
#  License: MIT
# ──────────────────────────────────────────────────────────────

import sys
from PyQt5.QtWidgets import QApplication
from player.video_player import CinesqPlayer  # FIXED import

def main():
    app = QApplication(sys.argv)
    window = CinesqPlayer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

