"""
test Core Server
Quick test to verify the core server can start
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

try:
    print("\n1. Testing imports...")
    from core.api.app import app
    print("   ✓ FastAPI app imported successfully")
    
    from core.privacy.modes import PrivacyModeConfig
    print("   ✓ Privacy modes imported successfully")
    
    from core.search.searx_client import SearxNGClient
    print("   ✓ SearxNG client imported successfully")
    
    from core.proxy.fetcher import PageFetcher
    print("   ✓ Page fetcher imported successfully")
    
    print("\n2. Testing privacy config...")
    config = PrivacyModeConfig()
    print(f"   ✓ Default mode: {config.get_mode()}")
    
    print("\n3. Testing FastAPI app...")
    print(f"   ✓ App title: {app.title}")
    print(f"   ✓ Routes: {[route.path for route in app.routes]}")
    
    print("\n✅ All tests passed! Core is ready to start.")
    print("\nTo run the core server directly:")
    print("   python core/main.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
