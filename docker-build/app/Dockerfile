FROM python:3.13-alpine

WORKDIR /code

COPY .env /code/.env
COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY start.sh /code/start.sh
COPY ./src /code/src
COPY ./static /code/static
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini


RUN dos2unix start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]