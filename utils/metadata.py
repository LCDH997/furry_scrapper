import json
from pathlib import Path


class MetadataWriter:
    @staticmethod
    def save(path, data):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
