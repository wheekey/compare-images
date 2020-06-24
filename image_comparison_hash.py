from PIL import Image
import imagehash

def compare(original_img_path, image_to_compare):
    hash0 = imagehash.average_hash(Image.open(original_img_path))
    hash1 = imagehash.average_hash(Image.open(image_to_compare))
    return hash0-hash1
