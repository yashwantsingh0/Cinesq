# player/menubar.py

from PyQt5.QtWidgets import (
    QMenuBar, QMenu, QAction, QMessageBox
)

def create_menu_bar(parent):
    menubar = QMenuBar(parent)

    # ─── File Menu ─────────────────────
    file_menu = menubar.addMenu("File")

    open_action = QAction("Open Media", parent)
    open_action.triggered.connect(parent.open_file)
    file_menu.addAction(open_action)

    # Recent media submenu
    recent_menu = QMenu("Open Recent Media", parent)
    file_menu.addMenu(recent_menu)

    # Dynamically populate recent files (if any)
    def refresh_recent_menu():
        recent_menu.clear()
        for path in parent.recent_files[-10:][::-1]:  # limit 10
            name = path.split("/")[-1]
            action = QAction(name, parent)
            action.triggered.connect(lambda checked=False, p=path: parent.open_file(p))
            recent_menu.addAction(action)

    parent.recent_files_changed = refresh_recent_menu  # Hook for future use
    refresh_recent_menu()

    # ─── Playback Menu ─────────────────
    playback_menu = menubar.addMenu("Playback")
    # Placeholder actions can go here later

    # ─── Audio Menu ────────────────────
    audio_menu = menubar.addMenu("Audio")

    # ─── Video Menu ────────────────────
    video_menu = menubar.addMenu("Video")

    # ─── Subtitles Menu ────────────────
    subtitle_menu = menubar.addMenu("Subtitles")

    # ─── Tools Menu ────────────────────
    tools_menu = menubar.addMenu("Tools")

    # ─── View Menu ─────────────────────
    view_menu = menubar.addMenu("View")

    # ─── Help Menu ─────────────────────
    help_menu = menubar.addMenu("Help")
    about_action = QAction("About Author", parent)
    about_action.triggered.connect(lambda: QMessageBox.information(
        parent, "About Author",
        "Cinesq Player\nMade by Yashwant Singh\n\nGitHub: yashwantsingh0"
    ))
    help_menu.addAction(about_action)

    return menubar
