FROM python

COPY . /app
WORKDIR /app

ENV TERM=xterm-256color

RUN python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry export -f requirements.txt | pip install -r /dev/stdin

ENTRYPOINT [ "python", "./main.py", "--deactivate-pygame=TRUE" ]
CMD [ "--play-online=TRUE" ]