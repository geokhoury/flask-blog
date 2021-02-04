FROM python:3.8-alpine

WORKDIR /flask_souq

ADD requirements.txt /flask_souq

RUN pip3 install -r requirements.txt

COPY souq/ /flask_souq

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "souq"]