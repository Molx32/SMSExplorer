FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install -y gcc build-essential libssl-dev

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 9000

CMD [ "uwsgi", "--ini", "uwsgi.ini"]