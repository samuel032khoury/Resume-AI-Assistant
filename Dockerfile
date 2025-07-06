FROM python:3.12.8
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["sh", "-c", "playwright install && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]