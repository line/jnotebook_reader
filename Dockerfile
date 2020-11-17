FROM python:3.7-slim-buster

WORKDIR /jnotebook_reader

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x ./docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]