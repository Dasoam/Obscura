# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Obscura Core API
FastAPI application providing privacy-focused search and fetch services
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging
import sys
import os

from core.privacy.modes import PrivacyModeConfig, PrivacyMode
from core.search.searx_client import SearxNGClient
from core.proxy.fetcher import PageFetcher

# Add parent directory to path if needed for importing preferences
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

try:
    from windows_app.config.preferences import PreferencesManager
    HAS_PREFERENCES = True
except ImportError as e:
    HAS_PREFERENCES = False
    print(f"[Core API] Could not import preferences: {e}")

# Get logger
logger = logging.getLogger("Obscura.API")


# Request/Response models
class SearchRequest(BaseModel):
    query: str
    mode: str = "lite"


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class SearchResponse(BaseModel):
    results: List[SearchResult]


class FetchRequest(BaseModel):
    url: str


class FetchResponse(BaseModel):
    html: str
    requires_js: bool


class ModeRequest(BaseModel):
    mode: str


class HealthResponse(BaseModel):
    status: str


# Create FastAPI app
app = FastAPI(
    title="Obscura Core API",
    description="Privacy-focused search and fetch API",
    version="1.0.0",
    docs_url=None,  # Disable docs for privacy
    redoc_url=None   # Disable redoc for privacy
)

# Global state
privacy_config = PrivacyModeConfig()


def get_search_client() -> SearxNGClient:
    """Get search client based on current preferences"""
    use_searxng = False
    
    if HAS_PREFERENCES:
        try:
            # Create new instance to reload from disk (Core runs as separate process)
            prefs = PreferencesManager()
            engine = prefs.get_search_engine()
            use_searxng = (engine == "searxng")
            logger.info(f"Search engine from preferences: {engine}, use_searxng={use_searxng}")
        except Exception as e:
            logger.warning(f"Could not read preferences: {e}, defaulting to DDG")
    else:
        logger.info("HAS_PREFERENCES is False, defaulting to DDG")
    
    return SearxNGClient(force_searxng=use_searxng)


logger.info(f"FastAPI app initialized. HAS_PREFERENCES={HAS_PREFERENCES}")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Perform a search
    
    Args:
        request: Search request with query and mode
        
    Returns:
        Search results
    """
    try:
        logger.info(f"Search request: query='{request.query}', mode='{request.mode}'")
        
        # Set privacy mode
        if request.mode:
            privacy_config.set_mode(request.mode)
            logger.debug(f"Privacy mode set to: {request.mode}")
        
        # Get search client based on current preferences
        searx_client = get_search_client()
        
        # Perform search
        logger.debug("Calling search client...")
        results = await searx_client.search(request.query)
        logger.info(f"Search completed: {len(results)} results")
        
        # Convert to response format
        search_results = [
            SearchResult(
                title=r["title"],
                url=r["url"],
                snippet=r["snippet"]
            )
            for r in results
        ]
        
        return SearchResponse(results=search_results)
        
    except ValueError as e:
        logger.error(f"Search validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        # Don't leak error details
        raise HTTPException(status_code=500, detail="Search failed")


@app.post("/fetch", response_model=FetchResponse)
async def fetch_page(request: FetchRequest):
    """
    Fetch and sanitize a web page
    
    Args:
        request: Fetch request with URL
        
    Returns:
        Sanitized HTML and JS requirement flag
    """
    try:
        logger.info(f"Fetch request: url='{request.url}'")
        
        # Create fetcher with current privacy config
        fetcher = PageFetcher(privacy_config)
        
        # Fetch and process page
        logger.debug("Fetching page...")
        html, requires_js = await fetcher.fetch_page(request.url)
        logger.info(f"Fetch completed: requires_js={requires_js}, html_length={len(html)}")
        
        return FetchResponse(
            html=html,
            requires_js=requires_js
        )
        
    except ValueError as e:
        logger.error(f"Fetch validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Fetch failed: {e}", exc_info=True)
        # Don't leak error details
        raise HTTPException(status_code=500, detail="Fetch failed")


@app.post("/mode")
async def set_mode(request: ModeRequest):
    """
    Set privacy mode
    
    Args:
        request: Mode request
        
    Returns:
        Success confirmation
    """
    try:
        logger.info(f"Mode change request: {request.mode}")
        privacy_config.set_mode(request.mode)
        logger.info(f"Privacy mode changed to: {request.mode}")
        return {"status": "ok", "mode": request.mode}
    except ValueError as e:
        logger.error(f"Invalid mode: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/mode")
async def get_mode():
    """
    Get current privacy mode
    
    Returns:
        Current mode
    """
    current_mode = privacy_config.get_mode().value
    logger.debug(f"Mode query: current mode is {current_mode}")
    return {"mode": current_mode}
