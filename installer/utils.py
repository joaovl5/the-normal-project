import os
import platform
import zipfile

current_os = platform.system()

host = os.environ.get("NORMAL_HOST", "http://149.28.101.35:5000/")
install_path: str

if current_os == "Windows":
    install_path = os.path.join(os.getenv("APPDATA"), "launchernormal", "app")
else:
    install_path = os.path.join(os.path.expanduser("~"), ".launchernormal", "app")


def _win_make_shortcut(source, dest_dir, dest_name=None, verbose=False):
    import win32com
    from pathlib import Path

    """Make shortcut of `source` path to file in `dest_dir` target folder.
    If `dest_name` is None, will use `source`'s filename.
    """
    # process user input
    if dest_name is None:
        dest_name = Path(source).name
    dest_path = str(Path(dest_dir, dest_name)) + ".lnk"

    # make shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(dest_path)
    shortcut.IconLocation = source
    shortcut.Targetpath = source
    shortcut.save()

    # print status
    if verbose:
        print("{}\n-->\n{}".format(source, dest_path))


def extract_archive(filename):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(install_path)
