from mongoengine import *
from enum import Enum
from datetime import datetime, timedelta
from auth import AuthenticationService
from typing import Optional
import requests
import os
import uuid


class AwardRarity(Enum):
    SECRET = "secret"
    EPIC = "epic"
    RARE = "rare"
    COMMON = "common"
    BAD = "bad"


class AwardRarityScores(Enum):
    secret = 100
    epic = 50
    rare = 30
    common = 10
    bad = 2


class Award(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    rarity = EnumField(enum=AwardRarity, required=True)
    icon = StringField()

    def discord_repr(self) -> str:
        icon = ""
        match self.rarity:
            case AwardRarity.BAD:
                icon = "🤡"
            case AwardRarity.COMMON:
                icon = "🫤"
            case AwardRarity.RARE:
                icon = "😯"
            case AwardRarity.EPIC:
                icon = "🤯"
            case AwardRarity.SECRET:
                icon = "🤩"
        return f"{icon} {self.name}"

    def serialize(self) -> dict[str, any]:
        return {
            "id": self.id.__str__(),
            "name": self.name,
            "description": self.description,
            "rarity": self.rarity,
            "icon": self.icon,
        }


class News(Document):
    images = ListField(StringField())


class ServerInfo(Document):
    events_happening = ListField(StringField())
    current_news = ReferenceField(News)


class Player(Document):
    nickname = StringField()
    discord_id = StringField(required=True)
    access_token = StringField()
    refresh_token = StringField()
    token_expires_in = DateTimeField()
    score = IntField()
    awards = ListField(ReferenceField(Award))

    def serialize(self) -> dict[str, any]:
        return {
            "discord_id": self.discord_id,
            "nickname": self.nickname,
            "score": self.score,
            "awards": [aw.serialize() for aw in self.awards],
        }


class Version(Document):
    filename = StringField(required=True)
    version_number = SequenceField()


class LauncherRelease(Document):
    filename = StringField(required=True)
    version_name = StringField(required=True)
    version_number = SequenceField()


class DatabaseService:

    def __init__(self) -> None:
        connect(host="mongodb://localhost:27017")

        self.auth = AuthenticationService()
        os.makedirs(os.path.join("assets", "awards"), exist_ok=True)
        os.makedirs(os.path.join("assets", "news"), exist_ok=True)
        os.makedirs("versions", exist_ok=True)
        os.makedirs("releases", exist_ok=True)

    def _err(self, msg: str):
        raise Exception(msg)

    def _player_new(self, **kwargs) -> Player:
        return Player(score=0, awards=[], **kwargs)

    def handle_player(
        self,
        discord_id: str,
        access_token: str,
        refresh_token: str,
        token_expiration: int,
    ) -> str:
        print(
            f"DISCORD_ID = {discord_id}\nTOKENS AND EXP: {access_token} {refresh_token} {token_expiration}"
        )
        player = Player.objects(discord_id=str(discord_id)).first()
        expiration_datetime = datetime.now() + timedelta(
            seconds=token_expiration)
        print(f"PLAYER FOUND? {player.__repr__()} is none? {player == None}")
        if player == None:
            new_player = self._player_new(
                discord_id=str(discord_id),
                access_token=access_token,
                refresh_token=refresh_token,
                token_expires_in=expiration_datetime,
            )

            new_player.save()
            # Authenticate new player
            return self.auth.generate_token(str(discord_id)), "1"
        else:
            # Authenticate existing player
            player.access_token = access_token
            player.refresh_token = refresh_token
            player.token_expires_in = expiration_datetime
            player.save()
            return self.auth.generate_token(str(discord_id)), "0"

    def handle_player_register(self, player: Player, nickname: str) -> str:
        player.nickname = nickname
        player.save()

    def token_to_player(self, token: str) -> Player:
        id = self.auth.decode_token(token)["discord_id"]
        return Player.objects(discord_id=id).first()

    def id_to_player(self, id: str) -> Player:
        return Player.objects(discord_id=id).first()

    def id_to_award(self, id: str) -> Award:
        return Award.objects(id=id).first()

    def id_to_news(self, id: str) -> News:
        return News.objects(id=id).first()

    def player_add_award_id(self, player: Player, award_id: str) -> None:
        award = Award.objects(id=award_id).first()
        if not award in player.awards:
            score = AwardRarityScores[award.rarity.value].value
            self.player_add_points(player, score)
            Player.objects(discord_id=player.discord_id).update_one(
                push__awards=award)
        else:
            self._err("Jogador já tem conquista!")

    def player_remove_award_id(self, player: Player, award_id: str) -> None:
        award = Award.objects(id=award_id).first()
        if award in player.awards:
            score = AwardRarityScores[award.rarity.value].value
            self.player_add_points(player, -score)
            Player.objects(discord_id=player.discord_id).update_one(
                pull__awards=award)
        else:
            self._err("Jogador não tem a conquista!")

    def player_add_points(self, player: Player, points: int) -> None:
        player.score += points
        player.save()

    def _find_ext(self, url):
        raw_ext = os.path.splitext(url)[1]
        raw_pos = raw_ext.find("?")
        return raw_ext[:raw_pos] if raw_pos != -1 else raw_ext

    def award_new(self, icon_url: str, **kwargs) -> Award:
        ext = self._find_ext(icon_url)
        path = os.path.join("assets", "awards", f"{uuid.uuid4().hex}{ext}")
        r = requests.get(icon_url)
        with open(path, "wb") as f:
            f.write(r.content)

        return Award(icon=path, **kwargs)

    def award_list(self) -> list[Award]:
        return Award.objects()

    def _download(self, file_url: str, folder: str) -> None:
        r = requests.get(file_url)
        path = os.path.join(folder, f"{uuid.uuid4().hex}.zip")
        f = open(path, "wb")
        f.write(r.content)
        return path

    def version_add(self, file_url):
        path = self._download(file_url, "versions")

        return Version(filename=path)

    def release_add(self, file_url, version):
        path = self._download(file_url, "releases")

        return LauncherRelease(filename=path, version_name=version)

    def _update_events(self, events: list[str]) -> None:
        if len(ServerInfo.objects()) == 0:
            obj = ServerInfo(events_happening=events)
            obj.save()
        else:
            ServerInfo.objects().update(set__events_happening=events)

    def _update_news(self, news: News):
        if len(ServerInfo.objects()) == 0:
            obj = ServerInfo(current_news=news)
            obj.save()
        else:
            ServerInfo.objects().update(set__current_news=news)

    def update_server_info(self,
                           events: Optional[list[str]] = None,
                           news: Optional[News] = None) -> None:
        if events:
            self._update_events(events)

        if news:
            self._update_news(news)

    def news_add(self, image_urls: list[str]) -> News:
        instance = News()
        image_paths = []

        for image_url in image_urls:
            ext = self._find_ext(image_url)
            path = os.path.join("assets", "news", f"{uuid.uuid4().hex}{ext}")
            r = requests.get(image_url)
            with open(path, "wb") as f:
                f.write(r.content)
            image_paths.append(path)

        instance.images.extend(image_paths)
        return instance.save()

    def get_server_info(self) -> ServerInfo:
        if len(ServerInfo.objects()) == 0:
            obj = ServerInfo()
            return obj.save()
        else:
            return ServerInfo.objects[0]
