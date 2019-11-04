FROM python:2.7.17-buster
MAINTAINER Gerolf Ziegenhain <gerolf.ziegenhain@gmail.com>

ADD . exitwp
RUN pip install -r /exitwp/pip_requirements.txt

WORKDIR /exitwp
