docker build --build-arg BOT_TOKEN=${BOT_TOKEN} -f docker/ubuntu/Dockerfile -t biblepybottelegram .
docker run --rm -v ${PWD}:/app  -d biblepybottelegram