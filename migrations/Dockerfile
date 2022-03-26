FROM python

COPY . /migrations

WORKDIR /migrations

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

CMD python3 migrator.py