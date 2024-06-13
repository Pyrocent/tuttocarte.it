FROM python
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]