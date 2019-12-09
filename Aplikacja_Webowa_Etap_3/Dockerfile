FROM python:3.7-alpine
WORKDIR /sixth_app
ENV FLASK_APP rest_full_app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 80
COPY ./sixth_app /sixth_app
RUN pip install -r requirements.txt
CMD ["flask", "run"]