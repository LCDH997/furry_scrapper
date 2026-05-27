from pyspark.sql import SparkSession

from config import SPARK_APP_NAME


class SparkManager:
    @staticmethod
    def create_session():
        spark = (
            SparkSession.builder
            .master("local[*]")
            .appName(SPARK_APP_NAME)
            .config(
                "spark.hadoop.io.native.lib.available",
                "false"
            )
            .getOrCreate()
        )

        spark.sparkContext.setLogLevel("ERROR")

        return spark