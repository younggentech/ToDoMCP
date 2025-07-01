import enum
import uuid

from src.domain.exceptions import ExternalServiceException, InvalidParameter
from src.domain.models import User, Task
from src.domain.ports.user_repository import UserRepository

class TaskCommand(enum.Enum):
    """Options to perform with the task."""
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    COMPLETE = "complete"

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, name) -> User:
        """Register a user and store it in repository."""
        user = User(name=name, tasks=[])
        try:
            self.user_repository.save(user)
        except ExternalServiceException as e:
            # todo setup logging
            raise from e
        return user

    def get_user(self, id_: uuid.UUID) -> User | None:
        """Get the user by its ID, if the user does not exist, get None"""
        return self.user_repository.get_by_id(id_)

    def get_tasks(self, user_id: uuid.UUID) -> list[Task] | None:
        """Get all user's tasks"""
        user = self.get_user(user_id)
        if user is None:
            return
        return user.tasks

    def create_task(self, user_id: uuid.UUID, task_data: dict):
        """Add a new task for a user"""
        user = self.get_user(user_id)
        if user is None:
            raise InvalidParameter(f"User with id={user_id} does not exist")
        task = Task(**task_data)
        user.add_task(task)
        self.user_repository.save(user)

    def modify_user_task(self, user_id: uuid.UUID, task_id: uuid.UUID, updates: dict):
        """Update user's task"""
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise InvalidParameter(f"User with id={user_id} does not exist")
        user.update_task(task_id, **updates)
        self.user_repository.save(user)

    def change_task_status(self, user_id: uuid.UUID, task_id: uuid.UUID, cmd: TaskCommand):
        """Change the task's state by using the cmd."""
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise InvalidParameter(f"User with id={user_id} does not exist")
        match cmd:
            case TaskCommand.START:
                user.start_the_task(task_id)
            case TaskCommand.PAUSE:
                user.start_the_task(task_id)
            case TaskCommand.RESUME:
                user.resume_the_task(task_id)
            case TaskCommand.COMPLETE:
                user.complete_the_task(task_id)
        self.user_repository.save(user)
