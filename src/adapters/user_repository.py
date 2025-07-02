import json
import sys
import uuid
from json import JSONDecodeError

from src.domain.models import User
from src.domain.ports.user_repository import UserRepository


class JSONUserRepository(UserRepository):
    def __init__(self):
        self.filepath = "/tmp/mcp_per_project_users.json"
        self.users = {}
        self._load_from_disk()

    def save(self, user: User):
        self.users[user.id_] = user
        self._save_on_disk()

    def _save_on_disk(self):
        str_users = {}
        try:
            for uid, user in self.users.items():
                str_users[str(uid)] = user.json()
            with open(self.filepath, "w") as f:
                json.dump(str_users, f)
        except Exception as e:
            print(e, file=sys.stderr)

    def _load_from_disk(self):
        try:
            with open(self.filepath, "r") as f:
                str_users = json.load(f)
            for uid, user in str_users.items():
                self.users[uuid.UUID(uid)] = User.model_validate_json(user)
        except (FileNotFoundError, JSONDecodeError):
            pass


    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.users.get(user_id)
