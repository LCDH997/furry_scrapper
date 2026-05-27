import pandas as pd
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


PARQUET_PATH = "storage/parquet/processed_images.parquet"


# =========================
# LOAD PARQUET
# =========================

df = pd.read_parquet(PARQUET_PATH)

print(df.head())
print(df.columns)


# =========================
# PREVIEW SINGLE ROW
# =========================

row = df.iloc[0]

print("\nMetadata:")
for col in df.columns:
    if col != "processed_image":
        print(f"{col}: {row[col]}")


# =========================
# SHOW IMAGE
# =========================

image_bytes = row["processed_image"]

image = Image.open(BytesIO(image_bytes))

plt.imshow(image)
plt.axis("off")
plt.show()