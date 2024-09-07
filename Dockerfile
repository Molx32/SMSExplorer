FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install -y gcc build-essential libssl-dev

COPY . .

RUN pip3 install -r requirements.txt
RUN apt install libpcre3 libpcre3-dev -y
RUN pip3 install uwsgi -I --no-cache-dir

EXPOSE 9000

# CMD [ "uwsgi", "--ini", "uwsgi.ini"]
# CMD [ "python3", "SMSExplorer.py"]
CMD [ "gunicorn", "--bind", "0.0.0.0:9000", "SMSExplorer:app"]
   

