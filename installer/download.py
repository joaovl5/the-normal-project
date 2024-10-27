import uuid
import threading
import shutil
import requests
import os
import tempfile
from utils import current_os, extract_archive, _win_make_shortcut


class DownloadManager:
    def __init__(self, progress_callback, host, install_path) -> None:
        self.progress_callback = progress_callback
        self.host = host
        self.install_path = install_path

    def _download_file(
        self, url: str, filename: str, callback, download_finished_callback
    ) -> None:
        self._download_progress(url, filename, callback, download_finished_callback)

    def _get_percentage(self, value, total):
        return value / total

    def _download_progress(self, url, filepath, callback, download_finished_callback):
        response = requests.get(url, stream=True)

        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024 * 1024

        with open(filepath, "wb") as file:
            volume = 0
            for data in response.iter_content(block_size):
                volume += len(data)
                percent = self._get_percentage(volume, total_size)
                file.write(data)
                callback(percent)
        download_finished_callback()

    def _get_temp_file(self) -> str:
        return os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)

    def get_latest(self) -> str:
        url = f"{self.host}release/check"
        res = requests.get(url).json()
        return res.get("latest")

    def get_already_instaled(self) -> bool:
        return os.path.exists(self.install_path)

    def prune_old_version(self) -> None:
        for item in os.listdir(self.install_path):
            item_path = os.path.join(self.install_path, item)
            if item != "minecraft":
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                except:
                    pass

    def download_installer(self) -> None:
        url = f"{self.host}release/update"
        response = requests.get(url, stream=True)
        filepath = os.path.join(
            self.install_path, "update" + (".exe" if current_os == "Windows" else "")
        )

        with open(filepath, "wb") as file:
            for data in response.iter_content(1024 * 1024):
                file.write(data)

    def make_shortcuts(self, path) -> None:
        if current_os == "Windows":
            desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            _win_make_shortcut(path, desktop)
        else:
            pass  # fazer coiso pra linux!!!

    def download_latest(self):
        try:
            url = f"{self.host}{self.get_latest()}"
            name = self._get_temp_file()

            print(f"Usando a url {url}")

            if self.get_already_instaled():
                print("detectado versão já instalada! apagando versão anterior...")
                self.prune_old_version()

            def download_finished_callback() -> None:
                print("extraindo...")
                extract_archive(name)
                print("baixando última versão do atualizador...")
                self.download_installer()
                print("saindo e abrindo launcher...")
                exec = os.path.join(self.install_path, "start.exe")
                self.make_shortcuts(os.path.join(self.install_path, "start.exe"))
                os.system(exec)
                os._exit(0)

            self.downloader_thread = threading.Thread(
                target=self._download_file,
                args=(url, name, self.progress_callback, download_finished_callback),
            )
            self.downloader_thread.start()
        except requests.exceptions.ConnectionError:
            print("Não foi possível conectar ao servidor!")
