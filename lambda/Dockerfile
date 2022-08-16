
FROM python:buster

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

RUN apt-get update && apt-get install libpq-dev


COPY * .
ADD util /util/

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "handler.main" ]
