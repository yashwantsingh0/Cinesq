from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(40)
        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 220);
            color: white;
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        # App name
        self.title = QLabel("Cinesq")
        self.title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(self.title)

        layout.addStretch()

        # Minimize button
        self.min_button = QPushButton("-")
        self.min_button.clicked.connect(parent.showMinimized)
        layout.addWidget(self.min_button)

        # Maximize button
        self.max_button = QPushButton("⬜")
        self.max_button.clicked.connect(self.toggle_max_restore)
        layout.addWidget(self.max_button)

        # Close button
        self.close_button = QPushButton("✕")
        self.close_button.clicked.connect(parent.close)
        layout.addWidget(self.close_button)

        for btn in [self.min_button, self.max_button, self.close_button]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("background: none; color: white; border: none; font-size: 14px;")

        self.setLayout(layout)
        self._is_maximized = False
        self.parent = parent

    def toggle_max_restore(self):
        if self._is_maximized:
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
        self._is_maximized = not self._is_maximized

