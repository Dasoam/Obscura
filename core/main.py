# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Obscura Core Server Entry Point
Starts the FastAPI server on localhost only
"""

import uvicorn
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup logging - FILE LOGGING DISABLED FOR PRIVACY
from core.logging_config import ObscuraLogger
ObscuraLogger.setup(log_to_file=False, log_level="INFO")  # No file logging in production

import logging
logger = logging.getLogger("Obscura.Core")


def main():
    """Start the Obscura core server"""
    try:
        logger.info("=" * 60)
        logger.info("Starting Obscura Core Server")
        logger.info(f"Project Root: {project_root}")
        logger.info(f"Python Version: {sys.version}")
        logger.info(f"Binding to: 127.0.0.1:8765")
        logger.info("=" * 60)
        
        # Run server on localhost only
        uvicorn.run(
            "core.api.app:app",
            host="127.0.0.1",
            port=8765,
            log_level="warning",  # Minimal logging
            access_log=False,     # No access logging
            server_header=False,  # Don't advertise server
            date_header=False     # Don't send date header
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        # Write error to stderr for debugging
        logger.error(f"Core server error: {e}", exc_info=True)
        print(f"Core server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
