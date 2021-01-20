FROM python:3.8
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
# ADD blog blog/
ENV FLASK_APP blog
ENV FLASK_ENV development
CMD pwd && ls -al && flask run --host 0.0.0.0