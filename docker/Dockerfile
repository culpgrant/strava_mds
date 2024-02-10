FROM python:3.11.7

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

COPY poetry.lock pyproject.toml /code/
COPY docker/workspace.yaml ${DAGSTER_HOME}

#RUN poetry install --without dev --no-root && rm -rf ${POETRY_CACHE_DIR}
RUN poetry install --without dev --no-root

# Copy all files
# TODO: I think if we get the code location grpc service working we might not need thi
#COPY . /code

# Expose Port
#EXPOSE 3000 Moved to docker-compose

#ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"] Moved to docker-compose
