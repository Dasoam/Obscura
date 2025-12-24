# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
SearxNG Client
Interfaces with local SearxNG instance for private search
Falls back to DuckDuckGo when SearxNG is unavailable or not selected
"""

import httpx
from typing import List, Dict, Any
import logging
from bs4 import BeautifulSoup
import re

logger = logging.getLogger("Obscura.Search")


class SearxNGClient:
    """Client for local SearxNG instance with DuckDuckGo fallback"""
    
    def __init__(self, searxng_url: str = "http://127.0.0.1:8888", force_searxng: bool = False):
        self.searxng_url = searxng_url.rstrip('/')
        self.timeout = 10.0
        self.force_searxng = force_searxng  # If True, use SearxNG; if False, use DuckDuckGo
        self.use_fallback = not force_searxng  # Start with DuckDuckGo unless SearxNG forced
    
    async def search_duckduckgo(self, query: str) -> List[Dict[str, str]]:
        """
        Fallback search using DuckDuckGo HTML
        
        Args:
            query: Search query
            
        Returns:
            List of search results
        """
        logger.info(f"Using DuckDuckGo fallback search for: {query}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                # DuckDuckGo HTML search
                response = await client.get(
                    "https://html.duckduckgo.com/html/",
                    params={"q": query},
                    headers={
                        "User-Agent": "Obscura/1.0",
                        "Accept-Language": "en-US"
                    }
                )
                response.raise_for_status()
                
                # Parse HTML results
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                
                # Find result divs
                result_divs = soup.find_all('div', class_='result')
                
                for div in result_divs[:10]:  # Limit to 10 results
                    try:
                        # Extract title and URL
                        title_elem = div.find('a', class_='result__a')
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        
                        # Extract actual URL from DuckDuckGo redirect
                        if url.startswith('//duckduckgo.com/l/'):
                            # Extract uddg parameter which contains the real URL
                            import urllib.parse
                            parsed = urllib.parse.urlparse('https:' + url)
                            params = urllib.parse.parse_qs(parsed.query)
                            if 'uddg' in params:
                                url = params['uddg'][0]
                        
                        # Ensure URL has proper scheme
                        if url.startswith('//'):
                            url = 'https:' + url
                        elif not url.startswith(('http://', 'https://')):
                            url = 'https://' + url
                        
                        # Extract snippet
                        snippet_elem = div.find('a', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        if title and url:
                            results.append({
                                "title": title,
                                "url": url,
                                "snippet": snippet
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing result: {e}")
                        continue
                
                logger.info(f"DuckDuckGo search returned {len(results)} results")
                
                if not results:
                    return [{
                        "title": "No results found",
                        "url": "",
                        "snippet": f"No results found for '{query}'"
                    }]
                
                return results
                
        except httpx.TimeoutException:
            logger.error("DuckDuckGo search timed out")
            return [{
                "title": "Search Timeout",
                "url": "",
                "snippet": "The search request timed out. Please try again."
            }]
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}", exc_info=True)
            return [{
                "title": "Search Error",
                "url": "",
                "snippet": f"An error occurred while searching: {str(e)}"
            }]
    
    async def search(self, query: str, engines: List[str] = None) -> List[Dict[str, str]]:
        """
        Perform a search via SearxNG or fallback to DuckDuckGo
        
        Args:
            query: Search query
            engines: List of search engines to use (SearxNG only)
            
        Returns:
            List of search results with title, url, snippet
        """
        if not query or not query.strip():
            return []
        
        # Try SearxNG first (if not already marked as unavailable)
        if not self.use_fallback:
            # Default engines if not specified
            if engines is None:
                engines = ["duckduckgo", "bing", "wikipedia"]
            
            # Prepare search parameters
            params = {
                "q": query,
                "format": "json",
                "engines": ",".join(engines)
            }
            
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(
                        f"{self.searxng_url}/search",
                        params=params
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    # Parse results
                    results = []
                    for result in data.get("results", []):
                        results.append({
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "snippet": result.get("content", "")
                        })
                    
                    logger.info(f"SearxNG search returned {len(results)} results")
                    return results
                    
            except httpx.TimeoutException:
                logger.warning("SearxNG timeout, falling back to DuckDuckGo")
                self.use_fallback = True
            except httpx.HTTPError as e:
                logger.warning(f"SearxNG HTTP error: {e}, falling back to DuckDuckGo")
                self.use_fallback = True
            except Exception as e:
                logger.warning(f"SearxNG error: {e}, falling back to DuckDuckGo")
                self.use_fallback = True
        
        # Use DuckDuckGo fallback
        return await self.search_duckduckgo(query)
    
    async def health_check(self) -> bool:
        """
        Check if SearxNG is available
        
        Returns:
            True if SearxNG is responding
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.searxng_url}/")
                return response.status_code == 200
        except Exception:
            return False
