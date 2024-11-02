import sys

# Windows-specific imports
if sys.platform == "win32":
    import ctypes
# macOS-specific imports
elif sys.platform == "darwin":
    from Quartz import CGEventSourceKeyState, kCGEventSourceStateHIDSystemState
# Linux-specific imports
elif sys.platform.startswith("linux"):
    from Xlib.display import Display

def is_capslock_on():
    """Check if Caps Lock is on, cross-platform."""
    # Windows
    if sys.platform == "win32":
        hll_dll = ctypes.WinDLL("User32.dll")
        return hll_dll.GetKeyState(0x14) == 1
    # macOS
    elif sys.platform == "darwin":
        return CGEventSourceKeyState(kCGEventSourceStateHIDSystemState, 57)
    # Linux
    elif sys.platform.startswith("linux"):
        display = Display()
        return display.get_keyboard_control().led_mask & 1 != 0
    # Unsupported OS
    else:
        raise OSError("Unsupported operating system for checking Caps Lock status.")

# Usage example
if __name__ == "__main__":
    if is_capslock_on():
        print("Caps Lock is ON")
    else:
        print("Caps Lock is OFF")
