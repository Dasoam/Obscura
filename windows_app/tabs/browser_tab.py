# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Browser Tab - Responsive Design
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject, Slot, Qt
import asyncio
import re
import logging

from windows_app.views.renderer_factory import create_page_renderer
from windows_app.views.search_view import SearchView

logger = logging.getLogger("Obscura.UI.BrowserTab")


class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)


class FetchWorker(QRunnable):
    def __init__(self, bridge, url):
        super().__init__()
        self.bridge = bridge
        self.url = url
        self.signals = WorkerSignals()
    
    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.bridge.fetch_page(self.url))
            loop.close()
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))


class SearchWorker(QRunnable):
    def __init__(self, bridge, query, mode):
        super().__init__()
        self.bridge = bridge
        self.query = query
        self.mode = mode
        self.signals = WorkerSignals()
    
    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(self.bridge.search(self.query, self.mode))
            loop.close()
            self.signals.finished.emit(results)
        except Exception as e:
            self.signals.error.emit(str(e))


class BrowserTab(QWidget):
    """Responsive browser tab"""
    
    title_changed = Signal(str)
    
    def __init__(self, bridge, mode="lite", parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self.mode = mode
        self.thread_pool = QThreadPool()
        self.current_url = ""
        self.history = []  # List of tuples: ('url', url_str) or ('search', query_str)
        self.history_index = -1
        
        self.setup_ui()
        self.title_changed.emit("New Tab")
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Navigation bar - responsive
        nav = QWidget()
        nav.setFixedHeight(48)
        nav.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav.setStyleSheet("background: #21262d; border-bottom: 1px solid #30363d;")
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(8, 6, 8, 6)
        nav_layout.setSpacing(4)
        
        btn_css = """
            QPushButton { background: #30363d; color: #c9d1d9; border: none; border-radius: 4px; padding: 6px; min-width: 32px; }
            QPushButton:hover:enabled { background: #484f58; }
            QPushButton:disabled { color: #484f58; }
        """
        
        self.back_btn = QPushButton("<")
        self.back_btn.setFixedSize(32, 32)
        self.back_btn.setEnabled(False)
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setStyleSheet(btn_css)
        nav_layout.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton(">")
        self.forward_btn.setFixedSize(32, 32)
        self.forward_btn.setEnabled(False)
        self.forward_btn.clicked.connect(self.go_forward)
        self.forward_btn.setStyleSheet(btn_css)
        nav_layout.addWidget(self.forward_btn)
        
        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.clicked.connect(self.refresh)
        self.refresh_btn.setStyleSheet(btn_css)
        self.refresh_btn.setToolTip("Refresh")
        nav_layout.addWidget(self.refresh_btn)
        
        home_btn = QPushButton("⌂")
        home_btn.setFixedSize(32, 32)
        home_btn.clicked.connect(self.go_home)
        home_btn.setStyleSheet(btn_css)
        home_btn.setToolTip("Home")
        nav_layout.addWidget(home_btn)
        
        # Address bar - expanding
        self.address = QLineEdit()
        self.address.setPlaceholderText("Search or enter URL...")
        self.address.returnPressed.connect(self.handle_input)
        self.address.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.address.setStyleSheet("""
            QLineEdit { 
                background: #0d1117; color: #c9d1d9; 
                border: 1px solid #30363d; border-radius: 6px; 
                padding: 8px 12px; 
            }
            QLineEdit:focus { border-color: #58a6ff; }
        """)
        nav_layout.addWidget(self.address)
        
        go_btn = QPushButton("Go")
        go_btn.setFixedSize(50, 32)
        go_btn.clicked.connect(self.handle_input)
        go_btn.setStyleSheet("""
            QPushButton { background: #238636; color: white; border: none; border-radius: 4px; }
            QPushButton:hover { background: #2ea043; }
        """)
        nav_layout.addWidget(go_btn)
        
        nav.setLayout(nav_layout)
        layout.addWidget(nav)
        
        # Content stack - NO padding
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.setStyleSheet("background: #0d1117; padding: 0; margin: 0;")
        self.stack.setContentsMargins(0, 0, 0, 0)
        
        self.search_view = SearchView()
        self.search_view.result_clicked.connect(self.load_url)
        self.search_view.load_more_clicked.connect(self._on_load_more)
        self.stack.addWidget(self.search_view)
        
        self.page_view = create_page_renderer()
        if hasattr(self.page_view, 'link_clicked'):
            self.page_view.link_clicked.connect(self.on_link_clicked)
        self.stack.addWidget(self.page_view)
        
        layout.addWidget(self.stack)
        self.setLayout(layout)
        
        # Store current search query
        self.current_query = ""
    
    def handle_input(self):
        text = self.address.text().strip()
        if not text:
            return
        
        if re.match(r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', text):
            self.load_url(text)
        else:
            self.search(text)
    
    def search(self, query: str):
        logger.info(f"Searching: {query}")
        self.current_query = query  # Store for Load More
        
        # Add to history
        history_entry = ('search', query)
        if not self.history or self.history[self.history_index] != history_entry:
            # Truncate forward history if navigating from middle
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(history_entry)
            self.history_index = len(self.history) - 1
        
        self.update_nav()
        self.stack.setCurrentWidget(self.search_view)
        self.search_view.show_message("Searching...")
        self.title_changed.emit(f"Search: {query[:15]}")
        self.address.setText(query)
        
        worker = SearchWorker(self.bridge, query, self.mode)
        worker.signals.finished.connect(self._on_search_done)
        worker.signals.error.connect(self._on_error)
        self.thread_pool.start(worker)
    
    def load_url(self, url: str):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.info(f"Loading: {url}")
        
        # History management
        history_entry = ('url', url)
        if not self.history or self.history[self.history_index] != history_entry:
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(history_entry)
            self.history_index = len(self.history) - 1
        
        self.current_url = url
        self.address.setText(url)
        self.update_nav()
        
        self.stack.setCurrentWidget(self.page_view)
        if hasattr(self.page_view, 'show_message'):
            self.page_view.show_message("Loading...")
        
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            self.title_changed.emit(domain[:18] or "Page")
        except:
            self.title_changed.emit("Page")
        
        worker = FetchWorker(self.bridge, url)
        worker.signals.finished.connect(self._on_page_loaded)
        worker.signals.error.connect(self._on_error)
        self.thread_pool.start(worker)
    
    def on_link_clicked(self, url: str):
        if url.startswith('/'):
            from urllib.parse import urljoin
            url = urljoin(self.current_url, url)
        self.load_url(url)
    
    @Slot(object)
    def _on_search_done(self, results):
        self.search_view.show_results(results, self.current_query)
    
    @Slot(object)
    def _on_more_results(self, results):
        """Append more results to existing ones"""
        self.search_view.append_results(results)
    
    def _on_load_more(self):
        """Handle Load More button - fetch more results and append"""
        if self.current_query:
            logger.info(f"Loading more results for: {self.current_query}")
            worker = SearchWorker(self.bridge, self.current_query, self.mode)
            worker.signals.finished.connect(self._on_more_results)
            worker.signals.error.connect(self._on_error)
            self.thread_pool.start(worker)
    
    @Slot(object)
    def _on_page_loaded(self, data):
        html = data.get("html", "")
        requires_js = data.get("requires_js", False)
        
        if hasattr(self.page_view, 'show_page'):
            self.page_view.show_page(self.current_url, html, requires_js)
        elif hasattr(self.page_view, 'load_html'):
            self.page_view.load_html(html, self.current_url)
    
    @Slot(str)
    def _on_error(self, error):
        logger.error(f"Error: {error}")
        if hasattr(self.page_view, 'show_message'):
            self.page_view.show_message(f"Error: {error}")
    
    def go_home(self):
        self.stack.setCurrentWidget(self.search_view)
        self.search_view.show_welcome()
        self.address.clear()
        self.title_changed.emit("New Tab")
    
    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self._navigate_to_history_entry(self.history[self.history_index])
    
    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._navigate_to_history_entry(self.history[self.history_index])
    
    def _navigate_to_history_entry(self, entry):
        """Navigate to a history entry (either search or URL)"""
        entry_type, value = entry
        self.update_nav()
        
        if entry_type == 'search':
            self.current_query = value
            self.address.setText(value)
            self.stack.setCurrentWidget(self.search_view)
            self.search_view.show_message("Searching...")
            self.title_changed.emit(f"Search: {value[:15]}")
            
            worker = SearchWorker(self.bridge, value, self.mode)
            worker.signals.finished.connect(self._on_search_done)
            worker.signals.error.connect(self._on_error)
            self.thread_pool.start(worker)
        else:
            self.current_url = value
            self.address.setText(value)
            self._fetch_url(value)
    
    def refresh(self):
        if self.history_index >= 0 and self.history_index < len(self.history):
            entry = self.history[self.history_index]
            entry_type, value = entry
            if entry_type == 'url':
                self._fetch_url(value)
            else:
                # Re-run search
                self.search_view.show_message("Searching...")
                worker = SearchWorker(self.bridge, value, self.mode)
                worker.signals.finished.connect(self._on_search_done)
                worker.signals.error.connect(self._on_error)
                self.thread_pool.start(worker)
    
    def _fetch_url(self, url: str):
        self.stack.setCurrentWidget(self.page_view)
        if hasattr(self.page_view, 'show_message'):
            self.page_view.show_message("Loading...")
        
        worker = FetchWorker(self.bridge, url)
        worker.signals.finished.connect(self._on_page_loaded)
        worker.signals.error.connect(self._on_error)
        self.thread_pool.start(worker)
    
    def update_nav(self):
        self.back_btn.setEnabled(self.history_index > 0)
        self.forward_btn.setEnabled(self.history_index < len(self.history) - 1)
