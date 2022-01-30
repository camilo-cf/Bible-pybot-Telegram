docker build --build-arg BOT_TOKEN=${BOT_TOKEN} -t biblepybottelegram .
docker run --rm -v ${PWD}:/app  -d biblepybottelegram