FROM python:3.12.3-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    unzip \
    gcc \
    git \
    gconf-service \
    libasound2 \
    libgbm1 \
    libgtk-3-0 \
    libnss3 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Matching ChromeDriver using Chrome for Testing (CfT) Endpoints
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1) \
    && LATEST_CHROMEDRIVER_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json" | grep -oP "\"${CHROME_MAJOR_VERSION}\.[^\"]*\":{\"version\":\"\K([^\"]+)" | head -n 1) \
    && echo "Detected Chrome Major Version: $CHROME_MAJOR_VERSION" \
    && echo "Using ChromeDriver Version: $LATEST_CHROMEDRIVER_VERSION" \
    && wget -q --show-progress -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${LATEST_CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && chromedriver --version
# Install Poetry
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir poetry==1.8.3

# Configure Poetry Environment
ENV POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ARG POETRY_FLAGS="--without dev"

# Set up Application Directory and Install Dependencies
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Add /usr/local/bin (where chromedriver is) and the virtualenv bin to PATH
ENV VIRTUAL_ENV=/app/.venv PATH="/app/.venv/bin:/usr/local/bin:$PATH"

RUN poetry install --no-root $POETRY_FLAGS \
    && rm -rf $POETRY_CACHE_DIR \
    && chmod -R 777 /app/.venv

COPY ./src /app/src


RUN echo "PATH is: $PATH"
RUN which python
RUN which poetry
RUN which google-chrome
RUN which chromedriver
RUN google-chrome --version
RUN chromedriver --version

CMD ["python", "src/main/python/webapp.py"]