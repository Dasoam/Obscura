# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Settings Dialog - Scrollable and Responsive
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QGroupBox, QButtonGroup, 
    QMessageBox, QScrollArea, QWidget, QSizePolicy
)
from PySide6.QtCore import Signal, QProcess, QCoreApplication, Qt
import sys
import os
import logging

from windows_app.config.preferences import get_preferences

logger = logging.getLogger("Obscura.UI.Settings")

# Main theme color - change this to change the overall look
BG_COLOR = "#0f1419"  # Dark blue-black (GitHub dark)
BOX_COLOR = "#1c2128"  # Slightly lighter for boxes
ACCENT_COLOR = "#58a6ff"  # Blue accent


class SettingsDialog(QDialog):
    mode_changed = Signal(str)
    preferences_changed = Signal()
    
    def __init__(self, current_mode: str = "lite", parent=None):
        super().__init__(parent)
        self.current_mode = current_mode
        self.preferences = get_preferences()
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Obscura Settings")
        self.setMinimumSize(400, 300)
        self.resize(480, 550)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: {BG_COLOR}; }}
            QScrollBar:vertical {{ background: #21262d; width: 10px; }}
            QScrollBar::handle:vertical {{ background: #484f58; border-radius: 5px; min-height: 30px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)
        
        # Content container - MUST ALSO SET BACKGROUND
        container = QWidget()
        container.setStyleSheet(f"background: {BG_COLOR};")
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Settings")
        header.setStyleSheet(f"color: {ACCENT_COLOR}; font-weight: bold; font-size: 18px; background: transparent;")
        content_layout.addWidget(header)
        
        # PRIVACY MODE
        privacy_group = QGroupBox("Privacy Mode")
        p_layout = QVBoxLayout()
        
        self.mode_btns = QButtonGroup(self)
        
        self.lite_rb = QRadioButton("Lite - Maximum Privacy")
        self.lite_rb.setChecked(self.current_mode == "lite")
        self.mode_btns.addButton(self.lite_rb, 0)
        p_layout.addWidget(self.lite_rb)
        p_layout.addWidget(self._desc("No JavaScript, no cookies, text-only"))
        
        self.std_rb = QRadioButton("Standard - Balanced")
        self.std_rb.setChecked(self.current_mode == "standard")
        self.mode_btns.addButton(self.std_rb, 1)
        p_layout.addWidget(self.std_rb)
        p_layout.addWidget(self._desc("Session cookies, images allowed"))
        
        self.tor_rb = QRadioButton("Tor - Anonymous")
        self.tor_rb.setChecked(self.current_mode == "tor")
        self.mode_btns.addButton(self.tor_rb, 2)
        p_layout.addWidget(self.tor_rb)
        p_layout.addWidget(self._desc("Traffic routed via Tor network"))
        
        privacy_group.setLayout(p_layout)
        content_layout.addWidget(privacy_group)
        
        # SEARCH ENGINE
        search_group = QGroupBox("Search Engine")
        s_layout = QVBoxLayout()
        
        self.search_btns = QButtonGroup(self)
        curr_engine = self.preferences.get_search_engine()
        
        self.ddg_rb = QRadioButton("DuckDuckGo")
        self.ddg_rb.setChecked(curr_engine == "duckduckgo")
        self.search_btns.addButton(self.ddg_rb, 0)
        s_layout.addWidget(self.ddg_rb)
        s_layout.addWidget(self._desc("Works immediately, no setup needed"))
        
        self.searx_rb = QRadioButton("SearxNG")
        self.searx_rb.setChecked(curr_engine == "searxng")
        self.search_btns.addButton(self.searx_rb, 1)
        s_layout.addWidget(self.searx_rb)
        s_layout.addWidget(self._desc("Self-hosted at 127.0.0.1:8888"))
        
        search_group.setLayout(s_layout)
        content_layout.addWidget(search_group)
        
        # RENDERER
        render_group = QGroupBox("Page Renderer")
        r_layout = QVBoxLayout()
        
        self.render_btns = QButtonGroup(self)
        curr_render = self.preferences.get_renderer()
        
        self.text_rb = QRadioButton("Text Only")
        self.text_rb.setChecked(curr_render == "text")
        self.render_btns.addButton(self.text_rb, 0)
        r_layout.addWidget(self.text_rb)
        r_layout.addWidget(self._desc("Maximum privacy, fast"))
        
        self.web_rb = QRadioButton("Web View")
        self.web_rb.setChecked(curr_render == "web")
        self.render_btns.addButton(self.web_rb, 1)
        r_layout.addWidget(self.web_rb)
        r_layout.addWidget(self._desc("Images and CSS, JS disabled"))
        
        warn = QLabel("* Changing renderer requires restart")
        warn.setStyleSheet("color: #f0883e; margin-top: 5px; background: transparent;")
        r_layout.addWidget(warn)
        
        render_group.setLayout(r_layout)
        content_layout.addWidget(render_group)
        
        # Notice
        notice = QLabel("Obscura never saves history or personal data.")
        notice.setWordWrap(True)
        notice.setStyleSheet("background: #1a3326; color: #3fb950; padding: 12px; border-radius: 6px;")
        content_layout.addWidget(notice)
        
        content_layout.addStretch()
        
        container.setLayout(content_layout)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        
        # Button bar (fixed at bottom)
        btn_bar = QWidget()
        btn_bar.setFixedHeight(60)
        btn_bar.setStyleSheet(f"background: {BOX_COLOR}; border-top: 1px solid #30363d;")
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.addStretch()
        
        cancel = QPushButton("Cancel")
        cancel.setFixedWidth(90)
        cancel.clicked.connect(self.reject)
        cancel.setStyleSheet("""
            QPushButton { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; padding: 8px; border-radius: 6px; }
            QPushButton:hover { background: #30363d; }
        """)
        btn_layout.addWidget(cancel)
        
        save = QPushButton("Save")
        save.setFixedWidth(90)
        save.clicked.connect(self.save)
        save.setStyleSheet("""
            QPushButton { background: #238636; color: white; border: none; padding: 8px; border-radius: 6px; }
            QPushButton:hover { background: #2ea043; }
        """)
        btn_layout.addWidget(save)
        
        btn_bar.setLayout(btn_layout)
        main_layout.addWidget(btn_bar)
        
        self.setLayout(main_layout)
        
        # Apply theme
        self.setStyleSheet(f"""
            QDialog {{ background: {BG_COLOR}; }}
            QGroupBox {{ 
                background: {BOX_COLOR}; 
                color: #e6edf3; 
                border: 1px solid #30363d; 
                border-radius: 8px; 
                margin-top: 20px; 
                padding: 15px; 
                padding-top: 25px;
                font-weight: bold;
            }}
            QGroupBox::title {{ 
                subcontrol-origin: margin; 
                subcontrol-position: top left;
                left: 15px; 
                top: 5px;
                padding: 0 8px; 
                background: {BOX_COLOR};
                color: {ACCENT_COLOR};
            }}
            QRadioButton {{ color: #e6edf3; padding: 4px; background: transparent; }}
            QRadioButton::indicator {{ width: 18px; height: 18px; }}
            QRadioButton::indicator:checked {{ background: {ACCENT_COLOR}; border: 2px solid {ACCENT_COLOR}; border-radius: 9px; }}
            QRadioButton::indicator:unchecked {{ background: #21262d; border: 2px solid #484f58; border-radius: 9px; }}
        """)
    
    def _desc(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #8b949e; margin-left: 25px; margin-bottom: 5px; background: transparent;")
        return lbl
    
    def save(self):
        mode = "lite"
        if self.std_rb.isChecked(): mode = "standard"
        elif self.tor_rb.isChecked(): mode = "tor"
        
        engine = "duckduckgo" if self.ddg_rb.isChecked() else "searxng"
        renderer = "text" if self.text_rb.isChecked() else "web"
        
        mode_changed = mode != self.current_mode
        renderer_changed = renderer != self.preferences.get_renderer()
        engine_changed = engine != self.preferences.get_search_engine()
        
        self.preferences.set_privacy_mode(mode)
        self.preferences.set_search_engine(engine)
        self.preferences.set_renderer(renderer)
        self.preferences.save()
        
        if mode_changed:
            self.mode_changed.emit(mode)
        if engine_changed or renderer_changed:
            self.preferences_changed.emit()
        
        if renderer_changed:
            reply = QMessageBox.question(
                self, "Restart Required",
                "Restart Obscura now?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                python = sys.executable
                script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "run.py")
                QProcess.startDetached(python, [script])
                QCoreApplication.quit()
                return
        
        self.accept()

