import datetime
import uuid

from pydantic import BaseModel, Field

from src.domain.exceptions import InvalidParameter


class WorkInterval(BaseModel):
    """
    Interval of working on a particular task.
    """
    task_id: uuid.UUID
    start: datetime.datetime | None = None
    end: datetime.datetime | None = None


class Task(BaseModel):
    """
    A task consists of:
     - name
     - is_complete indicating if the task was finished
     - optional description
     - optional deadline
     - a list of working intervals to calculate the time for working on a task.
    """
    id_: uuid.UUID  = Field(default_factory=uuid.uuid4, alias="id")
    name: str
    is_complete: bool = False
    description: str | None = None
    deadline: datetime.datetime | None = None
    intervals: list[WorkInterval] = Field(default_factory=list)


class User(BaseModel):
    """
    System's user who has an id and the name.
    """
    id_: uuid.UUID = Field(default_factory=uuid.uuid4, alias="id")
    name: str
    tasks: list[Task] = Field(default_factory=list)

    def add_task(self, task: Task):
        """
        Add a new task to the user's list.

        :param task: Task
        :return: None
        """
        self.tasks.append(task)

    def get_task(self, task_id: uuid.UUID) -> Task:
        """Get the task by its id."""
        for task in self.tasks:
            if task.id_ == task_id:
                return task
        else:
            raise InvalidParameter(f"Task with task_id={task_id} does not exist")

    def update_task(self, task_id: uuid.UUID,
                    name: str | None = None,
                    description: str | None = None,
                    deadline: datetime.datetime | None = None):
        """Update task's parameters."""
        task = self.get_task(task_id)
        if name:
            task.name = name
        if description:
            task.description = description
        if deadline:
            task.deadline = deadline

    def start_the_task(self, task_id: uuid.UUID):
        task = self.get_task(task_id)
        if len(task.intervals) != 0:
            raise InvalidParameter(f"Task with task_id={task_id} was already started")
        task.intervals.append(WorkInterval(start=datetime.datetime.now(), task_id=task_id))

    def pause_the_task(self, task_id: uuid.UUID):
        task = self.get_task(task_id)
        if len(task.intervals) == 0:
            raise InvalidParameter(f"Task with task_id={task_id} was not started")
        elif task.intervals[-1].end is not None:
            raise InvalidParameter(f"Task with task_id={task_id} was already paused")
        task.intervals[-1].end = datetime.datetime.now()

    def resume_the_task(self, task_id: uuid.UUID):
        task = self.get_task(task_id)
        if len(task.intervals) == 0:
            raise InvalidParameter(f"Task with task_id={task_id} was not started")
        elif task.intervals[-1].end is None:
            raise InvalidParameter(f"Task with task_id={task_id} was not paused")
        task.intervals.append(WorkInterval(start=datetime.datetime.now(), task_id=task_id))

    def complete_the_task(self, task_id: uuid.UUID):
        task = self.get_task(task_id)
        if len(task.intervals) == 0:
            raise InvalidParameter(f"Task with task_id={task_id} was not started")
        elif task.intervals[-1].end is None:
            self.pause_the_task(task_id)
        task.is_complete = True
