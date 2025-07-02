import datetime
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from src.adapters.user_repository import JSONUserRepository
from src.domain.exceptions import InvalidParameter
from src.domain.models import User
from src.domain.services.user import UserService, TaskCommand

service = UserService(JSONUserRepository())

class AppContext(BaseModel):
    global_user: User

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    predefined_id = uuid.UUID("0b2e1f84-93d8-4792-b2e1-6fbbfb376d74")
    try:
        global_user = service.create_user("Test user", id_=predefined_id)
    except InvalidParameter:
        global_user = service.get_user(predefined_id)
    try:
        yield AppContext(global_user=global_user)
    finally:
        pass

mcp = FastMCP(
    "ToDo app",
    lifespan=app_lifespan
)

@mcp.tool()
def create_task(name: str, description: str | None = None, deadline: datetime.datetime | None = None) -> uuid.UUID:
    """Create a new task and get its id."""
    ctx = mcp.get_context()
    global_user = ctx.request_context.lifespan_context.global_user
    print(ctx.request_context.lifespan_context.global_user)
    task_data = {"name": name, "description": description, "deadline": deadline}
    task_id = service.create_task(global_user.id_, task_data)
    return task_id

@mcp.tool()
def start_task(task_id: uuid.UUID) -> None:
    """Start the task's execution"""
    ctx = mcp.get_context()
    global_user = ctx.request_context.lifespan_context.global_user
    service.change_task_status(global_user.id_, task_id, TaskCommand.START)

@mcp.tool()
def pause_task(task_id: uuid.UUID) -> None:
    """Pause the task."""
    ctx = mcp.get_context()
    global_user = ctx.request_context.lifespan_context.global_user
    service.change_task_status(global_user.id_, task_id, TaskCommand.PAUSE)

@mcp.tool()
def resume_task(task_id: uuid.UUID) -> None:
    """Resume task's execution"""
    ctx = mcp.get_context()
    global_user = ctx.request_context.lifespan_context.global_user
    service.change_task_status(global_user.id_, task_id, TaskCommand.RESUME)

@mcp.tool()
def complete_task(task_id: uuid.UUID) -> None:
    """Complete the task's execution."""
    ctx = mcp.get_context()
    global_user = ctx.request_context.lifespan_context.global_user
    service.change_task_status(global_user.id_, task_id, TaskCommand.COMPLETE)

if __name__ == '__main__':
    mcp.run(transport="streamable-http")