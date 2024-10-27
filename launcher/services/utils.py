import sys
import platform
from os.path import join, expanduser, dirname, abspath
from os import getenv, _exit
from dotenv import dotenv_values
import psutil


current_os = platform.system()


def isBundled() -> bool:
    return getattr(sys, "bundled")


def electronPath() -> str:
    if not isBundled():
        return "node_modules/electron/dist/electron"

    if current_os == "Windows":
        return join("bin", "launchernormal.exe")
    else:
        return join("bin", "launchernormal")


def installPath() -> str:
    if current_os == "Windows":
        return join(getenv("APPDATA"), "launchernormal", "app")
    else:
        return join(expanduser("~"), ".launchernormal", "app")


def minecraftPath() -> str:
    if current_os == "Windows":
        return join(getenv("APPDATA"), "launchernormal", "minecraft")
    else:
        return join(expanduser("~"), ".launchernormal", "minecraft")


def closeAll() -> None:
    for proc in psutil.process_iter():
        if proc.name() in ["launchernormal", "launchernormal.exe", "start.exe"]:
            proc.kill()

    _exit(0)


def currentDir() -> str:
    return dirname(abspath(sys.argv[0]))


def getEnv() -> dict:
    return dotenv_values(".env")
