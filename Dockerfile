FROM ubuntu:20.04
FROM python:3.8


RUN set -ex \
    && apt-get update \
    && python -V \
    && whereis python \
    && /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.douban.com/simple/ \
    && pip list

RUN mkdir -p "/home/yolo_serv"

COPY . /home/yolo_serv

WORKDIR /home/yolo_serv

VOLUME /home/yolo_serv/out

RUN set -ex \
    && cp .env.example .env \
    && /usr/local/bin/python -m pip install -r requirements.txt -i https://pypi.douban.com/simple/ \
    && pip list

EXPOSE 8555

ENTRYPOINT ["python", "app.py"]
