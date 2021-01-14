FROM python:3.8-alpine

WORKDIR /flask_blog

ADD requirements.txt /flask_blog

RUN pip3 install -r requirements.txt

COPY blog/ /flask_blog

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "blog"]