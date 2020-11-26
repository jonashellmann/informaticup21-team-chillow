FROM python

COPY . /app
WORKDIR /app

ENV TERM=xterm-256color

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

CMD [ "python", "./main.py", "--deactivate-pygame=TRUE", "--play-online=TRUE" ]