FROM python:3.10.8

RUN apt-get update
RUN python3 -m pip install --upgrade pip
RUN git clone https://github.com/2chanhaeng/personal-ledger-management.git /app
RUN cd /app
RUN python3 -m pip install -r /app/requirements.txt

# set secret key environment variable
ENV SECRET_KEY=secret_key
RUN python /app/manage.py migrate
RUN python /app/manage.py runserver
