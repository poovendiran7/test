"""
open_manutd_results.py
Automate: open browser -> search Google for "Manchester United latest results and fixtures" -> open first result.

Notes:
- Default flow uses keyboard navigation (TABs) to reach the first result; adjust TABS_TO_FIRST_RESULT if needed.
- Optional: set CLICK_FIRST_RESULT_COORDS=(x, y) to click a known screen position instead of TABs.
- Press ESC at any input prompt, or move mouse to any screen corner to trigger PyAutoGUI failsafe.
"""

import sys
import time
import pyautogui

# ------------------ SETTINGS (tweak as needed) ------------------

QUERY = "Manchester United latest results and fixtures"

# Choose which browser to launch via OS app search:
# Windows examples: "chrome", "edge", "firefox"
# macOS examples: "Google Chrome", "Safari", "Firefox"
BROWSER_NAME = "edge"   # change to "edge" or "firefox" if you prefer

# How long to wait (in seconds) for things to open/load on your machine/connection:
WAIT_BROWSER_OPEN = 2.5
WAIT_RESULTS_LOAD = 3.5

# Keyboard approach: number of TAB presses from search box to highlight the top organic result.
# (Typical on Google is around 8–12 depending on banners, ads, etc.)
TABS_TO_FIRST_RESULT = 0

# Optional mouse-click fallback: put coordinates here (x, y) to click the first result instead of TAB navigation.
# To discover coordinates, run the helper at the bottom with SHOW_MOUSE_POSITION=True.
CLICK_FIRST_RESULT_COORDS = None  # e.g., (420, 360)  # Set to None to disable

# For debugging your mouse position (prints live coordinates to the console when True)
SHOW_MOUSE_POSITION = False

# ---------------------------------------------------------------

pyautogui.FAILSAFE = True   # move mouse to a corner to abort
pyautogui.PAUSE = 0.12      # small pause after each PyAutoGUI call for stability


def launch_browser(app_name: str):
    """Launch a browser via OS quick search (Start/Spotlight)."""
    platform = sys.platform
    if platform.startswith("win"):
        # Windows: open Start, type app name, Enter
        pyautogui.press("win")
        time.sleep(0.25)
        pyautogui.typewrite(app_name)
        time.sleep(0.25)
        pyautogui.press("enter")
    elif platform == "darwin":
        # macOS: Spotlight, type app name, Enter
        pyautogui.hotkey("command", "space")
        time.sleep(0.25)
        pyautogui.typewrite(app_name)
        time.sleep(0.25)
        pyautogui.press("enter")
    else:
        # Linux (generic): try Super to open launcher (may vary by distro/DE)
        pyautogui.press("win")
        time.sleep(0.25)
        pyautogui.typewrite(app_name)
        time.sleep(0.25)
        pyautogui.press("enter")


def maximize_window_windows():
    """Maximize active window on Windows (safe no-op elsewhere)."""
    if sys.platform.startswith("win"):
        #pyautogui.hotkey("alt", "space")
        time.sleep(0.2)
        #pyautogui.press("x")


def focus_address_bar():
    """Focus the browser address bar (works on all major browsers)."""
    if sys.platform == "darwin":
        pyautogui.hotkey("command", "l")
    else:
        pyautogui.hotkey("ctrl", "l")


def search_google(query: str):
    """Type a Google search into the address bar and go."""
    focus_address_bar()
    time.sleep(0.2)
    pyautogui.typewrite(query)
    pyautogui.press("enter")


def open_first_result_by_tabs(tabs: int):
    """
    From the Google results page, press TAB N times to highlight the top result link,
    then press ENTER to open it. Adjust `tabs` to fit your results layout.
    """
    # Small settle time
    time.sleep(0.4)

    for _ in range(tabs):
        pyautogui.press("tab")
        time.sleep(0.08)

    pyautogui.press("enter")


def open_first_result_by_click(xy):
    """Click specific screen coordinates for the first result."""
    x, y = xy
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()


def show_mouse_position_loop():
    """Utility to help you find coordinates. Press Ctrl+C in the console to stop."""
    print("Showing live mouse position. Press Ctrl+C in the terminal to stop.")
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rMouse position: ({x}, {y})", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    if SHOW_MOUSE_POSITION:
        show_mouse_position_loop()
        return

    # 1) Launch browser
    launch_browser(BROWSER_NAME)
    time.sleep(WAIT_BROWSER_OPEN)
    maximize_window_windows()

    # 2) Search Google
    search_google(QUERY)

    # 3) Wait for results to load
    time.sleep(WAIT_RESULTS_LOAD)

    # 4) Open first result
    if CLICK_FIRST_RESULT_COORDS:
        open_first_result_by_click(CLICK_FIRST_RESULT_COORDS)
    else:
        open_first_result_by_tabs(TABS_TO_FIRST_RESULT)


if __name__ == "__main__":
    main()
