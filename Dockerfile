FROM python:3.9-slim-buster

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install bs4

COPY . /home/alena/python/files_parser/
WORKDIR /home/alena/python/files_parser/

CMD ["python", "files_parser.py"]
