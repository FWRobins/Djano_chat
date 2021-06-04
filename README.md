# Django - Realtime Chat App

This is a realtime chat app using websockets and Docker Redis.

## Requirements

Docker is required. Run Docker Redis with "$ docker run -p 6379:6379 -d redis:5". Also found in "docker_redis.txt".

The rest is contained in its own enviroment.
In cmd/powershell start enviroment with "scripts/activate" from main directory.

cd to 'django_chat' and run command "$ python manage.py runserver"

When the server is ready you can browse to '127.0.0.1:8000/chat'

## Details

This was a hobby project to create a chat app with Python Django as the backend and webserver.
When a user is logged in they can dynamically create chat lobbies and anyone with the lobby name can join in.
As this is a realtime app, no messages are saved.
