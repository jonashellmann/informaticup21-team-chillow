FROM python

COPY . /code
WORKDIR /code

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "./src/main/python/main.py"]