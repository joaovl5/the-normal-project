from portablemc.standard import Version, Context, StreamRunner, XmlStreamEvent
from portablemc.forge import ForgeVersion
from pathlib import Path
from services.utils import minecraftPath, getEnv
from threading import Thread
import os
import requests
import zipfile
import uuid
import glob


class VersionRunner(StreamRunner):
    began_exec = False

    def __init__(self, callback, hide_launcher, show_callback) -> None:
        super().__init__()
        self.callback = callback
        self.hide_launcher = hide_launcher
        self.show_callback = show_callback

    def process_stream_event(self, event: any) -> None:
        if isinstance(event, XmlStreamEvent):
            str_event = repr(event)

            if "Stopping!" in str_event:
                self.callback("close")
                if self.hide_launcher:
                    self.show_callback()
            elif not self.began_exec:
                self.callback("open")
                self.began_exec = True
        else:
            print(f"raw log: {event}")


class VersionSystem:
    HOST = getEnv()["SERVER_HOST"]
    VERSION_FOLDER = minecraftPath()

    def __init__(self) -> None:
        os.makedirs(self.VERSION_FOLDER, exist_ok=True)

    def _archive_path(self, version_name):
        return os.path.join(self.VERSION_FOLDER, f"{version_name}.zip")

    def _download_archive(self, version_name):
        route = f"{self.HOST}/version/{version_name}"
        with requests.get(route, stream=True) as r:
            r.raise_for_status()
            with open(self._archive_path(version_name), "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)

    def _extract_archive(self, version_name):
        with zipfile.ZipFile(self._archive_path(version_name), "r") as zip_ref:
            zip_ref.extractall(self.VERSION_FOLDER)

    def _delete_archive(self, version_name):
        os.remove(self._archive_path(version_name))

    def _delete_mods(self):
        mods_folder = os.path.join(self.VERSION_FOLDER, "mods")
        mods_glob = glob.glob(os.path.join(mods_folder, "*"))
        if os.path.isdir(mods_folder):
            for f in mods_glob:
                os.remove(f)

    def download_version(self, version_name, callback):
        try:
            self._delete_mods()
            self._download_archive(version_name)
            self._extract_archive(version_name)
            self._delete_archive(version_name)
            callback(True)
        except Exception as e:
            import traceback

            print("\n".join(traceback.format_exception(e)))
            callback(False)

    def download_version_background(self, version_name, callback):
        print("Iniciando download no background!")
        from concurrent.futures import ThreadPoolExecutor

        executor = ThreadPoolExecutor(max_workers=2)
        future = executor.submit(self.download_version, version_name, callback)

    def run_version(
        self,
        username,
        callback,
        memory_allocation,
        hide_launcher,
        show_callback,
        play_code,
    ):
        main_path = Path(self.VERSION_FOLDER)
        context = Context(main_dir=main_path, work_dir=main_path)
        self.version = ForgeVersion(
            "1.20.1",
            context=context,
            # _forge_repo="https://maven.neoforged.net/releases/net/neoforged/forge",
        )
        self.version.set_auth_offline(username=username, uuid=uuid.uuid4().__str__())
        self.environment = self.version.install()
        self.environment.jvm_args.extend(
            [
                f"-Xmx{memory_allocation}G",
                f"-Xms{memory_allocation}G",
                f"-Dcode={play_code}",
            ]
        )
        self.environment.game_args.extend(
            [
                f"-Dcode={play_code}",
            ]
        )
        self.environment.run(VersionRunner(callback, hide_launcher, show_callback))

    def run(self):
        pass
