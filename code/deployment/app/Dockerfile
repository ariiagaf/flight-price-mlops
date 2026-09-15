FROM python:3.13-slim

WORKDIR /app

COPY code/deployment/app/app.py /app/app.py

RUN pip install --no-cache-dir \
    streamlit \
    requests

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]