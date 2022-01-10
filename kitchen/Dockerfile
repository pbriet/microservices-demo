FROM public.ecr.aws/bitnami/python:3.8.7-prod

RUN apt-get update && apt-get install -y postgresql-client gcc python3-dev libpq-dev

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED=0

RUN adduser user

RUN mkdir /src /entrypoint
COPY app/ /src/
COPY entrypoint/ /entrypoint/

RUN chown -R user:user /src /entrypoint

EXPOSE 9000
WORKDIR /src
USER user

ENTRYPOINT ["/entrypoint/start.sh"]

CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:9000"]