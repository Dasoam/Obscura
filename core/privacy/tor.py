# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Tor Routing Support
Handles SOCKS5 proxy configuration for Tor
"""

from typing import Dict, Optional


class TorRouter:
    """Tor SOCKS5 proxy manager"""
    
    def __init__(self, socks_url: str = "socks5://127.0.0.1:9050"):
        self.socks_url = socks_url
        self.enabled = False
    
    def enable(self) -> None:
        """Enable Tor routing"""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable Tor routing"""
        self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check if Tor routing is enabled"""
        return self.enabled
    
    def get_proxy_config(self) -> Optional[Dict[str, str]]:
        """
        Get proxy configuration for httpx
        
        Returns:
            Proxy configuration dict or None
        """
        if not self.enabled:
            return None
        
        return {
            "http://": self.socks_url,
            "https://": self.socks_url
        }
    
    def get_headers(self) -> Dict[str, str]:
        """
        Get Tor-specific headers
        
        Returns:
            Minimal headers for Tor mode
        """
        return {
            "User-Agent": "Obscura/1.0",
            "Accept-Language": "en-US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
