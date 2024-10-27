from services.utils import currentDir
import os
import pickle


class ConfigSystem:

    _config_object = {
        "access_token": "",
        "installed_version": "",
        "ram": 3,
        "closeLauncher": "1",
    }

    config_dir = os.path.join(currentDir(), "data")
    config_path = os.path.join(config_dir, "cfg")

    def __init__(self) -> None:
        self._load_config()

    def _load_config(self) -> None:
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            self._save_config()
        else:
            file = open(self.config_path, "rb")
            data = file.read()
            file.close()
            self._config_object = pickle.loads(data)

    def _save_config(self) -> None:
        file = open(self.config_path, "wb")
        file.write(pickle.dumps(self._config_object))
        file.close()

    def __getitem__(self, key) -> None:
        return self._config_object.get(key)

    def __setitem__(self, key, value) -> None:
        self._config_object[key] = value
        self._save_config()

    def dump(self):
        return self._config_object
