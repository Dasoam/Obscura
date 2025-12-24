# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Cache Cleanup Utilities
Handles cleanup of Python cache and other temporary files
"""

import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger("Obscura.CacheCleanup")


def clear_python_cache(base_path: str = None):
    """
    Clear all Python __pycache__ directories
    
    Args:
        base_path: Base path to search from (defaults to current directory)
    """
    if base_path is None:
        base_path = os.getcwd()
    
    base_path = Path(base_path)
    logger.info(f"Clearing Python cache from: {base_path}")
    
    deleted_count = 0
    
    try:
        # Find all __pycache__ directories
        for pycache_dir in base_path.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                deleted_count += 1
                logger.debug(f"Deleted: {pycache_dir}")
            except Exception as e:
                logger.warning(f"Failed to delete {pycache_dir}: {e}")
        
        # Find all .pyc files
        for pyc_file in base_path.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                deleted_count += 1
                logger.debug(f"Deleted: {pyc_file}")
            except Exception as e:
                logger.warning(f"Failed to delete {pyc_file}: {e}")
        
        logger.info(f"Cache cleared: {deleted_count} items deleted")
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}", exc_info=True)


def clear_webengine_cache():
    """Clear QtWebEngine cache directory"""
    try:
        # QtWebEngine cache location
        cache_dir = Path.home() / ".QtWebEngine"
        
        if cache_dir.exists():
            logger.info(f"Clearing WebEngine cache: {cache_dir}")
            shutil.rmtree(cache_dir, ignore_errors=True)
            logger.info("WebEngine cache cleared")
        else:
            logger.debug("No WebEngine cache found")
            
    except Exception as e:
        logger.warning(f"Failed to clear WebEngine cache: {e}")


def cleanup_all(base_path: str = None):
    """
    Perform complete cleanup of all caches
    
    Args:
        base_path: Base path for Python cache cleanup
    """
    logger.info("Starting complete cache cleanup...")
    clear_python_cache(base_path)
    clear_webengine_cache()
    logger.info("Cache cleanup complete")
