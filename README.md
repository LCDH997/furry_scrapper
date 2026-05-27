## Getting Started: Workflow Execution

To process your data, follow the pipeline sequence outlined below. Ensure your environment is properly configured before running these commands.

| Order | Task | Command |
| :--- | :--- | :--- |
| 1 | **Scraping** | `python main.py` |
| 2 | **Metadata Extraction** | `python -m spark.jobs.metadata_job` |
| 3 | **Deduplication** | `python -m spark.jobs.dedup_job` |
| 4 | **Image Processing** | `python -m pipelines.image_processing` |

> **Note:** These jobs are designed to be run sequentially. Ensure that the output of each step is successfully verified before initiating the subsequent job, particularly when handling large datasets.
