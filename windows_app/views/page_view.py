# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Page Content View - Responsive Design
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser, QLabel,
    QPushButton, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import logging

logger = logging.getLogger("Obscura.UI.PageView")


class PageView(QWidget):
    """Page content view - responsive text browser"""
    
    link_clicked = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_url = ""
        self.history = []
        self.history_index = -1
        self.setup_ui()
        logger.debug("PageView initialized")
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Warning banner
        self.warning = QWidget()
        self.warning.setStyleSheet("""
            QWidget { background: #3d2804; border-bottom: 2px solid #f0883e; }
        """)
        self.warning.setFixedHeight(60)
        
        warn_layout = QHBoxLayout()
        warn_layout.setContentsMargins(15, 10, 15, 10)
        
        warn_text = QLabel("This site may require JavaScript. Showing text content only.")
        warn_text.setStyleSheet("color: #f0883e;")
        warn_text.setWordWrap(True)
        warn_layout.addWidget(warn_text)
        
        warn_layout.addStretch()
        
        external_btn = QPushButton("Open in Browser")
        external_btn.clicked.connect(self.open_external)
        external_btn.setStyleSheet("""
            QPushButton { background: #1f6feb; color: white; border: none; padding: 6px 12px; border-radius: 4px; }
            QPushButton:hover { background: #388bfd; }
        """)
        warn_layout.addWidget(external_btn)
        
        self.warning.setLayout(warn_layout)
        self.warning.hide()
        layout.addWidget(self.warning)
        
        # Text browser (main content) - DARK THEME
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(False)
        self.browser.anchorClicked.connect(self._on_link_clicked)
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.browser.setStyleSheet("""
            QTextBrowser {
                background: #1a1a1a;
                color: #e0e0e0;
                border: none;
                padding: 20px;
            }
            QScrollBar:vertical { background: #2a2a2a; width: 12px; }
            QScrollBar::handle:vertical { background: #505050; border-radius: 6px; min-height: 30px; }
        """)
        layout.addWidget(self.browser)
        
        self.setLayout(layout)
    
    def _on_link_clicked(self, url):
        url_str = url.toString()
        logger.debug(f"Link clicked: {url_str}")
        self.link_clicked.emit(url_str)
    
    def show_page(self, url: str, html: str, requires_js: bool = False):
        logger.info(f"Showing page: {url}, requires_js={requires_js}")
        self.current_url = url
        
        # Add to history
        if self.history_index == -1 or (self.history and self.history[self.history_index] != url):
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(url)
            self.history_index = len(self.history) - 1
        
        # Show warning if JS required
        self.warning.setVisible(requires_js)
        
        # Display content
        self.browser.setHtml(html)
    
    def show_message(self, message: str):
        self.warning.hide()
        self.browser.setHtml(f"""
            <html>
            <body style="background:#0d1117; color:#c9d1d9; padding:40px; text-align:center;">
                <h2 style="color:#58a6ff;">{message}</h2>
            </body>
            </html>
        """)
    
    def open_external(self):
        if self.current_url:
            QDesktopServices.openUrl(QUrl(self.current_url))
    
    def back(self):
        if self.can_go_back():
            self.history_index -= 1
            return self.history[self.history_index]
        return None
    
    def forward(self):
        if self.can_go_forward():
            self.history_index += 1
            return self.history[self.history_index]
        return None
    
    def can_go_back(self) -> bool:
        return self.history_index > 0
    
    def can_go_forward(self) -> bool:
        return self.history_index < len(self.history) - 1
    
    def clear(self):
        self.browser.clear()
        self.warning.hide()
        self.current_url = ""
