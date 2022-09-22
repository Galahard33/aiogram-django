FROM python:3.9

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "/application/app.py"]