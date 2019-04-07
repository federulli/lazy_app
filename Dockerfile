FROM ubuntu:16.04
RUN apt-get update 
RUN apt-get install -y git python3-pip
RUN git clone https://github.com/federulli/lazy_app.git
RUN pip3 install virtualenv
RUN virtualenv -p /usr/bin/python3 venv
RUN /venv/bin/pip install -r /lazy_app/requirements
RUN /venv/bin/python3 /lazy_app/manage.py migrate
EXPOSE 8000