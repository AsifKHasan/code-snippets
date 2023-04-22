#!/usr/bin/env python3
from PIL import Image, ImageOps

IMAGE_DIR = ''

IMAGE_NAMES = [
]


for image_name in IMAGE_NAMES:
    image_path = f"{IMAGE_DIR}/{image_name}"

    new_image_name = f"{image_name}"
    new_image_path = f"{IMAGE_DIR}/{new_image_name}"

    im = Image.open(image_path)
    im = ImageOps.exif_transpose(im)
    width, height = im.size
    aspect_ratio = width/height
    print(f"dimension[{width} x {height}] found for       [{image_name}]")
    if width > 800:
        width = 800
        height = int(width / aspect_ratio)
        print(f"dimension[{width} x {height}] changed for     [{new_image_name}]")

        im = im.resize((width, height))
        im.save(new_image_path)
    else:
        print(f"dimension[{width} x {height}] not changed for [{image_name}]")
        im.save(new_image_path)
