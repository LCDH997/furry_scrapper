from spark.spark_session import SparkManager


spark = SparkManager.create_session()

metadata_df = spark.read.parquet(
    "storage/parquet/metadata"
)

species_distribution = (
    metadata_df
    .groupBy("species")
    .count()
)

species_distribution.show()
