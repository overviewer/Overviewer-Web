FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV OVERVIEWER_SETTINGS /usr/src/app/overviewer/settings/docker.py
EXPOSE 8000
CMD ./start.sh
