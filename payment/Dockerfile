FROM public.ecr.aws/bitnami/python:3.8.7-prod

RUN pip install pika==1.1.0

ENV PYTHONUNBUFFERED=0

RUN mkdir /src
COPY app/ /src/
WORKDIR /src

CMD ["python", "-u", "payment.py"]