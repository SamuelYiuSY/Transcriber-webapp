FROM python:3.8

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

EXPOSE 5100

CMD ["python3", "main.py"]
