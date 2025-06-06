from pyspark.sql import SparkSession
import pytest

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("Test Brewery Transformations") \
        .master("local[*]") \
        .getOrCreate()

def test_partition_by_country(spark):
    data = [
        {"id": 1, "name": "Brewery A", "country": "USA"},
        {"id": 2, "name": "Brewery B", "country": "USA"},
        {"id": 3, "name": "Brewery C", "country": "Canada"},
    ]
    df = spark.createDataFrame(data)

    grouped = df.groupBy("country").count().collect()
    grouped_dict = {row['country']: row['count'] for row in grouped}

    assert grouped_dict["USA"] == 2
    assert grouped_dict["Canada"] == 1