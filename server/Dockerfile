FROM python

COPY . /server
WORKDIR /server

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]