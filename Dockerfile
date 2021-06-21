FROM python:3.6-slim

COPY ["requeriments.txt" ,  "/app/"]

WORKDIR /app

RUN pip install -r requeriments.txt

COPY ["." ,  "/app/"]

EXPOSE 8000