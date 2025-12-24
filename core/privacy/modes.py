# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Privacy Modes Manager
Enforces privacy settings for different browsing modes
"""

from enum import Enum
from typing import Dict, Any


class PrivacyMode(str, Enum):
    """Privacy mode enumeration"""
    LITE = "lite"
    STANDARD = "standard"
    TOR = "tor"


class PrivacyModeConfig:
    """Privacy mode configuration"""
    
    def __init__(self):
        self.current_mode = PrivacyMode.LITE
        
    def get_mode(self) -> PrivacyMode:
        """Get current privacy mode"""
        return self.current_mode
    
    def set_mode(self, mode: str) -> None:
        """Set privacy mode"""
        if mode not in [m.value for m in PrivacyMode]:
            raise ValueError(f"Invalid privacy mode: {mode}")
        self.current_mode = PrivacyMode(mode)
    
    def get_config(self) -> Dict[str, Any]:
        """Get configuration for current mode"""
        configs = {
            PrivacyMode.LITE: {
                "javascript": False,
                "cookies": False,
                "images": False,
                "headers_minimal": True,
                "socks_proxy": None
            },
            PrivacyMode.STANDARD: {
                "javascript": True,
                "cookies": True,
                "images": True,
                "headers_minimal": False,
                "socks_proxy": None
            },
            PrivacyMode.TOR: {
                "javascript": False,
                "cookies": False,
                "images": False,
                "headers_minimal": True,
                "socks_proxy": "socks5://127.0.0.1:9050"
            }
        }
        return configs[self.current_mode]
    
    def javascript_enabled(self) -> bool:
        """Check if JavaScript is enabled for current mode"""
        return self.get_config()["javascript"]
    
    def cookies_enabled(self) -> bool:
        """Check if cookies are enabled for current mode"""
        return self.get_config()["cookies"]
    
    def images_enabled(self) -> bool:
        """Check if images are enabled for current mode"""
        return self.get_config()["images"]
    
    def use_minimal_headers(self) -> bool:
        """Check if minimal headers should be used"""
        return self.get_config()["headers_minimal"]
    
    def get_socks_proxy(self) -> str | None:
        """Get SOCKS proxy URL if applicable"""
        return self.get_config()["socks_proxy"]
