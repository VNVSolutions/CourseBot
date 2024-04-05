FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /CourseBot

WORKDIR /CourseBot

COPY web/requirements.txt /CourseBot/

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get install -y cron

ADD . /CourseBot/

CMD ["cron", "-f"]
