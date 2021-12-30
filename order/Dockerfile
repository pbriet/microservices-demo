FROM public.ecr.aws/bitnami/python:3.8.7-prod

RUN apt-get update && apt-get install -y postgresql-client gcc python3-dev libpq-dev

RUN pip install django==3.1.6
RUN pip install pika==1.1.0
RUN pip install psycopg2==2.8.6
RUN pip install requests==2.25.1
RUN pip install watchdog[watchmedo]

ENV PYTHONUNBUFFERED=0

RUN mkdir /src
COPY app/ /src/

EXPOSE 9000
WORKDIR /src

CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:9000"]