import imagehash
from PIL import Image


class Hashing:
    @staticmethod
    def phash(path):
        return str(imagehash.phash(Image.open(path)))
