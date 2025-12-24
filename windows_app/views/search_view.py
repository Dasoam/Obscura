# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Search Results View - Professional UI with Pagination
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel,
    QFrame, QSizePolicy, QPushButton
)
from PySide6.QtCore import Signal, Qt


class SearchResultCard(QFrame):
    """Modern search result card"""
    
    clicked = Signal(str)
    
    def __init__(self, title: str, url: str, snippet: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.setup_ui(title, url, snippet)
    
    def setup_ui(self, title: str, url: str, snippet: str):
        self.setStyleSheet("""
            SearchResultCard {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 10px;
            }
            SearchResultCard:hover {
                background: #1c2128;
                border-color: #58a6ff;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)
        
        # Title
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #58a6ff; font-size: 15px; font-weight: bold; background: transparent;")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)
        
        # URL
        url_lbl = QLabel(url)
        url_lbl.setStyleSheet("color: #3fb950; font-size: 11px; background: transparent;")
        url_lbl.setWordWrap(True)
        layout.addWidget(url_lbl)
        
        # Snippet
        if snippet:
            snippet_lbl = QLabel(snippet)
            snippet_lbl.setStyleSheet("color: #8b949e; font-size: 13px; background: transparent;")
            snippet_lbl.setWordWrap(True)
            layout.addWidget(snippet_lbl)
        
        self.setLayout(layout)
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        if self.url:
            self.clicked.emit(self.url)


class SearchView(QWidget):
    """Search results view with pagination"""
    
    result_clicked = Signal(str)
    load_more_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_query = ""
        self.all_results = []  # Store all results for appending
        self.load_more_btn = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Scroll area - NO extra padding
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background: #0d1117; padding: 0; margin: 0; }
            QScrollBar:vertical { background: #161b22; width: 10px; }
            QScrollBar::handle:vertical { background: #30363d; border-radius: 5px; min-height: 40px; }
            QScrollBar::handle:vertical:hover { background: #484f58; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        
        # Container - NO padding at top
        self.container = QWidget()
        self.container.setStyleSheet("background: #0d1117; padding: 0; margin: 0;")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.container.setContentsMargins(0, 0, 0, 0)
        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(12, 4, 12, 12)  # Minimal top padding
        self.results_layout.setSpacing(8)
        self.container.setLayout(self.results_layout)
        
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)
        self.setLayout(layout)
        
        self.show_welcome()
    
    def show_welcome(self):
        self.clear()
        self.all_results = []
        
        # Premium welcome card with gradient effect
        welcome = QFrame()
        welcome.setObjectName("welcomeCard")
        welcome.setStyleSheet("""
            QFrame#welcomeCard {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1f2e,
                    stop: 0.5 #161b22,
                    stop: 1 #0d1117
                );
                border: 1px solid #30363d;
                border-radius: 20px;
            }
            QFrame#welcomeCard QLabel {
                border: none;
                background: transparent;
            }
            QFrame#welcomeCard QFrame {
                border: none;
            }
        """)
        
        w_layout = QVBoxLayout()
        w_layout.setContentsMargins(50, 60, 50, 60)
        w_layout.setAlignment(Qt.AlignCenter)
        w_layout.setSpacing(16)
        
        # Glowing icon container
        icon_container = QFrame()
        icon_container.setFixedSize(100, 100)
        icon_container.setStyleSheet("""
            QFrame {
                background: qradialgradient(
                    cx: 0.5, cy: 0.5, radius: 0.5,
                    fx: 0.5, fy: 0.5,
                    stop: 0 rgba(88, 166, 255, 0.3),
                    stop: 0.7 rgba(88, 166, 255, 0.1),
                    stop: 1 transparent
                );
                border: none;
                border-radius: 50px;
            }
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon = QLabel("🔐")
        icon.setStyleSheet("font-size: 48px; background: transparent;")
        icon.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon)
        
        # Center the icon container
        icon_wrapper = QHBoxLayout()
        icon_wrapper.addStretch()
        icon_wrapper.addWidget(icon_container)
        icon_wrapper.addStretch()
        w_layout.addLayout(icon_wrapper)
        
        # Title with gradient-like effect
        title = QLabel("Private Search")
        title.setStyleSheet("""
            color: #58a6ff; 
            font-size: 32px; 
            font-weight: bold; 
            background: transparent;
            letter-spacing: 1px;
        """)
        title.setAlignment(Qt.AlignCenter)
        w_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure • Anonymous • Fast")
        subtitle.setStyleSheet("""
            color: #3fb950; 
            font-size: 13px; 
            font-weight: 600;
            background: transparent;
            letter-spacing: 2px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        w_layout.addWidget(subtitle)
        
        # Spacer
        w_layout.addSpacing(10)
        
        # Description
        desc = QLabel("Search the web without leaving a trace.\nNo tracking. No history. No cookies.")
        desc.setStyleSheet("""
            color: #8b949e; 
            font-size: 15px; 
            background: transparent;
            line-height: 1.8;
        """)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        w_layout.addWidget(desc)
        
        # Feature pills container
        w_layout.addSpacing(20)
        features_layout = QHBoxLayout()
        features_layout.setSpacing(12)
        features_layout.addStretch()
        
        features = [
            ("🛡️", "No Tracking"),
            ("🔒", "Encrypted"),
            ("⚡", "Fast"),
            ("🌐", "Private DNS")
        ]
        
        for emoji, text in features:
            pill = QLabel(f"{emoji} {text}")
            pill.setStyleSheet("""
                color: #c9d1d9;
                background: rgba(48, 54, 61, 0.8);
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            """)
            features_layout.addWidget(pill)
        
        features_layout.addStretch()
        w_layout.addLayout(features_layout)
        
        # Spacer
        w_layout.addSpacing(25)
        
        # Tip with highlight
        tip_container = QFrame()
        tip_container.setStyleSheet("""
            QFrame {
                background: rgba(88, 166, 255, 0.1);
                border: 1px solid rgba(88, 166, 255, 0.3);
                border-radius: 12px;
                padding: 5px;
            }
        """)
        tip_layout = QHBoxLayout(tip_container)
        tip_layout.setContentsMargins(20, 12, 20, 12)
        
        tip = QLabel("💡 Type in the search bar above to get started")
        tip.setStyleSheet("""
            color: #58a6ff; 
            font-size: 14px; 
            background: transparent;
            font-weight: 500;
        """)
        tip.setAlignment(Qt.AlignCenter)
        tip_layout.addWidget(tip)
        
        tip_wrapper = QHBoxLayout()
        tip_wrapper.addStretch()
        tip_wrapper.addWidget(tip_container)
        tip_wrapper.addStretch()
        w_layout.addLayout(tip_wrapper)
        
        welcome.setLayout(w_layout)
        self.results_layout.addWidget(welcome)
    
    def show_results(self, results: list, query: str = "", append: bool = False):
        """Show search results. If append=True, add to existing results."""
        self.current_query = query
        
        if append:
            # Append to existing results
            self.all_results.extend(results)
        else:
            # Clear and show new results
            self.clear()
            self.all_results = results
        
        if not self.all_results:
            self._show_no_results()
            return
        
        # Remove existing Load More button if any
        if self.load_more_btn:
            self.results_layout.removeWidget(self.load_more_btn)
            self.load_more_btn.deleteLater()
            self.load_more_btn = None
        
        # Compact header - inline with no extra space
        if not append:
            header = QLabel(f'🔍 Results for: "{query}"')
            header.setStyleSheet("color: #8b949e; font-size: 11px; background: transparent;")
            header.setFixedHeight(20)
            self.results_layout.addWidget(header)
        
        # Add new result cards (only new ones if appending)
        start_idx = len(self.all_results) - len(results) if append else 0
        for i in range(start_idx, len(self.all_results)):
            r = self.all_results[i]
            card = SearchResultCard(
                r.get("title", "Untitled"),
                r.get("url", ""),
                r.get("snippet", "")
            )
            card.clicked.connect(self.result_clicked.emit)
            self.results_layout.addWidget(card)
        
        # Add Load More button
        self.load_more_btn = QPushButton(f"Load More Results ({len(self.all_results)} loaded)")
        self.load_more_btn.setFixedHeight(44)
        self.load_more_btn.setCursor(Qt.PointingHandCursor)
        self.load_more_btn.clicked.connect(self._on_load_more_clicked)
        self.load_more_btn.setStyleSheet("""
            QPushButton {
                background: #21262d;
                color: #58a6ff;
                border: 1px solid #30363d;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                margin-top: 12px;
            }
            QPushButton:hover {
                background: #30363d;
                border-color: #58a6ff;
            }
            QPushButton:disabled {
                color: #8b949e;
                background: #161b22;
            }
        """)
        self.results_layout.addWidget(self.load_more_btn)
    
    def _on_load_more_clicked(self):
        """Show loading state and emit signal"""
        if self.load_more_btn:
            self.load_more_btn.setText("Loading more results...")
            self.load_more_btn.setEnabled(False)
        self.load_more_clicked.emit()
    
    def append_results(self, results: list):
        """Append more results to existing ones"""
        self.show_results(results, self.current_query, append=True)
    
    def _show_no_results(self):
        no_results = QFrame()
        no_results.setStyleSheet("""
            QFrame {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
            }
        """)
        
        nr_layout = QVBoxLayout()
        nr_layout.setContentsMargins(40, 40, 40, 40)
        nr_layout.setAlignment(Qt.AlignCenter)
        nr_layout.setSpacing(12)
        
        icon = QLabel("🔍")
        icon.setStyleSheet("font-size: 36px; background: transparent;")
        icon.setAlignment(Qt.AlignCenter)
        nr_layout.addWidget(icon)
        
        msg = QLabel("No results found")
        msg.setStyleSheet("color: #c9d1d9; font-size: 18px; font-weight: bold; background: transparent;")
        msg.setAlignment(Qt.AlignCenter)
        nr_layout.addWidget(msg)
        
        tip = QLabel("Try different keywords or check your spelling")
        tip.setStyleSheet("color: #8b949e; font-size: 13px; background: transparent;")
        tip.setAlignment(Qt.AlignCenter)
        nr_layout.addWidget(tip)
        
        no_results.setLayout(nr_layout)
        self.results_layout.addWidget(no_results)
    
    def clear(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.load_more_btn = None
    
    def show_message(self, message: str):
        self.clear()
        
        msg_frame = QFrame()
        msg_frame.setStyleSheet("""
            QFrame {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
            }
        """)
        
        m_layout = QVBoxLayout()
        m_layout.setContentsMargins(40, 60, 40, 60)
        m_layout.setAlignment(Qt.AlignCenter)
        m_layout.setSpacing(16)
        
        spinner = QLabel("⏳")
        spinner.setStyleSheet("font-size: 40px; background: transparent;")
        spinner.setAlignment(Qt.AlignCenter)
        m_layout.addWidget(spinner)
        
        lbl = QLabel(message)
        lbl.setStyleSheet("color: #c9d1d9; font-size: 16px; background: transparent;")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setWordWrap(True)
        m_layout.addWidget(lbl)
        
        msg_frame.setLayout(m_layout)
        self.results_layout.addWidget(msg_frame)

