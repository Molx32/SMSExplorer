FROM python:3.9-slim
WORKDIR /app

# Install system dependencies in one layer, clean up afterwards to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libssl-dev libpcre3 libpcre3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Install Python dependencies (use --no-cache-dir to avoid caching)
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir uwsgi


# Expose the port that your app will run on
EXPOSE 9000


# CMD [ "uwsgi", "--ini", "uwsgi.ini"]
# CMD [ "python3", "SMSExplorer.py"]
# Command to run the app with Gunicorn (this is the recommended production setup)
CMD ["gunicorn", "--access-logfile", "-", "--bind", "0.0.0.0:9000", "SMSExplorer:app"]