FROM python:slim

WORKDIR /server

COPY . /fractions_1.py /server/

COPY . /requirements.txt /server/

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "fractions_1.py"]