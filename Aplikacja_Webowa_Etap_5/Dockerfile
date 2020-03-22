FROM python:3.7-alpine
WORKDIR /P3
ENV FLASK_APP rest_full_app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8080
COPY ./P3 /P3
RUN pip install -r requirements.txt
CMD ["flask", "run"]
