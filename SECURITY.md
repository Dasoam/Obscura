# Security Policy

This document describes how to responsibly report security and privacy issues related to **Obscura**.

Obscura is a **local-first, privacy-by-architecture research browser**.  
Security and privacy are treated as core design constraints, not optional features.

---

## Supported Versions

The following versions are currently supported for security fixes:

| Version | Supported |
|-------|-----------|
| 1.0.x | ✅ Yes |


Only the latest stable release receives security updates.

---

## Reporting a Vulnerability

If you believe you have found a **security or privacy vulnerability**, please report it responsibly.

### What to Report

Please report issues related to:
- Privacy leaks (tracking, persistence, unexpected storage)
- Network behavior that contradicts documented guarantees
- Sandbox or isolation failures
- Tor mode misconfiguration or fallback issues
- Accidental telemetry or logging
- Dependency vulnerabilities that affect privacy or security

### What NOT to Report

Please do **not** report:
- Missing features
- Website incompatibility due to JavaScript restrictions
- Expected limitations described in the README or THREAT_MODEL.md
- Issues caused by modified builds or forks

---

## How to Report

### Option 1: GitHub Security Advisory (Recommended)

1. Go to [Security Advisories](https://github.com/Dasoam/Obscura/security/advisories)
2. Click **"New draft security advisory"**
3. Provide details of the vulnerability

### Option 2: GitHub Issue

For non-critical issues, open a [GitHub Issue](https://github.com/Dasoam/Obscura/issues) with the **"security"** label.

---

## Disclosure Policy

- We practice **coordinated disclosure**
- Please allow reasonable time for a fix before public disclosure
- Credit will be given to reporters (unless anonymity is requested)

---

## Security Design

For details on Obscura's security architecture, see:
- [THREAT_MODEL.md](THREAT_MODEL.md) - What we protect against
- [README.md](README.md) 
