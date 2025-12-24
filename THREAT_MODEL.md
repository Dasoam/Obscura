# Obscura – Threat Model

**Version:** 1.0  
**Last Updated:** December 2024

This document defines **what Obscura protects against, what it does not protect against, and why**.

It exists to:

* Set correct user expectations
* Prevent misuse
* Make privacy claims verifiable and honest
* Guide future development decisions

If a proposed feature violates this threat model, it **must not be added**.

---

## 1. Scope & Philosophy

Obscura is a **local-first, privacy-by-architecture research browser**.

It is designed to protect users during:

* Searching
* Reading
* Researching
* Learning

It is **not** designed to support:

* Persistent identities
* Account-based services
* Personalized web applications

Obscura prioritizes **anti-surveillance and anti-profiling**, not universal anonymity.

---

## 2. Assets We Protect

Obscura is built to protect the following user assets:

### 2.1 Search Intent

* What users search for
* Topics they explore
* Questions they ask

Search intent is considered **highly sensitive**.

### 2.2 Reading Behavior

* Which pages are opened
* What content is read
* What links are clicked

Obscura prevents persistent tracking of reading behavior.

### 2.3 Browser Identity

* Cookies
* Local storage
* Fingerprinting vectors
* Long-lived identifiers

Obscura removes or disables these by design.

---

## 3. Adversary Model

Obscura assumes the following adversaries:

### 3.1 Websites

**Capabilities:**
* Attempt to fingerprint browsers
* Use trackers, scripts, and cookies
* Correlate visits over time

**Mitigations:**
* Script stripping
* Cookie removal
* Header normalization
* No persistent storage

### 3.2 Search Engines

**Capabilities:**
* Log queries
* Build user profiles
* Personalize results

**Mitigations:**
* Use of DuckDuckGo or local SearxNG
* No query history
* No personalization

### 3.3 Network Observers

**Capabilities:**
* Observe IP address
* Monitor traffic volume

**Mitigations:**
* Optional Tor mode

**Limitations:**
* IP is **not hidden by default**

### 3.4 Obscura Itself

**Capabilities:**
* Full access to browsing data

**Mitigations:**
* No servers
* No logging
* No telemetry
* Local execution only

Trust is enforced by architecture, not promises.

---

## 4. Out-of-Scope Threats

Obscura does **NOT** protect against:

### 4.1 IP Address Exposure (Default Mode)

* Websites and search engines can see the user's IP address
* This is intentional
* Users may enable Tor mode for IP anonymity

### 4.2 Malicious Endpoints

* Obscura cannot protect against malicious content hosted on a site
* It does not sandbox OS-level exploits

### 4.3 Logged-in Identity Correlation

* If a user logs into an account, identity is revealed to that service
* Obscura discourages account-based usage

### 4.4 Device-Level Compromise

* Malware on the user's system
* Compromised operating system

These are outside Obscura's control.

---

## 5. Design Trade-offs

### 5.1 No Default IP Anonymity

**Reason:**
* Avoid central servers
* Avoid trust assumptions
* Preserve performance

**Trade-off:**
* IP visible unless Tor is enabled

### 5.2 JavaScript Disabled by Default

**Reason:**
* JavaScript enables tracking and fingerprinting

**Trade-off:**
* Some modern sites may not function

Users may explicitly relax this per session.

### 5.3 No Persistence

**Reason:**
* Prevent long-term profiling

**Trade-off:**
* No saved logins or history

---

## 6. Security Boundaries

```
┌─────────────────┐
│   Windows UI    │  → Untrusted (displays only)
└────────┬────────┘
         │ HTTP (localhost only)
┌────────▼────────┐
│  Obscura Core   │  → Trusted (enforces privacy)
└────────┬────────┘
         │
┌────────▼────────┐
│    Internet     │  → Hostile (assumed adversarial)
└─────────────────┘
```

All privacy enforcement happens in Core. The UI cannot bypass privacy rules.

---

## 7. Data Storage

| Data Type | Stored? | Location |
|-----------|---------|----------|
| User preferences | ✅ Yes | `~/.obscura/preferences.json` |
| Browsing history | ❌ No | Never saved |
| Cookies | ❌ No | Never saved |
| Search queries | ❌ No | Never saved |
| Cache | ❌ No | Cleared on exit |

---

## 8. Failure Modes

If any component fails:

* Obscura must fail **closed**
* Privacy must be preserved over usability

Examples:

* If Tor is unavailable → Tor mode cannot start
* If sanitization fails → Page not rendered
* If Core crashes → UI cannot bypass to fetch directly

---

## 9. User Responsibility

Users are responsible for:

* Enabling Tor mode when IP anonymity is required
* Not using Obscura for sensitive account logins
* Understanding the limitations described here

---

## 10. Non-Goals

Obscura intentionally does NOT aim to:

* Replace general-purpose browsers
* Support social media or web apps
* Provide absolute anonymity by default
* Compete with Tor Browser for high-risk use cases

---

## 11. Summary

Obscura protects **what you think about**, not **who you are**.

It removes surveillance from searching and reading while remaining honest about its limits.

---

> **If a feature contradicts this threat model, it must not be implemented.**
