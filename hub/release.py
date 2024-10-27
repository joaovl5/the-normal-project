from pathlib import Path
from db import DatabaseService, LauncherRelease
import os


class ReleaseService:
    release_folder = "releases"

    def __init__(self) -> None:
        self.db = DatabaseService()

    def latest_release(self) -> str:
        return "normal1_1"

        try:
            version = (
                LauncherRelease.objects().order_by("-version_number")[0].version_name
            )
            return version
        except:
            return "1"

    def get_release(self, version_name: str) -> str:
        version = LauncherRelease.objects(version_name=version_name).first()
        version_location = version.filename
        return version_location, f"r_{version_name}.zip"
