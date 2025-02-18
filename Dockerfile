FROM python:3.10.8

ENV PORT 8080

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
