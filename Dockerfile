FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . /app
#COPY ml_model /app
#COPY
WORKDIR /app


#RUN virtualenv venv/
#RUN /venv/bin/pip install -r requirements.txt

#CMD ["/venv/bin/python", "/app/main.py"]

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt