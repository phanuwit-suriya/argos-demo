FROM ubuntu:18.04

WORKDIR /argos-adf

# Sets utf-8 encoding for Python et al
ENV LANG=C.UTF-8
# Turns off writing .pyc files; superfluous on an ephemeral container.
ENV PYTHONDONTWRITEBYTECODE=1
# Seems to speed things up.
ENV PYTHONUNBUFFERED=1

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Makes the default answers be used for all questions.
ENV DEBIAN_FRONTEND=noninteraction

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    npm \
    nodejs \
    python3-jsonschema \
    python3-matplotlib \
    python3-requests \
    python3-numpy \
    python3-pip \
    python3-setuptools && \
    npm install -g pm2@latest && \
    pip3 install --no-cache-dir slackclient==2.1.0 && \
    rm -rf /var/lib/apt/lists/*

COPY src/ ./

CMD ["./argos-init.sh"]