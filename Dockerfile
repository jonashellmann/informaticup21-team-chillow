FROM python

COPY . /code
WORKDIR /code

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install

CMD [ "python", "./main.py"]