import uuid
from abc import ABC, abstractmethod

from src.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        """Save user into the persistant storage."""
        ...

    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Get the user by id or None is user does not exist."""
        ...
