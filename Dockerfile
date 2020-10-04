FROM python

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt
CMD [ "python", "./src/main/python/main.py" ]