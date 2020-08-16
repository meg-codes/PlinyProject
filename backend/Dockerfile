FROM python:3.7.8-slim-buster as base

ENV PYTHONUNBUFFERED=1 \
  # prevents python creating .pyc files
  PYTHONDONTWRITEBYTECODE=1 \
  \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv" \
  APP_DIR="/opt/app"

ENV PATH="$VENV_PATH/bin:$PATH"
RUN apt update && apt install -y \
  libpq-dev \
  gcc


FROM base as requirements

COPY requirements.txt .
RUN python -m venv $VENV_PATH
RUN pip install pip --upgrade && pip install wheel
RUN pip install -r requirements.txt

FROM requirements as production

WORKDIR $PYSETUP_PATH
COPY --from=requirements $PYSETUP_PATH $PYSETUP_PATH
WORKDIR $APP_DIR
COPY . $APP_DIR

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "plinyproj.wsgi"]


