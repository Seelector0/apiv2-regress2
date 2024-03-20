FROM python:3.10-slim

WORKDIR /app
COPY ./ /app

RUN cd /app && \
    mv .env.example .env && \
    mkdir logs

RUN pip install -r requirements.txt

ENTRYPOINT ["pytest -s -v tests/test_aggregation_russian_post.py tests/test_integration_russian_post.py"]
