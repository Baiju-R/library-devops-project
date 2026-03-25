FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y netcat-openbsd curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/wait-for-db.sh

EXPOSE 5000

COPY wait-for-db.sh .

CMD ["sh","./wait-for-db.sh","gunicorn","-w","4","-b","0.0.0.0:5000","--timeout","120","--graceful-timeout","30","--access-logfile","-","--error-logfile","-","--log-level","info","app:app"]