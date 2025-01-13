# Dockerfile for backend
FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# install mysql_client
RUN apt-get update && apt-get install -y default-mysql-client

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD /wait-for-it.sh db:3306 -- sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
