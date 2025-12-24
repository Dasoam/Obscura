# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Core Bridge
Manages communication with the Core API
"""

import httpx
from typing import Dict, List, Any, Optional
import subprocess
import time
import sys
import os
import logging

logger = logging.getLogger("Obscura.CoreBridge")


class CoreBridge:
    """Bridge to Core API"""
    
    def __init__(self, core_url: str = "http://127.0.0.1:8765"):
        self.core_url = core_url.rstrip('/')
        self.core_process: Optional[subprocess.Popen] = None
        self.core_thread = None
        self.timeout = 30.0
        self._server_error = None
    
    def _run_core_server(self):
        """Run core server in thread (for PyInstaller bundle)"""
        try:
            logger.info("Thread starting: importing modules...")
            import asyncio
            import uvicorn
            import sys
            import io
            
            # Fix for PyInstaller: provide dummy streams if stdout/stderr are None
            if sys.stdout is None:
                sys.stdout = io.StringIO()
            if sys.stderr is None:
                sys.stderr = io.StringIO()
            
            logger.info("Thread: importing FastAPI app...")
            from core.api.app import app
            
            logger.info("Thread: creating event loop...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            logger.info("Thread: configuring uvicorn...")
            config = uvicorn.Config(
                app,
                host="127.0.0.1",
                port=8765,
                log_level="warning",
                access_log=False,
                log_config=None,  # Disable uvicorn's logging setup to avoid isatty crash
            )
            server = uvicorn.Server(config)
            
            logger.info("Thread: starting server...")
            loop.run_until_complete(server.serve())
        except Exception as e:
            logger.error(f"Thread crashed: {e}", exc_info=True)
            self._server_error = str(e)
    
    def start_core(self) -> bool:
        """
        Start the Core server process
        
        Returns:
            True if core started successfully
        """
        import threading
        
        try:
            # For PyInstaller bundle, run core in a thread
            if getattr(sys, 'frozen', False):
                logger.info("Running as PyInstaller bundle, starting core in thread...")
                self.core_thread = threading.Thread(target=self._run_core_server, daemon=True)
                self.core_thread.start()
            else:
                # Running as script - use subprocess for development
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                core_main = os.path.join(base_path, "core", "main.py")
                
                if not os.path.exists(core_main):
                    logger.error(f"Core main.py not found at: {core_main}")
                    return False
                
                logger.info(f"Starting core server from: {core_main}")
                
                creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                
                self.core_process = subprocess.Popen(
                    [sys.executable, core_main],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=creationflags,
                    cwd=base_path
                )
            
            logger.info("Waiting for core server to be ready...")
            
            # Wait for core to be ready
            for i in range(20):  # 10 seconds total
                time.sleep(0.5)
                if self.check_health():
                    logger.info("Core server is healthy!")
                    return True
                
                # Check if subprocess died (dev mode only)
                if self.core_process and self.core_process.poll() is not None:
                    stdout, stderr = self.core_process.communicate()
                    logger.error(f"Core process died! STDERR: {stderr.decode('utf-8', errors='ignore')}")
                    return False
            
            logger.error("Core health check timed out")
            return False
            
        except Exception as e:
            print(f"Failed to start core: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def stop_core(self) -> None:
        """Stop the Core server process"""
        if self.core_process:
            try:
                logger.info("Stopping core server...")
                self.core_process.terminate()
                try:
                    # Wait for graceful shutdown
                    self.core_process.wait(timeout=3)
                    logger.info("Core server stopped gracefully")
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't stop
                    logger.warning("Core server didn't stop gracefully, force killing...")
                    self.core_process.kill()
                    self.core_process.wait(timeout=2)
                    logger.info("Core server force killed")
            except Exception as e:
                logger.error(f"Error stopping core: {e}")
                # Last resort - force kill
                if self.core_process:
                    try:
                        self.core_process.kill()
                        logger.info("Core server killed (last resort)")
                    except Exception:
                        pass
    
    def check_health(self) -> bool:
        """
        Check if Core is healthy
        
        Returns:
            True if core is responding
        """
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{self.core_url}/health")
                return response.status_code == 200
        except Exception:
            return False
    
    async def search(self, query: str, mode: str = "lite") -> List[Dict[str, str]]:
        """
        Perform a search
        
        Args:
            query: Search query
            mode: Privacy mode
            
        Returns:
            List of search results
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.core_url}/search",
                    json={"query": query, "mode": mode}
                )
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
        except Exception as e:
            return [{
                "title": "Search Error",
                "url": "",
                "snippet": f"Failed to perform search: {str(e)}"
            }]
    
    async def fetch_page(self, url: str) -> Dict[str, Any]:
        """
        Fetch a web page
        
        Args:
            url: URL to fetch
            
        Returns:
            Page data with html and requires_js flag
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.core_url}/fetch",
                    json={"url": url}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {
                "html": f"<h1>Failed to fetch page</h1><p>{str(e)}</p>",
                "requires_js": False
            }
    
    async def set_mode(self, mode: str) -> bool:
        """
        Set privacy mode
        
        Args:
            mode: Privacy mode (lite/standard/tor)
            
        Returns:
            True if successful
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{self.core_url}/mode",
                    json={"mode": mode}
                )
                response.raise_for_status()
                return True
        except Exception:
            return False
    
    async def get_mode(self) -> str:
        """
        Get current privacy mode
        
        Returns:
            Current mode
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.core_url}/mode")
                response.raise_for_status()
                data = response.json()
                return data.get("mode", "lite")
        except Exception:
            return "lite"
