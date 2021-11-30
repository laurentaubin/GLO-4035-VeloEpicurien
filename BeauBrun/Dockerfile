FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ src

EXPOSE 5002

CMD ["python", "-u", "src/__main__.py"]