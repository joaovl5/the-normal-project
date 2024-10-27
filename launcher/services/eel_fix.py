import sys
import io

dev_mode = "--dev" in sys.argv
bundled = hasattr(sys, "frozen")

if not dev_mode:
    sys.stderr = open("logs.txt", "+a")
    sys.stdout = open("logs.txt", "+a")

# fixes eel trying to join paths with sys._MEIPASS, which does not exist without pyinstaller
setattr(sys, "bundled", bundled)
if bundled:
    delattr(sys, "frozen")
