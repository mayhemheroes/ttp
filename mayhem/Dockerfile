# Build Stage
FROM python:3.11-slim

RUN pip install --no-cache-dir atheris

ADD . /src
WORKDIR /src
RUN python3 -m pip install --no-cache-dir .

CMD ["/src/mayhem/fuzz_template.py"]
