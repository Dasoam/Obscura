# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Main Window - Responsive Design
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
import asyncio
import logging
import os
import sys

from windows_app.tabs.browser_tab import BrowserTab
from windows_app.settings.dialog import SettingsDialog
from windows_app.core_bridge import CoreBridge
from windows_app.config.preferences import get_preferences
from windows_app.widgets.status_badge import StatusBadge

logger = logging.getLogger("Obscura.UI.MainWindow")


class MainWindow(QMainWindow):
    """Responsive main window"""
    
    def __init__(self, bridge: CoreBridge):
        super().__init__()
        self.bridge = bridge
        self.preferences = get_preferences()
        self.current_mode = self.preferences.get_privacy_mode()
        logger.info("MainWindow initializing...")
        self.setup_ui()
        logger.info("MainWindow initialized")
    
    def setup_ui(self):
        self.setWindowTitle("Obscura - Privacy Browser")
        self.setMinimumSize(800, 600)
        self.resize(1280, 800)
        
        # Set window icon
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        icon_path = os.path.join(base_path, "obscura.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            logger.debug(f"Window icon set from: {icon_path}")
        else:
            # Try PNG as fallback
            png_path = os.path.join(base_path, "obscura_icon.png")
            if os.path.exists(png_path):
                self.setWindowIcon(QIcon(png_path))
                logger.debug(f"Window icon set from: {png_path}")
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header - responsive
        header = QWidget()
        header.setFixedHeight(50)
        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header.setStyleSheet("background: #010409; border-bottom: 1px solid #21262d;")
        
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(15, 0, 15, 0)
        h_layout.setSpacing(10)
        
        # Logo
        logo = QLabel("OBSCURA")
        logo.setStyleSheet("color: #58a6ff; font-weight: bold;")
        h_layout.addWidget(logo)
        
        h_layout.addStretch()
        
        # Mode badge
        self.mode_badge = StatusBadge(
            icon="🛡️",
            label="Mode",
            value=self.current_mode.upper(),
            accent_color="#3fb950"
        )
        h_layout.addWidget(self.mode_badge)
        
        # Renderer badge
        renderer = self.preferences.get_renderer()
        self.renderer_badge = StatusBadge(
            icon="🖥️",
            label="Renderer",
            value="TEXT" if renderer == "text" else "WEB",
            accent_color="#f0883e"
        )
        h_layout.addWidget(self.renderer_badge)
        
        # Search badge
        engine = self.preferences.get_search_engine()
        self.engine_badge = StatusBadge(
            icon="🔍",
            label="Search",
            value="DDG" if engine == "duckduckgo" else "SearxNG",
            accent_color="#58a6ff"
        )
        h_layout.addWidget(self.engine_badge)
        
        # New Tab
        new_btn = QPushButton("+ Tab")
        new_btn.clicked.connect(self.new_tab)
        new_btn.setStyleSheet("""
            QPushButton { background: #238636; color: white; border: none; padding: 6px 12px; border-radius: 4px; }
            QPushButton:hover { background: #2ea043; }
        """)
        h_layout.addWidget(new_btn)
        
        # Settings
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.show_settings)
        settings_btn.setStyleSheet("""
            QPushButton { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; padding: 6px 12px; border-radius: 4px; }
            QPushButton:hover { background: #30363d; }
        """)
        h_layout.addWidget(settings_btn)
        
        header.setLayout(h_layout)
        layout.addWidget(header)
        
        # Tabs - expanding
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: #0d1117; }
            QTabBar { background: #161b22; }
            QTabBar::tab { 
                background: #21262d; color: #8b949e; 
                padding: 10px 20px; margin-right: 1px;
                border-top-left-radius: 6px; border-top-right-radius: 6px;
                min-width: 100px;
            }
            QTabBar::tab:selected { background: #0d1117; color: #c9d1d9; }
            QTabBar::tab:hover:!selected { background: #30363d; }
            QTabBar::close-button { image: none; }
            QTabBar::close-button:hover { background: #f85149; border-radius: 2px; }
        """)
        layout.addWidget(self.tabs)
        
        # Footer with UX guardrail and version
        try:
            from version import __version__
            version_text = f" • v{__version__}"
        except ImportError:
            version_text = ""
        footer = QLabel(f"🔒 Obscura{version_text} — Optimized for research and reading. It is not intended for account-based services.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            color: #484f58; 
            font-size: 11px; 
            padding: 6px;
            background: #010409;
            border-top: 1px solid #21262d;
        """)
        footer.setFixedHeight(28)
        layout.addWidget(footer)
        
        central.setLayout(layout)
        self.setStyleSheet("QMainWindow { background: #0d1117; }")
        
        # First tab
        self.new_tab()
    
    def new_tab(self):
        tab = BrowserTab(self.bridge, self.current_mode)
        tab.title_changed.connect(lambda t: self.update_tab_title(tab, t))
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        return tab
    
    def close_tab(self, index: int):
        if self.tabs.count() <= 1:
            return
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        widget.deleteLater()
    
    def update_tab_title(self, tab: BrowserTab, title: str):
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, title[:20] + "..." if len(title) > 20 else title)
    
    def show_settings(self):
        dialog = SettingsDialog(self.current_mode, self)
        dialog.mode_changed.connect(self.on_mode_changed)
        dialog.preferences_changed.connect(self.on_prefs_changed)
        dialog.exec()
    
    @Slot(str)
    def on_mode_changed(self, mode: str):
        self.current_mode = mode
        self.mode_badge.set_value(mode.upper())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.bridge.set_mode(mode))
        loop.close()
    
    @Slot()
    def on_prefs_changed(self):
        prefs = get_preferences()
        renderer = prefs.get_renderer()
        engine = prefs.get_search_engine()
        self.renderer_badge.set_value("TEXT" if renderer == "text" else "WEB")
        self.engine_badge.set_value("DDG" if engine == "duckduckgo" else "SearxNG")

