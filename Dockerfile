FROM python

COPY . /code
WORKDIR /code

RUN pip install pybuilder
RUN pyb