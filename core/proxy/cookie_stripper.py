# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Cookie Stripper
Removes or filters cookies based on privacy mode
"""

from typing import Dict, Optional


class CookieStripper:
    """Cookie management and removal"""
    
    def __init__(self, allow_session_cookies: bool = False):
        self.allow_session_cookies = allow_session_cookies
        self.session_cookies: Dict[str, str] = {}
    
    def strip_cookies_from_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """
        Remove Set-Cookie headers from response
        
        Args:
            headers: Response headers
            
        Returns:
            Headers without Set-Cookie
        """
        filtered = {}
        for key, value in headers.items():
            if key.lower() not in ['set-cookie', 'set-cookie2']:
                filtered[key] = value
        
        return filtered
    
    def get_cookies_for_request(self, url: str) -> Optional[str]:
        """
        Get cookies to send with request
        
        Args:
            url: Request URL
            
        Returns:
            Cookie header value or None
        """
        if not self.allow_session_cookies:
            return None
        
        # In session mode, return stored session cookies
        if self.session_cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in self.session_cookies.items()])
            return cookie_str
        
        return None
    
    def store_session_cookie(self, name: str, value: str) -> None:
        """
        Store a session cookie (if allowed)
        
        Args:
            name: Cookie name
            value: Cookie value
        """
        if self.allow_session_cookies:
            self.session_cookies[name] = value
    
    def clear_session_cookies(self) -> None:
        """Clear all session cookies"""
        self.session_cookies.clear()
