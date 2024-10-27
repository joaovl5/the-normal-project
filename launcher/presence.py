from threading import Thread
from queue import Queue
from pypresence import Presence
from enum import Enum
import time


class PresenceSignal(Enum):
    SHOW = "show"
    HIDE = "hide"
    RESET_TIMER = "reset_timer"


class DiscordService:
    CLIENT_ID = "1251909768755281961"

    def __init__(self) -> None:
        self.queue = Queue()
        self.thread = Thread(target=self._thread_run, args=(self.queue,))
        self.thread.start()

    def _signal(self, msg: PresenceSignal) -> None:
        self.queue.put(msg)

    def show(self) -> None:
        self._signal(PresenceSignal.SHOW)

    def hide(self) -> None:
        self._signal(PresenceSignal.HIDE)

    def reset_timer(self) -> None:
        self._signal(PresenceSignal.RESET_TIMER)

    def _update_rpc(self, presence: Presence, data: dict[str, any]) -> None:
        print(presence.__repr__(), data.__repr__())
        presence.update(
            large_image="icon",  # name of your asset
            large_text="isso é normal?",
            details=data.get("details"),
            state=data.get("state"),
            start=data.get("start"),
            buttons=[
                {
                    "label": "Entre no Discord",
                    "url": "https://discord.gg/tbSq3WuQxw",
                },
            ],  # up to 2 buttons
        )

    def _thread_run(self, queue: Queue) -> None:
        data = {
            "state": "Launcher aberto",
            "details": "Jogador com launcher aberto!",
            "start": int(time.time()),
        }

        # rpc: Presence
        rpc = Presence(self.CLIENT_ID)
        rpc.connect()

        while True:
            item = queue.get()
            print(item)
            match item:
                case PresenceSignal.SHOW:
                    shown = True
                case PresenceSignal.HIDE:
                    shown = False
                case PresenceSignal.RESET_TIMER:
                    data["start"] = int(time.time())

            if shown:
                self._update_rpc(rpc, data)
            else:
                rpc.clear()


if __name__ == "__main__":
    svc = DiscordService()
    while True:
        svc.show()
        time.sleep(10)
        svc.hide()
        time.sleep(10)
