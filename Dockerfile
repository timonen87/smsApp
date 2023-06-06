FROM python:3.10-alpine3.16

COPY ./requirements.txt /temp/requirements.txt

COPY . /app

WORKDIR /app/

RUN apk add postgresql-client build-base postgresql-dev
RUN pip3 install --upgrade pip
RUN pip install -r /temp/requirements.txt



RUN adduser -D dockuser
USER dockuser

CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
#    python3 manage.py collectstatic --noinput && \
#
#CMD sudo chown -R $dockuser:$dockuser /app
