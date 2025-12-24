# Obscura - Project Structure

> A quick guide to the Obscura codebase

## 📁 Directory Overview

```
Obscura/
├── core/                 # Backend (Privacy Engine)
├── windows_app/          # Frontend (PySide6 UI)
├── installer/            # Windows installer (Inno Setup)
├── tests/                # Development tests
├── .github/              # GitHub templates
├── logs/                 # Runtime logs (gitignored)
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
├── build.bat             # Windows build script
├── obscura.spec          # PyInstaller configuration
├── obscura.ico           # Application icon
└── README.md             # Project documentation
```

---

## 🔒 Core Module (`core/`)

The privacy engine - all security-critical logic lives here.

| File | Purpose |
|------|---------|
| `main.py` | Starts the FastAPI server on localhost:8765 |
| `logging_config.py` | Centralized logging setup |

### `core/api/`
| File | Purpose |
|------|---------|
| `app.py` | FastAPI application with `/search`, `/fetch`, `/mode` endpoints |

### `core/privacy/`
| File | Purpose |
|------|---------|
| `modes.py` | Privacy mode definitions (Lite/Standard/Tor) |
| `js_policy.py` | JavaScript detection and stripping |
| `tor.py` | SOCKS5 proxy configuration for Tor routing |

### `core/proxy/`
| File | Purpose |
|------|---------|
| `fetcher.py` | Page fetching with privacy protections |
| `header_filter.py` | HTTP header sanitization |
| `cookie_stripper.py` | Cookie removal logic |

### `core/search/`
| File | Purpose |
|------|---------|
| `searx_client.py` | DuckDuckGo/SearxNG search client |

---

## 🖥️ Windows App (`windows_app/`)

The user interface - PySide6/Qt application.

| File | Purpose |
|------|---------|
| `app.py` | Application bootstrap and lifecycle |
| `main_window.py` | Main window with tabs and header |
| `core_bridge.py` | HTTP client for Core API communication |

### `windows_app/tabs/`
| File | Purpose |
|------|---------|
| `browser_tab.py` | Browser tab with navigation controls |
| `tab_widget.py` | Custom tab widget styling |

### `windows_app/views/`
| File | Purpose |
|------|---------|
| `search_view.py` | Search results display |
| `page_view.py` | Text-only page renderer |
| `web_view.py` | Qt WebEngine renderer with privacy settings |
| `renderer_factory.py` | Renderer selection logic |

### `windows_app/settings/`
| File | Purpose |
|------|---------|
| `dialog.py` | Settings dialog UI |

### `windows_app/widgets/`
| File | Purpose |
|------|---------|
| `status_badge.py` | Status indicator widgets |

### `windows_app/config/`
| File | Purpose |
|------|---------|
| `preferences.py` | User preferences management |

### `windows_app/utils/`
| File | Purpose |
|------|---------|
| `cache_cleaner.py` | Cache cleanup utilities |

---

## 📦 Installer (`installer/`)

Windows installer files using Inno Setup.

| File | Purpose |
|------|---------|
| `obscura_setup.iss` | Inno Setup script for creating Windows installer |
| `LICENSE.txt` | License file included in installer |
| `README_INSTALLER.txt` | Pre-install information |

---

## 🧪 Tests (`tests/`)

Development and testing utilities.

| File | Purpose |
|------|---------|
| `test_core.py` | Core module import/functionality tests |

---

## 📋 GitHub (`.github/`)

GitHub integration files.

| Folder | Purpose |
|--------|---------|
| `ISSUE_TEMPLATE/` | Bug report and feature request templates |

---

## 📄 Root Files

| File | Purpose |
|------|---------|
| `run.py` | Entry point - run with `python run.py` |
| `version.py` | Version constants |
| `requirements.txt` | Python package dependencies |
| `build.bat` | Windows build script using PyInstaller |
| `obscura.spec` | PyInstaller configuration for single-file EXE |
| `version_info.txt` | Windows EXE version metadata |
| `obscura.ico` | Windows application icon (multi-size) |
| `obscura_icon.png` | Icon source file |
| `.gitignore` | Git ignore rules |
| `LICENSE` | Mozilla Public License 2.0 |
| `README.md` | Project documentation |
| `STRUCTURE.md` | This file - project structure guide |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CODE_OF_CONDUCT.md` | Community code of conduct |
| `KNOWN_ISSUES.md` | Known bugs and planned fixes |
| `SECURITY.md` | Security policy and reporting |
| `THREAT_MODEL.md` | Privacy threat model |
| `CHANGELOG.md` | Version history and release notes |

---

## 🔄 Data Flow

```
User Input → Windows App → Core Bridge → Core API → Internet
                ↑                            ↓
          Sanitized HTML ← Header Filter ← Page Fetcher
```

---

## 🛡️ Privacy Architecture

1. **UI is untrusted** - All privacy logic lives in Core
2. **Core enforces rules** - Privacy settings can't be bypassed
3. **Fail closed** - Errors preserve privacy
4. **No persistence** - Nothing saved between sessions

---

## 📝 License

This project is licensed under the [Mozilla Public License 2.0](LICENSE).
