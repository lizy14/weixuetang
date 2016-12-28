FROM python:3.5

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# this section is very important to keep a separate layer for the dependencies
RUN mkdir /code/requirements
ADD requirements.txt /code/
ADD requirements/* /code/requirements/
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/
