FROM python:3.8-alpine

COPY . /app
WORKDIR /app

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apk --no-cache add tzdata && \
  cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
  echo "Asia/Seoul" > /etc/timezone && \
  pip install --no-cache-dir pipenv && \
  pipenv install --system --deploy --clear

CMD ["python3", "src/main.py"]