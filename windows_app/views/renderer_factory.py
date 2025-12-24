# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Renderer Factory
Creates appropriate renderer based on user preferences
"""

from PySide6.QtWidgets import QWidget
import logging

from windows_app.config.preferences import get_preferences

logger = logging.getLogger("Obscura.RendererFactory")


def create_page_renderer(parent=None) -> QWidget:
    """
    Create page renderer based on user preferences
    
    Args:
        parent: Parent widget
        
    Returns:
        Either a PageView (text) or WebView (web engine)
    """
    preferences = get_preferences()
    renderer_type = preferences.get_renderer()
    
    logger.info(f"Creating renderer: {renderer_type}")
    
    if renderer_type == "web":
        try:
            from windows_app.views.web_view import WebView
            logger.info("Using WebView renderer")
            return WebView(parent)
        except ImportError as e:
            logger.error(f"Failed to import WebView: {e}, falling back to text")
            # Fall back to text renderer
            from windows_app.views.page_view import PageView
            return PageView(parent)
    else:
        # Default: text renderer
        from windows_app.views.page_view import PageView
        logger.info("Using PageView (text) renderer")
        return PageView(parent)
