# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Obscura Logging Configuration

Provides centralized logging for development and debugging.
File logging is disabled by default for privacy (no disk writes).
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


class ObscuraLogger:
    """
    Centralized logging manager for Obscura.
    
    Console-only by default to maintain privacy.
    File logging can be enabled for development.
    """
    
    _initialized = False
    
    @classmethod
    def setup(cls, log_to_file: bool = False, log_level: str = "INFO"):
        """
        Initialize the Obscura logging system.
        
        Args:
            log_to_file: Enable file logging (creates ./logs/ directory)
            log_level: Logging level - DEBUG, INFO, WARNING, ERROR
        """
        if cls._initialized:
            return
        
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Log format
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler (always enabled)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        
        handlers = [console_handler]
        log_file = None
        
        # File handler (optional - for development only)
        if log_to_file:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"obscura_{timestamp}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        
        # Configure root logger
        logging.basicConfig(level=level, handlers=handlers, force=True)
        
        # Suppress noisy third-party loggers
        for noisy in ['httpx', 'httpcore', 'uvicorn', 'uvicorn.access']:
            logging.getLogger(noisy).setLevel(logging.WARNING)
        
        cls._initialized = True
        
        # Log startup message
        logger = logging.getLogger("Obscura")
        logger.info("=" * 50)
        logger.info("Obscura Started")
        logger.info(f"Log Level: {log_level}")
        if log_file:
            logger.info(f"Log File: {log_file}")
        logger.info("=" * 50)
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a named logger instance.
        
        Args:
            name: Logger name (will be prefixed with 'Obscura.')
            
        Returns:
            Configured Logger instance
        """
        if not cls._initialized:
            cls.setup()
        return logging.getLogger(f"Obscura.{name}")


def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger instance."""
    return ObscuraLogger.get_logger(name)
