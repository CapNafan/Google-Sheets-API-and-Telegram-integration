FROM python:3
FROM postgres
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB testcase_numbers
WORKDIR /code
COPY requirements.txt /code/
RUN set -xe && apt-get update -y && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
CMD python3 manage_database.py