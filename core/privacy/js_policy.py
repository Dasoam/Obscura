# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
JavaScript Policy Enforcement
Controls JavaScript execution based on privacy mode
"""

import re
from typing import Tuple


class JavaScriptPolicy:
    """JavaScript policy enforcer"""
    
    @staticmethod
    def detect_js_requirement(html: str) -> bool:
        """
        Detect if page requires JavaScript
        
        Args:
            html: Page HTML content
            
        Returns:
            True if page likely requires JS
        """
        # Common patterns indicating JS requirement
        js_indicators = [
            r'<noscript>.*please enable javascript.*</noscript>',
            r'<div[^>]*class="[^"]*js-required[^"]*"',
            r'document\.write',
            r'window\.onload',
            r'<script[^>]*src=',
        ]
        
        html_lower = html.lower()
        for pattern in js_indicators:
            if re.search(pattern, html_lower, re.IGNORECASE | re.DOTALL):
                return True
        
        # Check for heavy script usage
        script_count = len(re.findall(r'<script', html_lower))
        return script_count > 5
    
    @staticmethod
    def strip_javascript(html: str) -> str:
        """
        Remove all JavaScript from HTML
        
        Args:
            html: Original HTML
            
        Returns:
            Sanitized HTML without JavaScript
        """
        # Remove script tags and content
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove inline event handlers
        event_handlers = [
            'onclick', 'onload', 'onerror', 'onmouseover', 'onmouseout',
            'onfocus', 'onblur', 'onchange', 'onsubmit', 'onkeydown',
            'onkeyup', 'onkeypress'
        ]
        
        for handler in event_handlers:
            html = re.sub(rf'{handler}="[^"]*"', '', html, flags=re.IGNORECASE)
            html = re.sub(rf"{handler}='[^']*'", '', html, flags=re.IGNORECASE)
        
        # Remove javascript: URLs
        html = re.sub(r'href="javascript:[^"]*"', 'href="#"', html, flags=re.IGNORECASE)
        html = re.sub(r"href='javascript:[^']*'", "href='#'", html, flags=re.IGNORECASE)
        
        return html
    
    @staticmethod
    def process_content(html: str, allow_js: bool) -> Tuple[str, bool]:
        """
        Process HTML content based on JS policy
        
        Args:
            html: Original HTML
            allow_js: Whether JavaScript is allowed
            
        Returns:
            Tuple of (processed_html, requires_js)
        """
        requires_js = JavaScriptPolicy.detect_js_requirement(html)
        
        if not allow_js:
            html = JavaScriptPolicy.strip_javascript(html)
        
        return html, requires_js
