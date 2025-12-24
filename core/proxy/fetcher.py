# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Privacy-Focused HTTP Fetcher
Fetches web pages with privacy protections
"""

import httpx
from typing import Dict, Tuple, Optional
from urllib.parse import urlparse
import re

from core.privacy.modes import PrivacyModeConfig
from core.privacy.js_policy import JavaScriptPolicy
from core.proxy.header_filter import HeaderFilter
from core.proxy.cookie_stripper import CookieStripper


class PageFetcher:
    """Privacy-focused page fetcher"""
    
    def __init__(self, privacy_config: PrivacyModeConfig):
        self.privacy_config = privacy_config
        self.header_filter = HeaderFilter()
        self.cookie_stripper = CookieStripper(
            allow_session_cookies=privacy_config.cookies_enabled()
        )
    
    def validate_url(self, url: str) -> bool:
        """
        Validate URL for safety
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid and safe
        """
        try:
            parsed = urlparse(url)
            # Only allow http and https
            if parsed.scheme not in ['http', 'https']:
                return False
            # Must have a network location
            if not parsed.netloc:
                return False
            return True
        except Exception:
            return False
    
    def sanitize_html(self, html: str) -> str:
        """
        Sanitize HTML content
        
        Args:
            html: Original HTML
            
        Returns:
            Sanitized HTML
        """
        # Remove script tags (if JS disabled)
        if not self.privacy_config.javascript_enabled():
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove iframes
        html = re.sub(r'<iframe[^>]*>.*?</iframe>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove embeds and objects
        html = re.sub(r'<embed[^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<object[^>]*>.*?</object>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove tracking pixels (1x1 images)
        html = re.sub(r'<img[^>]*width=["\']1["\'][^>]*height=["\']1["\'][^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<img[^>]*height=["\']1["\'][^>]*width=["\']1["\'][^>]*>', '', html, flags=re.IGNORECASE)
        
        # Remove images if not allowed
        if not self.privacy_config.images_enabled():
            html = re.sub(r'<img[^>]*>', '[Image removed for privacy]', html, flags=re.IGNORECASE)
        
        return html
    
    async def fetch_page(self, url: str) -> Tuple[str, bool]:
        """
        Fetch and sanitize a web page
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (sanitized_html, requires_js)
        """
        # Validate URL
        if not self.validate_url(url):
            raise ValueError(f"Invalid URL: {url}")
        
        # Prepare headers
        headers = self.header_filter.sanitize_request_headers(
            {}, 
            minimal=self.privacy_config.use_minimal_headers()
        )
        
        # Add cookies if allowed
        cookie_header = self.cookie_stripper.get_cookies_for_request(url)
        if cookie_header:
            headers["Cookie"] = cookie_header
        
        # Get proxy config for Tor mode
        proxy_url = self.privacy_config.get_socks_proxy()
        proxies = {"http://": proxy_url, "https://": proxy_url} if proxy_url else None
        
        # Fetch page
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                max_redirects=5,
                proxies=proxies
            ) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                html = response.text
                
                # Sanitize HTML
                html = self.sanitize_html(html)
                
                # Check JS requirement and process
                processed_html, requires_js = JavaScriptPolicy.process_content(
                    html,
                    allow_js=self.privacy_config.javascript_enabled()
                )
                
                return processed_html, requires_js
                
        except httpx.TimeoutException:
            raise Exception("Request timed out")
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to fetch page: {str(e)}")
