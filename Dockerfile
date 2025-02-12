FROM python:3.12.1-slim-bullseye

# Don't write .pyc files (or __pycache__ dirs) inside the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=.

RUN apt update -y && \
    DEBIAN_FRONEND=noninteractive apt install -y gcc musl-dev libffi-dev make && \
    apt clean -y all

# Install Python dependencies from PyPI
COPY requirements*.txt ./

RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache --force-reinstall --ignore-installed -r requirements_dev.txt

# Copy application source code into container
WORKDIR /usr/src/app
COPY . .

CMD [ "bash" ]
