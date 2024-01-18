FROM python:3.11 AS requirements-project

LABEL maintainer="requirements-project <ali20bn20ali.email@example.com>"
LABEL org.label-schema.name="requirements-project"
LABEL org.label-schema.description="requirements-project description"
LABEL org.label-schema.version="1.0"


RUN apt update
RUN apt install -y cron nano supervisor

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash ali_tank

RUN apt-get update && apt-get upgrade -y
RUN apt-get purge -y --auto-remove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /root/.cache \

COPY src/marker/pyproject.toml src/marker/poetry.lock /app/
COPY . /app
WORKDIR /app

RUN cat scripts/install/apt-requirements.txt | xargs apt-get install -y

RUN pip install --upgrade pip
RUN pip install -r  requirements.txt



ADD supervisord.conf /etc/supervisor/conf.d/
COPY . /app

ENV TESSDATA_PREFIX=/tessdata
RUN pip install beautifulsoup4
#USER ali_tank

EXPOSE 8000

CMD ["python", "src/main.py"]
CMD ["/usr/bin/supervisord"]