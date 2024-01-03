# plex-sad-ui
The UI component of my Plex Search and Destroy solution

# PyPi Dependency updates

```shell
docker run -it --rm -v ${PWD}:/repo -w /repo python:3.12-slim bash
apt update && apt install -y git
pip install --upgrade pip
pip install --upgrade Flask gunicorn 'sad_libraries@git+https://github.com/chrisjohnson00/plex-sad-libraries.git@initial-version'
pip freeze > requirements.txt
```

## Running locally

```commandline
export FLASK_APP=sad_ui
flask --debug run
```

or

```shell
docker build . -t sad-ui
docker run -it --rm -p 5000:5000 sad-ui
```

Run redis locally with

```shell
docker run --rm --name redis -p 6379:6379 -d redis
```

