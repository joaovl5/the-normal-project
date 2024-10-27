import jwt
import os


class AuthenticationService:
    def __init__(self) -> None:
        self.secret = os.getenv("JWT_SECRET")

    def generate_token(self, discord_id) -> str:
        payload = {"discord_id": discord_id}
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token) -> bool:
        try:
            data = jwt.decode(token, self.secret, algorithms="HS256")
            return True
        except jwt.exceptions.InvalidSignatureError:
            return False

    def decode_token(self, token) -> object:
        return jwt.decode(token, self.secret, algorithms="HS256")

    def generate_code(self, player_name) -> str:
        payload = {"player_name": player_name}
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_code(self, code) -> bool:
        try:
            data = jwt.decode(code, self.secret, algorithms="HS256")
            return True
        except jwt.exceptions.InvalidSignatureError:
            return False

    def decode_code(self, code) -> object:
        return jwt.decode(code, self.secret, algorithms="HS256")
