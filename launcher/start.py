from services.eel_fix import dev_mode 
import eel
from flask import Flask, request
import threading
from services.gui import start_gui


app = Flask(__name__)


@app.route("/callback")
def login_callback():
    token = request.args.get("token")
    player_is_new = request.args.get("new_player") == "1"
    eel.handle_login(token, player_is_new)
    return "Logado! Já pode fechar essa janela"


def run_server(flask_app):
    flask_app.run(port=9969)


if __name__ == "__main__":
    app_thread = threading.Thread(target=run_server, args=(app,))
    app_thread.start()
    start_gui(dev_mode)
