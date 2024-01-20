FROM python:3.11

RUN apt-get update && apt-get install -y cron nano supervisor

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y \
    && apt-get purge -y --auto-remove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /root/.cache/

#COPY src/marker/pyproject.toml src/marker/poetry.lock /app/
COPY . /app

WORKDIR /app

RUN cat scripts/install/apt-requirements.txt | xargs apt-get install -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#COPY . /app

ADD supervisord.conf /etc/supervisor/conf.d/

ENV TESSDATA_PREFIX=/tessdata
#USER ali_tank

EXPOSE 8000

CMD ["/usr/bin/supervisord"]
