FROM python:3.8-slim

COPY ./ /vpn
WORKDIR /vpn
RUN pip install -r requirements.txt
EXPOSE 8000 443

CMD ["gunicorn", "server:app", "--workers=1", "--threads=3", "-b", "0.0.0.0:8000"]