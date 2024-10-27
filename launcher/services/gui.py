import eel
import platform
import webbrowser
import subprocess
import os
import time
from services.utils import electronPath, installPath, closeAll, current_os
from services.version import VersionSystem
from services.config import ConfigSystem


version_system = VersionSystem()
config_system = ConfigSystem()


@eel.expose
def trigger_update():
    # exec = os.path.join(installPath(), "update.exe")
    os.system("update.exe")
    # os.execl(exec, "scragbadun")


@eel.expose
def trigger_quit():
    closeAll()


@eel.expose
def config_dump():
    return config_system.dump()


@eel.expose
def config_get(key):
    return config_system[key]


@eel.expose
def config_set(key, value):
    config_system[key] = value


@eel.expose
def bring_window_to_front():
    current_os = platform.system()
    window_title = "isso é um launcher?"

    if current_os == "Windows":
        import pygetwindow as gw

        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            window = windows[0]
            window.activate()
        else:
            print(f'No window with title "{window_title}" found.')
    elif current_os == "Linux":
        from ewmh import EWMH
        import re

        ewmh = EWMH()
        windows = ewmh.getClientList()
        for win in windows:
            win_name = ewmh.getWmName(win)
            if win_name and re.search(
                window_title, win_name.decode("utf-8"), re.IGNORECASE
            ):
                print(f"Attempting to bring window '{win_name}' to front.")
                ewmh.setActiveWindow(win)
                ewmh.display.flush()
                return True

        print("Window not found.")
        return False

    else:
        print(f"Unsupported operating system: {current_os}")


@eel.expose
def open_url(url):
    webbrowser.open(url)


@eel.expose
def download_version(version_name, callback_name):
    start = time.time()
    print(f"baixando versão {version_name}...")

    js_callback = getattr(eel, callback_name)

    def download_callback(result):
        js_callback(result)
        end = time.time()
        print(f"versão {version_name} baixada... tempo demorado: {str(end - start)}s")

    eel.spawn(
        version_system.download_version_background, version_name, download_callback
    )
    # version_system.download_version_background(version_name, download_callback)
    print("fim fim fim!")


@eel.expose
def start_mine(username, callback_name, memory_allocation, hide_launcher, play_code):
    callback = getattr(eel, callback_name)

    version_system.run_version(
        username, callback, memory_allocation, hide_launcher, start_gui, play_code
    )


@eel.expose
def plog(msg):
    print(msg)


started = False


def start_gui(dev_mode=False):
    global started

    eel.init("web")

    if started == True:
        eel.show_hook()
        return

    started = True
    args = {
        "size": (642 * 1.5, 394 * 1.5),
        "mode": "custom",
        "cmdline_args": [
            electronPath(),
            ".",
        ],
        "port": 9965,
    }

    if dev_mode:
        eel.start(**args)
    else:
        eel.start(**args)
