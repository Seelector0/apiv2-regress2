FROM europe-west1-docker.pkg.dev/pimpay-cloud/dockerhub-remote-proxy/python:3.10-slim

WORKDIR /app
COPY ./ /app

RUN cd /app && \
    mv .env.example .env && \
    mkdir logs && \
    mkdir -p reports

RUN pip install -r requirements.txt

ENTRYPOINT ["pytest", "-c", "pytest_parallel.ini", "tests/"]
