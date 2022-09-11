FROM python:3-bullseye
COPY ./app /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir
CMD gunicorn --workers=4 --threads=4 --worker-class=gthread --log-file=- --bind 0.0.0.0:5000 musicdb:app
