FROM python:3.11-slim

# 1) copy reqs first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2) then copy the rest
COPY . .

CMD ["python", "main.py"]