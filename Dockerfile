# From: https://stackoverflow.com/a/64642121

FROM python:3.9.5 as base

ARG YOUR_ENV

ENV \
    YOUR_ENV=${YOUR_ENV} \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    SETUPTOOLS_VERSION=57.0.0 \
    PIP_VERSION=21.1.2
RUN pip install "setuptools==$SETUPTOOLS_VERSION" "pip==$PIP_VERSION"
WORKDIR /app


FROM base as builder
ENV \
    POETRY_VERSION=1.1.6
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv
COPY poetry.lock pyproject.toml ./
RUN . /venv/bin/activate && poetry install --no-dev --no-root
#COPY . .
#RUN . /venv/bin/activate && poetry build


FROM base as final
COPY --from=builder /venv /venv
COPY django-invest ./
COPY docker-entrypoint.sh ./
EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
