# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
User Preferences Manager
Handles saving and loading user preferences
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger("Obscura.Preferences")


class PreferencesManager:
    """Manages user preferences for Obscura"""
    
    def __init__(self):
        # Preferences file location
        self.config_dir = Path.home() / ".obscura"
        self.config_file = self.config_dir / "preferences.json"
        
        # Default preferences
        self.defaults = {
            "privacy_mode": "lite",
            "search_engine": "duckduckgo",
            "renderer": "text"
        }
        
        self.preferences = self._load()
    
    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load(self) -> Dict[str, Any]:
        """Load preferences from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    prefs = json.load(f)
                    logger.info(f"Loaded preferences: {prefs}")
                    # Merge with defaults for any missing keys
                    return {**self.defaults, **prefs}
            else:
                logger.info("No preferences file found, using defaults")
                return self.defaults.copy()
        except Exception as e:
            logger.error(f"Error loading preferences: {e}", exc_info=True)
            return self.defaults.copy()
    
    def save(self):
        """Save preferences to file"""
        try:
            self._ensure_config_dir()
            with open(self.config_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
            logger.info(f"Saved preferences: {self.preferences}")
        except Exception as e:
            logger.error(f"Error saving preferences: {e}", exc_info=True)
    
    def get(self, key: str, default=None) -> Any:
        """Get a preference value"""
        return self.preferences.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a preference value"""
        self.preferences[key] = value
        logger.debug(f"Updated preference: {key} = {value}")
    
    def get_privacy_mode(self) -> str:
        """Get current privacy mode"""
        return self.get("privacy_mode", "lite")
    
    def set_privacy_mode(self, mode: str):
        """Set privacy mode"""
        if mode not in ["lite", "standard", "tor"]:
            raise ValueError(f"Invalid privacy mode: {mode}")
        self.set("privacy_mode", mode)
    
    def get_search_engine(self) -> str:
        """Get current search engine"""
        return self.get("search_engine", "duckduckgo")
    
    def set_search_engine(self, engine: str):
        """Set search engine"""
        if engine not in ["duckduckgo", "searxng"]:
            raise ValueError(f"Invalid search engine: {engine}")
        self.set("search_engine", engine)
    
    def get_renderer(self) -> str:
        """Get current renderer"""
        return self.get("renderer", "text")
    
    def set_renderer(self, renderer: str):
        """Set renderer"""
        if renderer not in ["text", "web"]:
            raise ValueError(f"Invalid renderer: {renderer}")
        self.set("renderer", renderer)
    
    def requires_restart(self, key: str) -> bool:
        """Check if changing this preference requires restart"""
        restart_keys = ["renderer"]
        return key in restart_keys


# Global instance
_preferences = None

def get_preferences() -> PreferencesManager:
    """Get global preferences instance"""
    global _preferences
    if _preferences is None:
        _preferences = PreferencesManager()
    return _preferences
