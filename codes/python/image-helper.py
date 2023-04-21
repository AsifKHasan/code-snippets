#!/usr/bin/env python3
from PIL import Image, ImageOps

IMAGE_DIR = '/home/asif/Documents/ftp.spectrum-bd.biz/artifacts/educational-certificates/bachelor/celloscope/'

IMAGE_NAMES = [
    'Ahmed.Nafis.Fuad__BSc__certificate.png',
    'Amiya.Ahamed__BSc__certificate.png',
    'Arnab.Basak__BSc__certificate.png',
    'Dip.Chowdhury__BSc__certificate.png',
    'Mahabuba.Rahman.Moon__BSc__certificate.png',
    'Mainur.Rahman.Rasel__BSc__certificate.png',
    'Maly.Mohsem.Ahmed__BSc__certificate.png',
    'Md.Abdur.Rakib__BA__certificate.png',
    'Md.Abu.Yousuf.Sajal__BSc__certificate.png',
    'MD.Fuad.Hasan.Chowdhury__BSc__certificate.png',
    'Md.Hafizur.Rahman__BSc__certificate.png',
    'Md.Nahidul.Islam.Siddique__BSc__certificate.png',
    'Md.Nazmul.Alam__BSc__certificate.png',
    'Md.Samiul.Alim__BSc__certificate.png',
    'Md.Shariar.Kabir__BSc__certificate.png',
    'Mehedi.Hasan__BBS__certificate.png',
    'Mohammad.Kamrul.Hasan__BSc__certificate.png',
    'Mohammad.Mashud.Karim__BSc__certificate.png',
    'Mohammad.Wakib.Hasan__BSc__certificate.png',
    'Mushfika.Faria__BSc__certificate.png',
    'Nasima.Aktar__BCom__certificate.png',
    'Shah.Shafi.Mohammed.Shariful.Alam__BSc__certificate.png',
    'Syed.Mostofa.Monsur__BSc__certificate.png',
    'Umme.Rumman.Usha__BSc__certificate.png',
]


for image_name in IMAGE_NAMES:
    image_path = f"{IMAGE_DIR}/{image_name}"

    new_image_name = f"{image_name}"
    new_image_path = f"{IMAGE_DIR}/{new_image_name}"

    im = Image.open(image_path)
    im = ImageOps.exif_transpose(im)
    width, height = im.size
    aspect_ratio = width/height
    print(f"dimension[{width} x {height}] found for [{image_name}]")
    if width > 800:
        width = 800
        height = int(width / aspect_ratio)
        print(f"dimension[{width} x {height}] changed for [{new_image_name}]")

        im = im.resize((width, height))
        im.save(new_image_path)
    else:
        print(f"dimension[{width} x {height}] not changed for [{image_name}]")
