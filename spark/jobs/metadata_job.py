from pathlib import Path

from spark.spark_session import SparkManager


spark = SparkManager.create_session()

metadata_files = [
    str(p)
    for p in Path("storage/metadata").rglob("*.json")
]

if not metadata_files:
    raise RuntimeError(
        "No metadata JSON files found in storage/metadata"
    )

metadata_df = spark.read.option("multiline", "true").json(metadata_files)

metadata_df.write.mode("overwrite").parquet(
    "storage/parquet/metadata"
)

species_stats = (
    metadata_df
    .groupBy("species")
    .count()
    .orderBy("count", ascending=False)
)

species_stats.show()