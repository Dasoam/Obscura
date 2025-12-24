# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Tab Widget
Manages individual tabs with page content
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
import logging

logger = logging.getLogger("Obscura.UI.Tab")


class TabWidget(QWidget):
    """Individual tab containing a page renderer"""
    
    title_changed = Signal(str)  # Emitted when tab title changes
    
    def __init__(self, renderer, parent=None):
        super().__init__(parent)
        self.renderer = renderer
        self.tab_title = "New Tab"
        
        # Setup layout
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.renderer)
        self.setLayout(layout)
        
        # Connect signals if renderer supports them
        if hasattr(self.renderer, 'url_changed'):
            self.renderer.url_changed.connect(self._on_url_changed)
        
        logger.debug("Tab widget created")
    
    def _on_url_changed(self, url: str):
        """Handle URL changes to update title"""
        # Extract domain from URL for title
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            title = parsed.netloc or url[:30]
            self.set_title(title)
        except:
            self.set_title(url[:30] if url else "")
    
    def set_title(self, title: str):
        """Set tab title"""
        self.tab_title = title or "New Tab"
        self.title_changed.emit(self.tab_title)
        logger.debug(f"Tab title set to: {self.tab_title}")
    
    def get_title(self) -> str:
        """Get tab title"""
        return self.tab_title
    
    def get_renderer(self):
        """Get the renderer widget"""
        return self.renderer
