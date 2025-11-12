import time
import platform

# Detect the current OS
CURRENT_OS = platform.system()

# ---------------------------------------------------------------------
# 🪟 Windows Implementation (using ctypes + SendInput)
# ---------------------------------------------------------------------
if CURRENT_OS == "Windows":
    import ctypes

    SendInput = ctypes.windll.user32.SendInput

    # Key scan codes
    up_pressed = 0x48
    down_pressed = 0x50
    right_pressed = 0x4D
    left_pressed = 0x4B
    space_pressed = 0x39
    a_pressed = 0x1E
    d_pressed = 0x20

    PUL = ctypes.POINTER(ctypes.c_ulong)

    class KeyBdInput(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]

    class HardwareInput(ctypes.Structure):
        _fields_ = [("uMsg", ctypes.c_ulong),
                    ("wParamL", ctypes.c_short),
                    ("wParamH", ctypes.c_ushort)]

    class MouseInput(ctypes.Structure):
        _fields_ = [("dx", ctypes.c_long),
                    ("dy", ctypes.c_long),
                    ("mouseData", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]

    class Input_I(ctypes.Union):
        _fields_ = [("ki", KeyBdInput),
                    ("mi", MouseInput),
                    ("hi", HardwareInput)]

    class Input(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("ii", Input_I)]

    def PressKey(hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def ReleaseKey(hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# ---------------------------------------------------------------------
# 🍎 macOS / 🐧 Linux Implementation (using pynput)
# ---------------------------------------------------------------------
else:
    from pynput.keyboard import Controller, Key

    keyboard = Controller()

    # Human-readable key mappings for convenience
    up_pressed = Key.up
    down_pressed = Key.down
    right_pressed = Key.right
    left_pressed = Key.left
    space_pressed = Key.space
    a_pressed = 'a'
    d_pressed = 'd'

    def PressKey(key):
        """Press a key (works for both string keys and special keys)."""
        try:
            keyboard.press(key)
        except Exception as e:
            print(f"[PressKey Error] {e}")

    def ReleaseKey(key):
        """Release a key."""
        try:
            keyboard.release(key)
        except Exception as e:
            print(f"[ReleaseKey Error] {e}")

# ---------------------------------------------------------------------
# 🔧 Test Mode
# ---------------------------------------------------------------------
if __name__ == '__main__':
    print(f"Running directkeys.py test on {CURRENT_OS}...")
    try:
        # Example: Press and release the 'w' key
        PressKey(a_pressed if CURRENT_OS != "Windows" else 0x1E)
        time.sleep(1)
        ReleaseKey(a_pressed if CURRENT_OS != "Windows" else 0x1E)
        print("✅ Key press test completed successfully.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
