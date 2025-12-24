# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Obscura Windows Application
Main application entry point
"""

import sys
import os

# Suppress Qt OpenType warnings
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.text.font.db=false'

from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont

# Setup logging BEFORE importing other modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.logging_config import ObscuraLogger
ObscuraLogger.setup(log_to_file=False, log_level="INFO")  # No file logging for privacy

import logging
logger = logging.getLogger("Obscura.App")

from windows_app.main_window import MainWindow
from windows_app.core_bridge import CoreBridge
from windows_app.utils.cache_cleaner import cleanup_all


def create_splash_screen():
    """Create a splash screen"""
    logger.debug("Creating splash screen")
    # Create a simple splash screen
    pixmap = QPixmap(400, 300)
    pixmap.fill(QColor("#0a0a0a"))
    
    painter = QPainter(pixmap)
    painter.setPen(QColor("#4a9eff"))
    
    # Draw logo/title
    font = QFont()
    font.setPointSize(24)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "🔒 OBSCURA")
    
    # Draw subtitle
    font.setPointSize(12)
    font.setBold(False)
    painter.setFont(font)
    painter.setPen(QColor("#888888"))
    painter.drawText(50, 180, 300, 30, Qt.AlignCenter, "Privacy-First Research Browser")
    
    # Draw loading message
    font.setPointSize(10)
    painter.setFont(font)
    painter.setPen(QColor("#00ff00"))
    painter.drawText(50, 220, 300, 30, Qt.AlignCenter, "Starting Core...")
    
    painter.end()
    
    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    return splash


def main():
    """Main application entry point"""
    logger.info("="*60)
    logger.info("Obscura Application Starting")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info("="*60)
    
    # Clear cache on startup for fresh module loading
    logger.info("Clearing old cache...")
    cleanup_all()
    
    app = QApplication(sys.argv)
    app.setApplicationName("Obscura")
    app.setOrganizationName("Obscura")
    logger.debug("QApplication initialized")
    
    # Show splash screen
    splash = create_splash_screen()
    splash.show()
    app.processEvents()
    
    # Initialize core bridge
    logger.info("Initializing Core Bridge")
    bridge = CoreBridge()
    
    # Start core server
    splash.showMessage(
        "Starting Core Server...",
        Qt.AlignBottom | Qt.AlignCenter,
        QColor("#00ff00")
    )
    app.processEvents()
    
    logger.info("Starting core server...")
    if not bridge.start_core():
        splash.close()
        logger.critical("Failed to start core server!")
        QMessageBox.critical(
            None,
            "Startup Error",
            "Failed to start Obscura Core.\n\n"
            "Please ensure:\n"
            "• Python is installed\n"
            "• All dependencies are available\n"
            "• Port 8765 is not in use"
        )
        sys.exit(1)
    
    # Create and show main window
    splash.showMessage(
        "Loading Interface...",
        Qt.AlignBottom | Qt.AlignCenter,
        QColor("#00ff00")
    )
    app.processEvents()
    
    logger.info("Creating main window")
    window = MainWindow(bridge)
    window.show()
    logger.info("Main window displayed")
    
    # Close splash
    splash.finish(window)
    logger.debug("Splash screen closed")
    
    logger.info("Application ready - entering main loop")
    # Run application
    result = app.exec()
    
    # Cleanup
    logger.info("Application shutting down...")
    bridge.stop_core()
    logger.info("Core server stopped")
    
    # Clear cache on shutdown
    logger.info("Clearing cache...")
    cleanup_all()
    
    logger.info("Obscura shutdown complete")
    
    sys.exit(result)


if __name__ == "__main__":
    main()
