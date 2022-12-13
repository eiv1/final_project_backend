FROM python:slim

WORKDIR /server

COPY . /fun.py /server/

COPY . /requirements.txt /server/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "fun.py"]