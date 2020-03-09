FROM python:3.7-slim

LABEL "maintainer"="Christian Heider <christian.heider@alexandra.dk>"
LABEL "repository"="https://github.com/cnheider/gh-action-postdoc"
LABEL "homepage"="https://github.com/cnheider/gh-action-postdoc"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /postdoc_build/

COPY LICENSE.md .
COPY requirements.txt .
COPY postdoc .
#COPY scripts .

RUN apt-get -y update && apt-get -y install make
RUN pip install -r requirements.txt
#RUN chmod +x ---.sh
ENTRYPOINT ["/postdoc_build/postdoc/entry_point.py"]


