FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY . /usr/src/app

RUN rm -rf /usr/src/app/data && \
  mkdir /data && \
  ln -s /data /usr/src/app/data

VOLUME /data
EXPOSE 8080
ENV FLASK_APP app.py
CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]
