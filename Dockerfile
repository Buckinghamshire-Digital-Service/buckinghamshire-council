FROM node:12.22.12-alpine as frontend

# Make build & post-install scripts behave as if we were in a CI environment (e.g. for logging verbosity purposes).
ARG CI=true

# Install front-end dependencies.
COPY package.json package-lock.json .babelrc webpack.config.js ./
RUN npm ci --no-optional --no-audit --progress=false

# Install operating system dependencies.
# npm needs this to sync directories.
RUN apk add --no-cache rsync

# Compile static files
COPY ./bc/static_src/ ./bc/static_src/
RUN npm run build:prod

# We use Debian images because they are considered more stable than the alpine
# ones becase they use a different C compiler. Debian images also come with
# all useful packages required for image manipulation out of the box. They
# however weight a lot, approx. up to 1.5GiB per built image.
FROM python:3.11-slim as backend

ARG POETRY_INSTALL_ARGS="--without=dev"

# IMPORTANT: Remember to review both of these when upgrading
ARG POETRY_VERSION=1.8.2

# Install dependencies in a virtualenv
ENV VIRTUAL_ENV=/venv

RUN useradd bc --create-home && mkdir /app $VIRTUAL_ENV && chown -R bc /app $VIRTUAL_ENV

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku or Dokku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PATH - Make sure that Poetry is on the PATH, along with our venv
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.12/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.12/using/cmdline.html#cmdoption-u
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used. Please match with EXPOSE so it works on Dokku.
#    Heroku will ignore EXPOSE and only set PORT variable. PORT variable is
#    read/used by Gunicorn.
ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    POETRY_INSTALL_ARGS=${POETRY_INSTALL_ARGS} \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=bc.settings.production \
    PORT=8000

# Make $BUILD_ENV available at runtime
ARG BUILD_ENV
ENV BUILD_ENV=${BUILD_ENV}

# Port exposed by this container. Should default to the port used by your WSGI
# server (Gunicorn). This is read by Dokku only. Heroku will ignore this.
EXPOSE 8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# Install poetry at the system level
RUN pip install --no-cache poetry==${POETRY_VERSION}

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
USER bc

# Install your app's Python requirements.
RUN python -m venv $VIRTUAL_ENV
COPY --chown=wagtailkit_repo_name pyproject.toml poetry.lock ./
RUN pip install --no-cache --upgrade pip && poetry install ${POETRY_INSTALL_ARGS} --no-root && rm -rf $HOME/.cache

COPY --chown=bc --from=frontend ./bc/static_compiled ./bc/static_compiled

# Copy application code.
COPY --chown=bc . .

# Run poetry install again to install our project (so the the bc package is always importable)
RUN poetry install ${POETRY_INSTALL_ARGS}

# Collect static. This command will move static files from application
# directories and "static_compiled" folder to the main static directory that
# will be served by the WSGI server.
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

# Load shortcuts
COPY ./docker/bashrc.sh /home/bc/.bashrc


# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn

# These steps won't be run on production
FROM backend as dev

# Swap user, so the following tasks can be run as root
USER root

# Update apt repositories
RUN apt-get update --yes --quiet

# Install `psql`, useful for `manage.py dbshell`
# `rsync` is used by mode to build the frontend.
RUN apt-get install -y postgresql-client rsync

# Restore user
USER bc

# Install nvm and node/npm
ARG NVM_VERSION=0.39.3
COPY --chown=bc .nvmrc ./
RUN curl https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash \
    && bash --login -c "nvm install --no-progress && nvm alias default $(nvm run --silent --version)"

# Pull in the node modules for the frontend
COPY --chown=bc --from=frontend ./node_modules ./node_modules

# do nothing forever - exec commands elsewhere
CMD tail -f /dev/null
