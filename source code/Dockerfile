FROM bitnami/spark:3.3.2

LABEL maintainer="vitor-docker"

RUN pip3 install pyspark pandas pytest pyarrow

WORKDIR /app

COPY . /app

CMD ["python3", "-m", "pytest", "tests/test_transformations.py"]
