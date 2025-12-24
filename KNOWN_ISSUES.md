# Known Issues

This document tracks known issues that are planned to be addressed in future releases.

## 🐛 Bugs

### 1. "Load More" button shows duplicate results
**Status:** Open  
**Priority:** Medium

**Description:**  
When clicking "Load More" on search results, it loads the same 10 results again instead of the next batch.

**Current Behavior:**  
- Search returns results
- User clicks "Load More"
- Same results are displayed again

**Expected Behavior:**  
- Store all results from API (e.g., 30 results)
- Display first 10 results initially
- On "Load More", display next 10 results
- Hide "Load More" button when all results are shown
- Show "All results loaded" message when exhausted

**Files to modify:**
- `windows_app/views/search_view.py` - UI pagination logic
- `windows_app/tabs/browser_tab.py` - Result storage
- `core/api/app.py` - Optional: pagination support in API

**Technical approach:**
1. Store full result set in browser tab state
2. Track current display offset
3. Slice results array for display: `results[offset:offset+10]`
4. Update offset on "Load More" click
5. Hide button when `offset >= len(results)`

---

### 2. Restart dialog text is hard to see
**Status:** Open  
**Priority:** Low

**Description:**  
When changing the renderer setting, a dialog prompts the user to restart the app. The dialog text is too dark and difficult to read against the dark background.

**Current Behavior:**  
- User changes renderer in Settings
- Restart prompt dialog appears
- Text color is too dark, hard to read

**Expected Behavior:**  
- Dialog text should be clearly visible (light text on dark background)
- Consider using system-default dialog styling for better visibility

**Files to modify:**
- `windows_app/settings/dialog.py` - QMessageBox styling

---

## 💡 Enhancements

*(None currently tracked)*

---

## ✅ Resolved

*(None yet)*
