FROM python:3.11

WORKDIR /code

COPY requirements.txt /code/

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000