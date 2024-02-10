FROM python:3.12.2

ENV \
  # Poetry's configuration
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'\
  # Dagster configuration
  DAGSTER_HOME='/opt/dagster/dagster_home/'

# Install Poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them
WORKDIR /code

# This is unable to find the files
COPY poetry.lock pyproject.toml /code/

#RUN poetry install --without dev --no-root && rm -rf ${POETRY_CACHE_DIR}
RUN poetry install --without dev --no-root

# Copy all files
COPY . /code

# Expose Port
EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
