FROM python

WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
CMD [ "gunicorn app:app" ]