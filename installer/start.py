import customtkinter
import zipfile
from app import App
from download import DownloadManager
from utils import current_os, host, install_path


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

if __name__ == "__main__":
    app = App()
    app.update()
    manager = DownloadManager(app.update_progress, host=host, install_path=install_path)
    manager.download_latest()
    app.mainloop()
