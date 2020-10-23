FROM python

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt
RUN python -m pip install --upgrade pip
CMD [ "python", "./src/main/python/main.py"]