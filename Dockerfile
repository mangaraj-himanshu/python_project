FROM python:3.8.15-buster

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --quiet --no-cache-dir -r requirements.txt

COPY . .

# CMD ["uvicorn", "app:app","--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "app.py"]