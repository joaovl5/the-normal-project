from pathlib import Path
from db import DatabaseService, Version
import os


class VersionService:
    version_folder = "versions"

    def __init__(self) -> None:
        self.db = DatabaseService()

    def latest_version(self) -> str:
        try:
            version = (
                Version.objects()
                .order_by("-version_number")[0]
                .version_number.__str__()
            )
            print(version)
            return version
        except:
            return "1"

    def get_version(self, version_name: str) -> str:
        version = Version.objects(version_number=int(version_name)).first()
        version_location = version.filename
        return version_location, f"v{version_name}.zip"
