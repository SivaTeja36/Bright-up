# Introduction 
NSP Notification service
# Getting Started
always install dependencies from requirements.txt.
if you need new dependency then put it in requirements.in file and then run `pip-compile --output-file=- > requirements.txt` for generating updated dependency file.

when database is empty run first `alembic upgrade head`
go to debugger of the vscode and run as a python fastapi project.
or follow the fast api tutorial to start and developing this service
https://fastapi.tiangolo.com/