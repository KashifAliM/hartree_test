FROM python:3.10.10-slim-buster

RUN apt-get -y update && \
    apt-get -y clean

COPY requirements.txt /tmp

RUN pip install pip=="23.0.1" --upgrade

ARG APP_DIR=/opt/app/

ADD . ${APP_DIR}
WORKDIR ${APP_DIR}

RUN pip install -r requirements.txt

RUN pip install .
#ENV PYTHONPATH=${APP_DIR}

CMD [ "/bin/bash" ]
