FROM python:3.7.3-alpine

WORKDIR /app

RUN python3 -m pip install --user --upgrade setuptools wheel

COPY . /app

RUN python3 setup.py sdist bdist_wheel

RUN pip install -e .
