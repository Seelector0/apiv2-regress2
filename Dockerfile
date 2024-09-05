FROM python:3.10-slim

WORKDIR /app
COPY ./ /app

RUN cd /app && \
    mv .env.example .env && \
    mkdir logs

RUN pip install -r requirements.txt

ENTRYPOINT ["sleep", "30", "&&", "pytest", "-c", "pytest_parallel.ini", "tests/"]