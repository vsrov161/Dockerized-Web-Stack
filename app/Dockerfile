FROM python:3.12-slim

WORKDIR /app

# Сначала копируем только requirements — так Docker закэширует этот слой,
# и переустановка зависимостей при каждой сборке не будет происходить,
# если requirements.txt не менялся
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]