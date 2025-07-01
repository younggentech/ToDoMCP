import datetime

import pytest

from src.domain.models import User, Task


@pytest.fixture
def user_without_tasks():
    return User(name="Test user")

@pytest.fixture
def user_with_task():
    return User(name="Test user", tasks=[Task(name="Task 1")])


def test_task_creation(user_without_tasks):
    t1 = Task(name="Task 1")
    t2 = Task(name="Task 2")
    user_without_tasks.add_task(t1)
    user_without_tasks.add_task(t2)
    assert len(user_without_tasks.tasks) == 2
    assert user_without_tasks.get_task(t1.id_).name == t1.name


def test_task_modification(user_with_task):
    task = user_with_task.tasks[0]
    new_description = "ensure the task works"
    user_with_task.update_task(task.id_, description=new_description)
    assert user_with_task.tasks[0].description == new_description
    assert user_with_task.get_task(task.id_).description == new_description
    new_deadline = datetime.datetime.now()
    user_with_task.update_task(task.id_, deadline=new_deadline)
    assert user_with_task.tasks[0].deadline == new_deadline
    assert user_with_task.get_task(task.id_).deadline == new_deadline


def test_task_state_transition(user_with_task):
    task_id = user_with_task.tasks[0].id_
    user_with_task.start_the_task(task_id)
    assert len(user_with_task.get_task(task_id).intervals) == 1
    assert user_with_task.get_task(task_id).intervals[0].end is None
    user_with_task.pause_the_task(task_id)
    assert len(user_with_task.get_task(task_id).intervals) == 1
    assert (datetime.datetime.now() - user_with_task.get_task(task_id).intervals[0].end) < datetime.timedelta(seconds=1)
    user_with_task.resume_the_task(task_id)
    assert len(user_with_task.get_task(task_id).intervals) == 2
    assert user_with_task.get_task(task_id).intervals[1].end is None
    user_with_task.complete_the_task(task_id)
    assert len(user_with_task.get_task(task_id).intervals) == 2
    assert (datetime.datetime.now() - user_with_task.get_task(task_id).intervals[1].end) < datetime.timedelta(seconds=1)
    assert user_with_task.get_task(task_id).is_complete

