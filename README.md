# 🔒 OBSCURA

**Privacy-First Research Browser for Windows**

Obscura is a local-first, privacy-by-architecture research browser that runs entirely on your machine with **zero telemetry**, **zero tracking**, and **zero data collection**.

---

## 🎯 What is Obscura?

Obscura is **NOT** a replacement for Chrome, Firefox, or Edge. It is a **private search and reading tool** designed for:

- 🔍 **Private research** without tracking
- 📚 **Reading web content** without ads or JavaScript bloat
- 🛡️ **Maximum privacy** with no compromises

### Core Principles

✅ **100% Local** - No servers, no backend, no accounts  
✅ **Zero Data Collection** - No history, no cookies, no logs  
✅ **Privacy by Architecture** - Privacy rules enforced at the core level  
✅ **Transparent** - Full control over privacy settings  

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** (64-bit)
- **Python 3.11+** (for development/building)
- **SearxNG** (optional, for search functionality)

### Installation

#### Option 1: Run from Source (Development)

1. **Clone or download** this repository

2. **Install dependencies** (assuming venv is already created):
   ```bash
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

#### Option 2: Build Standalone EXE

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script**:
   ```bash
   build.bat
   ```

3. **Find the executable** in `dist/Obscura.exe`

4. **Run** `Obscura.exe` - no installation required!

---

## 📖 How to Use

### Basic Usage

1. **Launch Obscura** - The application will start the privacy-protected core automatically

2. **Search or Browse**:
   - **Search**: Type your query in the address bar and press Enter
   - **Visit URL**: Enter a full URL (e.g., `https://example.com`)

3. **View Results**:
   - Click on search results to view pages
   - Use the back button (←) to return to search results

4. **Adjust Privacy Settings**:
   - Click the ⚙ **Settings** button
   - Choose your privacy mode (see below)

### Privacy Modes

#### 🟢 Lite (Default - Maximum Privacy)
- ❌ JavaScript **disabled**
- ❌ Cookies **blocked**
- ❌ Images **removed**
- ✅ Minimal headers (maximum anonymity)

**Use when**: You want maximum privacy and don't need interactive content.

#### 🟡 Standard (Balanced)
- ⚠️ Limited JavaScript **allowed**
- 🍪 Session cookies only (cleared on exit)
- 🖼️ Images **allowed**
- ✅ Standard headers

**Use when**: You need to view modern websites with some interactivity.

#### 🔴 Tor (Maximum Anonymity)
- 🧅 All traffic routed through **Tor network**
- ❌ JavaScript **disabled**
- ❌ Cookies **blocked**
- ✅ Aggressive header stripping

**Use when**: You need maximum anonymity and are willing to sacrifice speed.  
**Requires**: Tor running locally on `127.0.0.1:9050`

---

## 🛠️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────┐
│      Windows UI (PySide6)          │
│  ┌──────────────────────────────┐  │
│  │  • Main Window               │  │
│  │  • Search/Address Bar        │  │
│  │  • Search Results View       │  │
│  │  • Page Content View         │  │
│  │  • Settings Dialog           │  │
│  └──────────────────────────────┘  │
│               ↕ HTTP               │
│      (localhost only: 127.0.0.1)   │
└─────────────────────────────────────┘
                 ↕
┌─────────────────────────────────────┐
│     Privacy Core (FastAPI)         │
│  ┌──────────────────────────────┐  │
│  │  • Privacy Mode Controller   │  │
│  │  • SearxNG Client            │  │
│  │  • HTTP Fetcher              │  │
│  │  • Content Sanitizer         │  │
│  │  • Header Filter             │  │
│  │  • Cookie Stripper           │  │
│  │  • JavaScript Policy         │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
                 ↕
         Internet (via proxy)
```

### Technology Stack

**Core Backend:**
- **Python 3.11+**
- **FastAPI** - Local API server (127.0.0.1 only)
- **httpx** - HTTP client with SOCKS5 support
- **uvicorn** - ASGI server

**Windows UI:**
- **PySide6** - Qt for Python
- **QTextBrowser** - Content rendering (no JavaScript by default)

**Packaging:**
- **PyInstaller** - Single EXE distribution

---

## 🔐 Privacy Guarantees

### What Obscura NEVER Does

❌ **No Telemetry** - Zero analytics or usage tracking  
❌ **No Logging** - Searches and URLs are never logged  
❌ **No History** - Nothing is saved to disk  
❌ **No Cookies** - No persistent cookies (session only in Standard mode)  
❌ **No Identifiers** - No user accounts or device fingerprinting  
❌ **No Background Calls** - Only explicit user actions trigger network requests  
❌ **No Central Servers** - Everything runs locally  

### What Gets Stored

The ONLY thing Obscura stores:
- ✅ **User Preferences** in `~/.obscura/preferences.json`
  - Privacy mode (lite/standard/tor)
  - Search engine (duckduckgo/searxng)
  - Renderer type (text/web)

**No browsing data is ever saved** - everything is cleared when you close the app.

---

## 📁 Project Structure

```
Obscura/
├── core/                          # Privacy-protected backend
│   ├── main.py                    # Core server entry point
│   ├── logging_config.py         # Centralized logging
│   ├── api/
│   │   └── app.py                 # FastAPI application
│   ├── search/
│   │   └── searx_client.py        # Search (DDG + SearxNG)
│   ├── proxy/
│   │   ├── fetcher.py             # HTTP page fetcher
│   │   ├── header_filter.py       # Header sanitization
│   │   └── cookie_stripper.py     # Cookie management
│   ├── privacy/
│   │   ├── modes.py               # Privacy modes
│   │   ├── js_policy.py           # JavaScript policy
│   │   └── tor.py                 # Tor routing
│   └── config/
│       └── defaults.yaml          # Default configuration
│
├── windows_app/                   # Windows UI
│   ├── app.py                     # Application entry point
│   ├── main_window.py             # Main window with tabs
│   ├── core_bridge.py             # Core API client
│   ├── config/
│   │   └── preferences.py         # User preferences manager
│   ├── tabs/
│   │   ├── browser_tab.py         # Browser tab widget
│   │   └── tab_widget.py          # Tab container
│   ├── views/
│   │   ├── search_view.py         # Search results UI
│   │   ├── page_view.py           # Text content view
│   │   ├── web_view.py            # WebEngine view
│   │   └── renderer_factory.py    # Renderer selection
│   ├── widgets/
│   │   └── status_badge.py        # Status indicators
│   ├── settings/
│   │   └── dialog.py              # Settings dialog
│   └── utils/
│       └── cache_cleaner.py       # Cache cleanup
│
├── installer/                     # Windows installer files
│   ├── obscura_setup.iss          # Inno Setup script
│   └── LICENSE.txt
│
├── .github/                       # GitHub templates
│   └── ISSUE_TEMPLATE/
│
├── requirements.txt               # Python dependencies
├── obscura.spec                   # PyInstaller configuration
├── build.bat                      # Build script
├── run.py                         # Development runner
└── README.md                      # This file
```

---

## 🔧 Advanced Configuration

### Search Engines

Obscura supports two search engines:

#### DuckDuckGo (Default)
- **Works out of the box** - no setup required
- Uses DuckDuckGo's HTML interface for privacy
- No tracking, no JavaScript required

#### SearxNG (Optional)
- Self-hosted metasearch engine
- Even more private than DuckDuckGo
- Requires local installation

To use SearxNG:
1. **Install SearxNG** following the [official guide](https://docs.searxng.org/)
2. **Run SearxNG** on `http://127.0.0.1:8888`
3. **Select SearxNG** in Obscura Settings

### Using Tor Mode

To use Tor mode:

1. **Install Tor Browser** or **Tor service**

2. **Configure Tor** to run a SOCKS5 proxy on `127.0.0.1:9050`

3. **Select Tor mode** in Obscura settings

4. All traffic will be routed through Tor

---

## 🐛 Troubleshooting

### Core Server Won't Start

**Problem**: "Failed to start Obscura Core"

**Solutions**:
- Ensure **port 8765** is not in use by another application
- Check that Python 3.11+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Search Not Working

**Problem**: "SearxNG Not Available"

**Solutions**:
- Install and run **SearxNG** on `http://127.0.0.1:8888`
- Check SearxNG logs for errors
- Test SearxNG directly in a browser: `http://127.0.0.1:8888`

### Pages Show "Requires JavaScript" Warning

**Problem**: Page content is broken or blank

**Solutions**:
- Click **"Continue Read-Only"** to view text content
- Switch to **Standard mode** in Settings to enable JavaScript
- Click **"Open in External Browser"** for full functionality

### Tor Mode Not Working

**Problem**: "Connection failed" in Tor mode

**Solutions**:
- Ensure Tor is running on `127.0.0.1:9050`
- Test Tor connection independently
- Check Tor logs for errors

---

## 🚫 Explicit Non-Goals

Obscura is designed for privacy-first research. It does **NOT** include:

❌ User accounts or sync  
❌ Browser extensions  
❌ Password manager  
❌ Autofill  
❌ Bookmarks (to prevent tracking)  
❌ Advertisements  
❌ Analytics or metrics  

If you need these features, use a traditional browser.

---

## 📜 License

This project is provided as-is for educational and privacy research purposes.

---

## 🤝 Contributing

Contributions are welcome! Please ensure any changes:

1. ✅ **Maintain privacy guarantees** - No telemetry, logging, or tracking
2. ✅ **Follow architecture** - Privacy logic stays in Core
3. ✅ **Are well-documented** - Update README and code comments
4. ✅ **Pass testing** - Ensure no privacy leaks

---

## 📞 Support

For issues, questions, or suggestions:

1. **Check the Troubleshooting section** above
2. **Check Known Issues**: `KNOWN_ISSUES.md`
3. **Open an issue** on GitHub with detailed information

---

## ⚠️ Important Notes

### This is a Privacy Tool, Not a Daily Browser

- Obscura is **not designed** for social media, streaming, or complex web apps
- Many modern sites **require JavaScript** and will not work in Lite mode
- Use **Standard mode** for better compatibility (with reduced privacy)
- For maximum compatibility, use an external browser

### Privacy vs. Functionality Trade-off

The more privacy you want, the fewer sites will work correctly:

- **Lite Mode** = Maximum privacy, minimal compatibility
- **Standard Mode** = Balanced privacy and compatibility
- **Tor Mode** = Maximum anonymity, slowest speed

Choose the mode that best fits your needs for each browsing session.

---

## 🎉 Acknowledgments

Built with:
- **FastAPI** - Modern Python web framework
- **PySide6** - Qt for Python
- **httpx** - Advanced HTTP client
- **SearxNG** - Privacy-respecting metasearch engine
- **PyInstaller** - Python to executable

---

**Made with ❤️ for privacy advocates and security researchers**

🔒 **Your privacy is not for sale. Your data stays on your machine.**
