FROM ubuntu

RUN apt-get update && apt-get install -q -y \
  git \
  python-pip \
  python-yaml \
  python-bs4 \
  python-html2text \
  libyaml-dev \
  python-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./pip_requirements.txt ./pip_requirements.txt
RUN pip install --upgrade -r pip_requirements.txt

COPY . .

RUN python exitwp.py

CMD ["tar", "-cf", "-", "./build" ]
