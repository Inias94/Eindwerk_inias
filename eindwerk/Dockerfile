FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY boot.sh .

RUN chmod +x boot.sh  # Maak boot.sh uitvoerbaar

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]
