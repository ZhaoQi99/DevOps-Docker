FROM python:3.6-slim
LABEL maintainer="zhaoqi99@outlook.com"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client gettext vim

RUN apt-get install -y build-essential \
    libldap2-dev libsasl2-dev 

RUN mkdir -p /usr/src/qops_server
WORKDIR /usr/src/qops_server
COPY requirements.txt  /usr/src/qops_server
RUN pip install -r requirements.txt
RUN rm -rf /usr/src/qops_server
COPY . /usr/src/qops_server
ENV ENV=pro
RUN python manage.py collectstatic
RUN python manage.py compilemessages
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
