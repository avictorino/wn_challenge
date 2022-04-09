FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
ADD . /app
ENV PYTHONUNBUFFERED 1

RUN \
 apt-get update && \
 pip install --upgrade pip && \
 pip install gunicorn && \
 python3 -m pip install -r requirements.txt && \
 apt-get clean


CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8001"]


EXPOSE 8001