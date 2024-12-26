FROM python:3.11.4-alpine3.18

WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"] 

#docker compose up
#docker compose down