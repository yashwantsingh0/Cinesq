# player/menubar.py

from PyQt5.QtWidgets import (
    QMenuBar, QMenu, QAction, QMessageBox
)

def create_menu_bar(parent):
    menubar = QMenuBar(parent)

    # ─── File Menu ─────────────────────
    file_menu = menubar.addMenu("File")

    open_action = QAction("Open Media…", parent)
    open_action.setShortcut("Ctrl+O")
    open_action.triggered.connect(parent.open_file)
    file_menu.addAction(open_action)

    # ─── Playlist toggle ───────────────
    toggle_playlist = QAction("Toggle Playlist", parent)
    toggle_playlist.setShortcut("Ctrl+P")
    toggle_playlist.setCheckable(True)
    toggle_playlist.setChecked(False)
    toggle_playlist.triggered.connect(parent.toggle_playlist)
    file_menu.addAction(toggle_playlist)

    file_menu.addSeparator()

    # ─── Recent media submenu ──────────
    recent_menu = QMenu("Open Recent Media", parent)
    file_menu.addMenu(recent_menu)

    def refresh_recent_menu():
        recent_menu.clear()
        for path in parent.recent_files[-10:][::-1]:
            name = path.split("/")[-1]
            action = QAction(name, parent)
            action.triggered.connect(lambda checked=False, p=path: parent.open_file(p))
            recent_menu.addAction(action)

    parent.recent_files_changed = refresh_recent_menu
    refresh_recent_menu()

    file_menu.addSeparator()

    quit_action = QAction("Quit", parent)
    quit_action.setShortcut("Ctrl+Q")
    quit_action.triggered.connect(parent.close)
    file_menu.addAction(quit_action)

    # ─── Playback Menu ─────────────────
    playback_menu = menubar.addMenu("Playback")

    play_pause = QAction("Play / Pause", parent)
    play_pause.setShortcut("Space")
    play_pause.triggered.connect(parent.toggle_play)

    playback_menu.addAction(play_pause)

    stop = QAction("Stop", parent)
    stop.setShortcut("S")
    stop.triggered.connect(parent.stop_video)

    playback_menu.addAction(stop)

    playback_menu.addSeparator()

    rewind = QAction("Rewind 10s", parent)
    rewind.setShortcut("Left")
    rewind.triggered.connect(lambda: parent.seek_relative(-10))
    playback_menu.addAction(rewind)

    forward = QAction("Forward 10s", parent)
    forward.setShortcut("Right")
    forward.triggered.connect(lambda: parent.seek_relative(10))
    playback_menu.addAction(forward)

    playback_menu.addSeparator()

    vol_up = QAction("Increase Volume", parent)
    vol_up.setShortcut("Up")
    vol_up.triggered.connect(lambda: parent.adjust_volume(+10))
    playback_menu.addAction(vol_up)

    vol_down = QAction("Decrease Volume", parent)
    vol_down.setShortcut("Down")
    vol_down.triggered.connect(lambda: parent.adjust_volume(-10))
    playback_menu.addAction(vol_down)

    # ─── Audio Menu ────────────────────
    audio_menu = menubar.addMenu("Audio")
    # Placeholder — implement audio track switching later

    # ─── Video Menu ────────────────────
    video_menu = menubar.addMenu("Video")

    toggle_fullscreen = QAction("Toggle Fullscreen", parent)
    toggle_fullscreen.setShortcut("F")
    toggle_fullscreen.triggered.connect(parent.toggle_fullscreen)
    video_menu.addAction(toggle_fullscreen)

    # ─── Subtitles Menu ────────────────
    subtitle_menu = menubar.addMenu("Subtitles")

    load_sub = QAction("Load External Subtitle…", parent)
    load_sub.triggered.connect(parent.load_subtitle)
    subtitle_menu.addAction(load_sub)

    subtitle_menu.addSeparator()

    inc_font = QAction("Increase Font Size", parent)
    inc_font.triggered.connect(lambda: parent.adjust_sub_font(+2))
    subtitle_menu.addAction(inc_font)

    dec_font = QAction("Decrease Font Size", parent)
    dec_font.triggered.connect(lambda: parent.adjust_sub_font(-2))
    subtitle_menu.addAction(dec_font)

    subtitle_menu.addSeparator()

    delay_up = QAction("Delay +0.5s", parent)
    delay_up.triggered.connect(lambda: parent.adjust_sub_delay(+500))
    subtitle_menu.addAction(delay_up)

    delay_down = QAction("Delay -0.5s", parent)
    delay_down.triggered.connect(lambda: parent.adjust_sub_delay(-500))
    subtitle_menu.addAction(delay_down)

    subtitle_menu.addSeparator()

    disable_sub = QAction("Disable Subtitles", parent)
    disable_sub.triggered.connect(parent.disable_subtitle)
    subtitle_menu.addAction(disable_sub)

    # ─── Tools Menu ────────────────────
    tools_menu = menubar.addMenu("Tools")
    # Placeholder for future tools (screenshot, color settings, etc.)

    # ─── View Menu ─────────────────────
    view_menu = menubar.addMenu("View")
    # Placeholder for future themes/layouts

    # ─── Help Menu ─────────────────────
    help_menu = menubar.addMenu("Help")

    about_action = QAction("About Cinesq", parent)
    about_action.triggered.connect(lambda: QMessageBox.information(
        parent, "About Cinesq Player",
        "🎬 Cinesq Player v2.0\n"
        "A clean, minimalistic video player built with PyQt5 and GStreamer.\n\n"
        "Features:\n"
        "– GStreamer backend for fast and efficient playback\n"
        "– Dark and light UI themes\n"
        "– Fullscreen minimal UI\n"
        "– Subtitle loading, delay, font size controls\n"
        "– GNOME-native file picker via Zenity\n"
        "– Playlist integration\n"
        "– Keyboard shortcuts (Space, F, Up/Down, etc.)\n\n"
        "👨‍💻 Made by Yashwant Singh\n"
        "🔗 GitHub: https://github.com/yashwantsingh0"
    ))
    help_menu.addAction(about_action)

    return menubar
