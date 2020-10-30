FROM python

COPY . /app
WORKDIR /app

ENV DEACTIVATE_PYGAME=TRUE
ENV PLAY_ONLINE=TRUE

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

CMD [ "python", "./main.py"]