FROM ubuntu:22.04@sha256:74075bbbd941a1766a0db1d66e617a0ab82ab54dd23e0b55bebd7e62d9e9b7be

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev python3-venv

#npm
RUN apt -y update
RUN apt -y install nodejs
RUN apt -y install npm

COPY ./python_app /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN pip3 install -e .

# CMD ["tail", "-f", "/dev/null"]

CMD ["pserve", "development.ini",  "--reload"]