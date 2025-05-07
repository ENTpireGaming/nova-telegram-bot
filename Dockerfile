FROM python:3.10-slim
WORKDIR /app

EXPOSE 10000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
