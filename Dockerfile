# Stage 1: Build image
FROM python:3.10-slim AS build

# Install dependencies needed for building (e.g., git)
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install dependencies into the virtual environment
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.10-slim

ARG VERSION=unset
ENV VERSION=$VERSION

WORKDIR /usr/src/app
EXPOSE 5000

ENV PATH="/venv/bin:$PATH"

# Copy only the virtual environment from the build stage
COPY --from=build /venv /venv

COPY . .

CMD gunicorn --log-file=- --workers=2 --threads=4 --worker-class=gthread --worker-tmp-dir /dev/shm --bind 0.0.0.0:5000 "sad_ui:create_app()"
