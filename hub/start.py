from threading import Thread

import bot
import uvicorn


def start_api():
    config = uvicorn.Config("api:app", port=5000)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":

    api_thread = Thread(target=start_api)
    bot_thread = Thread(target=bot.start_bot)
    api_thread.start()
    bot_thread.start()
