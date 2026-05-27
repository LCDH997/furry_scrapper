from pyspark.sql.functions import col

from spark.spark_session import SparkManager


spark = SparkManager.create_session()

hashes_df = spark.read.parquet(
    "storage/parquet/metadata"
)

possible_duplicates = (
    hashes_df.alias("a")
    .join(
        hashes_df.alias("b"),
        col("a.phash") == col("b.phash")
    )
    .filter(col("a.id") != col("b.id"))
)

possible_duplicates.show()
