# plex-sad-ui
The UI component of my Plex Search and Destroy solution

# PyPi Dependency updates

`pulsar-client` does not support Python > 3.10

```shell
docker run -it --rm -v ${PWD}:/repo -w /repo python:3.10-slim bash
apt update && apt install -y git
pip install --upgrade pip
pip install --upgrade Flask gunicorn pulsar-client 'sad_libraries@git+https://github.com/chrisjohnson00/plex-sad-libraries.git@v0.1.3'
pip freeze > requirements.txt
```

## Running locally

```commandline
export TMDB_API_ACCESS_TOKEN='your token'
export PULSAR_SERVER=192.168.1.133
export PULSAR_TOPIC=test-topic
export FLASK_APP=sad_ui
flask --debug run
```

Run redis locally with

```shell
docker run --rm --name redis -p 6379:6379 -d redis
```

