FROM python:3.11 AS base

WORKDIR /app

COPY requirements.txt /app/requirements.txt


FROM base AS builder

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt

FROM builder AS run

WORKDIR /app

COPY . .

ENTRYPOINT ["python3"]
CMD ["main.py"]