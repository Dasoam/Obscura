# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
QWebEngineView-based Renderer
Normal website rendering with privacy controls
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtCore import QUrl, Signal
import logging

logger = logging.getLogger("Obscura.UI.WebView")


class PrivacyWebPage(QWebEnginePage):
    """Custom web page with privacy settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_privacy()
    
    def setup_privacy(self):
        """Configure privacy settings"""
        settings = self.settings()
        
        # Disable JavaScript by default (max privacy)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        
        # Disable plugins
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        
        # Disable local storage
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        
        # Allow images and CSS for normal rendering
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        
        # Disable geolocation and WebGL
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)
        
        # Disable persistent storage on the profile
        from PySide6.QtWebEngineCore import QWebEngineProfile
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        profile.setPersistentStoragePath("")
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        
        logger.debug("Privacy settings applied: JS disabled, no storage, no plugins, no disk cache")


class WebView(QWidget):
    """Web view renderer with privacy controls"""
    
    url_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_url = ""
        self.setup_ui()
        logger.debug("WebView initialized")
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view with privacy page
        self.web_view = QWebEngineView()
        self.privacy_page = PrivacyWebPage()
        self.web_view.setPage(self.privacy_page)
        
        # Connect signals
        self.web_view.urlChanged.connect(self._on_url_changed)
        
        layout.addWidget(self.web_view)
        self.setLayout(layout)
    
    def _on_url_changed(self, url: QUrl):
        """Handle URL changes"""
        url_str = url.toString()
        if url_str and url_str != "about:blank":
            self.current_url = url_str
            self.url_changed.emit(url_str)
            logger.debug(f"URL changed to: {url_str}")
    
    def load_url(self, url: str):
        """Load a URL"""
        logger.info(f"Loading URL in web view: {url}")
        self.web_view.setUrl(QUrl(url))
        self.current_url = url
    
    def load_html(self, html: str, base_url: str = ""):
        """Load HTML content"""
        logger.info(f"Loading HTML content, length={len(html)}")
        if base_url:
            self.web_view.setHtml(html, QUrl(base_url))
        else:
            self.web_view.setHtml(html)
        self.current_url = base_url
    
    def show_message(self, message: str):
        """Show a simple message"""
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background-color: #1e1e1e;
                    color: #cccccc;
                }}
                h2 {{
                    color: #4a9eff;
                }}
            </style>
        </head>
        <body>
            <h2>{message}</h2>
        </body>
        </html>
        """
        self.web_view.setHtml(html)
    
    def back(self):
        """Navigate back"""
        if self.web_view.history().canGoBack():
            self.web_view.back()
            logger.debug("Navigated back")
    
    def forward(self):
        """Navigate forward"""
        if self.web_view.history().canGoForward():
            self.web_view.forward()
            logger.debug("Navigated forward")
    
    def reload(self):
        """Reload current page"""
        self.web_view.reload()
        logger.debug("Reloaded page")
    
    def can_go_back(self) -> bool:
        """Check if can go back"""
        return self.web_view.history().canGoBack()
    
    def can_go_forward(self) -> bool:
        """Check if can go forward"""
        return self.web_view.history().canGoForward()
    
    def get_title(self) -> str:
        """Get current page title"""
        return self.web_view.title()
    
    def clear(self):
        """Clear the view"""
        logger.debug("Clearing web view")
        self.web_view.setHtml("")
        self.current_url = ""
