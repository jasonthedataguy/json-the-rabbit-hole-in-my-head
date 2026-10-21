FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libnss3 libdbus-1-3 libatk1.0-0 libgbm-dev libasound2 \
    libxrandr2 libxkbcommon-dev libxfixes3 libxcomposite1 libxdamage1 \
    libpango-1.0-0 libcairo2 libcups2 libatk-bridge2.0-0 \
    && rm -rf /var/lib/apt/lists/*
