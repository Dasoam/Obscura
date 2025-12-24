# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
HTTP Header Filter
Sanitizes and normalizes HTTP headers for privacy
"""

from typing import Dict


class HeaderFilter:
    """HTTP header sanitization"""
    
    @staticmethod
    def get_minimal_headers() -> Dict[str, str]:
        """
        Get minimal privacy-focused headers
        
        Returns:
            Minimal header set
        """
        return {
            "User-Agent": "Obscura/1.0",
            "Accept-Language": "en-US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1"
        }
    
    @staticmethod
    def get_standard_headers() -> Dict[str, str]:
        """
        Get standard headers (slightly less restrictive)
        
        Returns:
            Standard header set
        """
        return {
            "User-Agent": "Obscura/1.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        }
    
    @staticmethod
    def filter_response_headers(headers: Dict[str, str]) -> Dict[str, str]:
        """
        Filter response headers to remove tracking
        
        Args:
            headers: Original response headers
            
        Returns:
            Filtered headers
        """
        # Headers to remove for privacy
        blocked_headers = {
            'set-cookie',
            'set-cookie2',
            'x-frame-options',
            'content-security-policy',
            'strict-transport-security',
            'x-xss-protection',
            'x-content-type-options'
        }
        
        filtered = {}
        for key, value in headers.items():
            if key.lower() not in blocked_headers:
                filtered[key] = value
        
        return filtered
    
    @staticmethod
    def sanitize_request_headers(headers: Dict[str, str], minimal: bool = True) -> Dict[str, str]:
        """
        Sanitize outgoing request headers
        
        Args:
            headers: Original headers
            minimal: Use minimal header set
            
        Returns:
            Sanitized headers
        """
        if minimal:
            return HeaderFilter.get_minimal_headers()
        else:
            return HeaderFilter.get_standard_headers()
