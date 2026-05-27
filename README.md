Typical working scenario:
Run Scraper
python main.py
Run Spark Metadata Job
python -m spark.jobs.metadata_job
Run Deduplication
python -m spark.jobs.dedup_job
Run Image Processing
python -m pipelines.image_processing
