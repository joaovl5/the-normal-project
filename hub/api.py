from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from db import *
import json
import uuid
import urllib.parse
import requests
import os
from dotenv import load_dotenv
from auth import AuthenticationService
from version import VersionService
from release import ReleaseService
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidSignatureError
from starlette.responses import FileResponse

load_dotenv()

api_endpoint = "https://discord.com/api/v10"
client_id = "1251909768755281961"
client_secret = "006Ta7scLoHB8kgdO92KB04_lZVwe087"
redirect_url = "http://149.28.101.35:5000/auth/discord/callback"
# redirect_url = "http://localhost:5000/auth/discord/callback"

app = FastAPI()
db = DatabaseService()
auth = AuthenticationService()
version_service = VersionService()
release_service = ReleaseService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9965", "http://localhost:9965/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_authentication(request: Request, call_next):
    auth_token = request.headers.get("Authorization")

    if (
        request.url.path.startswith("/auth/")
        or request.url.path.startswith("/version/")
        or request.url.path.startswith("/release/")
        or request.url.path.startswith("/code/verify")
        or request.url.path.startswith("/awards")
        or request.url.path.startswith("/news")
        or request.url.path.startswith("/server")
        or (auth_token and auth.verify_token(auth_token))
        or request.method == "OPTIONS"
    ):
        return await call_next(request)
    else:
        return Response("Not authenticated", status_code=403)


@app.get("/")
def read_root():
    return {}


@app.get("/players")
def read_players():
    results = []
    for player in Player.objects:
        results.append(json.loads(player.to_json()))
    return results


@app.get("/awards/{award_id}/icon")
def read_award_icon(award_id: str):
    aw = db.id_to_award(award_id)

    if aw:
        return FileResponse(
            aw.icon,
            media_type="image/png",
        )
    else:
        return Response(status_code=404)


@app.get("/news/{news_id}/{image_id}")
def read_news_image(news_id: str, image_id: str):
    nw = db.id_to_news(news_id)
    if not nw:
        return Response(status_code=404)

    try:
        img = nw.images[int(image_id)]

        return FileResponse(
            img,
            media_type="image/png",
        )
    except:
        return Response(status_code=404)


@app.get("/server/info")
def server_info():
    info = db.get_server_info()
    return {
        "events": info.events_happening,
        "news": (
            [
                f"/news/{info.current_news.id.__str__()}/{index.__str__()}"
                for index, _ in enumerate(info.current_news.images)
            ]
            if hasattr(info, "current_news")
            else []
        ),
    }


@app.get("/players/@me")
def read_player(request: Request):
    token = request.headers.get("Authorization")
    player = db.token_to_player(token)
    return player.serialize()


@app.get("/version/check")
def version_check(request: Request):
    return {"latest": version_service.latest_version()}


@app.get("/release/check")
def release_check(request: Request):
    return {"latest": release_service.latest_release()}


@app.get("/version/{version_name}")
def version_download(version_name: str):
    version_location, version_filename = version_service.get_version(version_name)
    if version_location:
        return FileResponse(
            version_location,
            media_type="application/octet-stream",
            filename=version_filename,
        )
    else:
        return Response(status_code=404)


@app.get("/release/update")
def release_update():
    return FileResponse(
        os.path.join("releases", "update.exe"),
        media_type="application/octet-stream",
    )


@app.get("/release/{version_name}")
def release_download(version_name: str):
    version_location, version_filename = release_service.get_release(version_name)
    if version_location:
        return FileResponse(
            version_location,
            media_type="application/octet-stream",
            filename=version_filename,
        )
    else:
        return Response(status_code=404)


@app.get("/code/generate")
def code_generate(request: Request):
    token = request.headers.get("Authorization")
    player = db.token_to_player(token)
    code = auth.generate_code(player.nickname)
    return {"code": code}


@app.get("/code/verify")
def code_verify(request: Request):
    try:
        code = request.query_params.get("code")
        data = auth.decode_code(code)
        return {"valid": True, "player_name": data.get("player_name")}
    except:
        return {"valid": False}


@app.get("/players/@me/register")
def register_nickname(request: Request):
    token = request.headers.get("Authorization")
    nickname = request.query_params.get("nickname")
    player = db.token_to_player(token)
    db.handle_player_register(player, nickname)
    return "success!"


@app.get("/auth/discord/url")
def make_discord_url():
    state = uuid.uuid4().hex

    generated_url = (
        "https://discord.com/oauth2/authorize?response_type=code&client_id="
        + client_id
        + "&scope=identify&state="
        + state
        + "habn&redirect_uri="
        + urllib.parse.unquote(redirect_url)
        + "&prompt=none&integration_type=0"
    )

    return {"url": generated_url}


@app.get("/auth/discord/callback")
def handle_discord_redirect(request: Request):
    if "error" in request.query_params:
        return "BUG!"

    code = request.query_params.get("code")
    state = request.query_params.get("state")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_url,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        "%s/oauth2/token" % api_endpoint,
        data=data,
        headers=headers,
        auth=(client_id, client_secret),
    ).json()

    if "error" in r:
        return Response(status_code=500)

    access_token = r.get("access_token")
    refresh_token = r.get("refresh_token")
    token_expiration = r.get("expires_in")

    user_data = requests.get(
        f"{api_endpoint}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    token, player_is_new = db.handle_player(
        user_data.get("id"), access_token, refresh_token, token_expiration
    )

    return RedirectResponse(
        url=f"http://localhost:9969/callback?token={token}&new_player={player_is_new}",
        status_code=302,
    )
