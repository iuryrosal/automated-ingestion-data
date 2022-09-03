FROM python:3.8-buster

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 5000

CMD ["python", "src/api_main.py"]