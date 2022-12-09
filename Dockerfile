# ************ CHALLENGE ************ : We could've used alpine based image for minimun disk image but apline is not a recommended use with python since it does not support wheel for packages
#  Warning from Fastapi creator himself : https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#-alpine-python-warning
FROM python:3.7.5-slim
RUN apt-get update 
# setting PYTHONUNBUFFERED to a value different from 0 ensures that the python output i.e. the stdout and stderr streams are sent straight to terminal (e.g. your container log) 
ENV PYTHONUNBUFFERED=1
# setting Lang env var For standard language support
ENV LANG C.UTF-8
# Symbolic links to pip and python for ease of use in the cli
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
RUN ln -sf /usr/bin/python3 /usr/bin/python
# upgrading package manager
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
# Using pipenv instead of Conda since Conda consumes much larger disk space and pipenv results in more deterministic build using .lock file which is safer
RUN pip install --no-cache-dir pipenv
# setting the working directory to the project folder
WORKDIR /app
COPY Pipfile Pipfile.lock ./
# Installing project dependencies
# --system flag, so it will install all packages into the system python, and not into the virtualenv. Since docker containers do not need to have virtualenvs
RUN pipenv install --system --deploy
COPY . ./
EXPOSE 8000
CMD [ "uvicorn","app.main:app","--reload","--host", "0.0.0.0"]