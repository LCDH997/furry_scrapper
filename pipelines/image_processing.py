from pathlib import Path
from io import BytesIO

import pandas as pd
from PIL import Image
import pyarrow as pa
import pyarrow.parquet as pq
import shutil


INPUT_PARQUET = "storage/parquet/metadata"
OUTPUT_PARQUET = "storage/parquet/processed_images"


# =========================
# LOAD METADATA
# =========================

metadata_df = pd.read_parquet(INPUT_PARQUET)

processed_rows = []


# =========================
# IMAGE PROCESSING
# =========================

for _, row in metadata_df.iterrows():
    image_path = row["image_path"]

    try:
        image = Image.open(image_path).convert("RGB")

        # resize
        image = image.resize((1024, 1024))

        # save processed image to bytes
        buffer = BytesIO()
        image.save(buffer, format="JPEG")

        image_bytes = buffer.getvalue()

        # preserve ALL metadata
        row_dict = row.to_dict()

        # add processed image
        row_dict["processed_image"] = image_bytes

        processed_rows.append(row_dict)


    except Exception as e:
        print(f"Failed: {image_path} -> {e}")


# =========================
# SAVE PARQUET
# =========================

result_df = pd.DataFrame(processed_rows)

OUTPUT_PARQUET = "storage/parquet/processed_images.parquet"

old_path = Path("storage/parquet/processed_images")

if old_path.exists() and old_path.is_dir():
    shutil.rmtree(old_path)


table = pa.Table.from_pandas(result_df)

pq.write_table(
    table,
    OUTPUT_PARQUET,
    compression="snappy"
)

print("Saved.")