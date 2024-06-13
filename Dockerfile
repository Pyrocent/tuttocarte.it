FROM python
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]