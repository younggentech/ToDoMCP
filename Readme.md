# Disclaimer
This is a project for fun.
# Idea
Create a simple ToDo API, supporting HTTP API and MCP.
# Desired Features
- Authorization with JWT
- Add a task with:
  - Name
  - Optional description
  - Optional deadline
- Start working on a task
- Pause the work on a task
- Continue working on task
- Mark task as completed
- Calculate task's duration by summing all working intervals up
# Notes
1. Start with in-memory database
# Implemented functionality:
- MCP for one global client (good for on-machine usage)
- Add a task with:
  - Name
  - Optional description
  - Optional deadline
- Start working on a task
- Pause the work on a task
- Continue working on task
- Mark task as completed

![Claude Dialog](/assets/img.png)
# How to install to Claude
```sh
PYTHONPATH=$(pwd) mcp install --env-var="PYTHONPATH=$(pwd)" src/application/mcp/server.py
```