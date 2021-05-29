FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . /app
WORKDIR /app


RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt