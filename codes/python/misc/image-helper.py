#!/usr/bin/env python3
from PIL import Image, ImageOps

IMAGE_DIR = '/home/asif/Documents/ftp.spectrum-bd.biz/artifacts/photo/05-ael/'

IMAGE_NAMES = [
'photo__Asadul.Haque.png',
'photo__Asif.Yusuf.png',
'photo__Assaduzzaman.png',
'photo__Dipankar.Kumar.Biswas.png',
'photo__Iqbal.Yusuf.png',
'photo__Md.Ahsan.Habib.Rocky.png',
'photo__Md.Atikur.Zaman.png',
'photo__Md.Mijanur.Rahman.png',
'photo__MD.Nahidul.Islam.Siddique.png',
'photo__Md.Nahidul.Islam.Siddique.png',
'photo__Md.Nasir.Uddin.png',
'photo__MD.Sohel.Rana.png',
'photo__Md.Yousuf.Ali.png',
'photo__Mir.Earfan.Elahi.png',
'photo__Salman.Ahmed.Firoz.png',
'photo__Sohel.Rana.png',
'photo__Suday.Kumer.Ghosh.png',
'photo__Tanvir.Rahman.png',
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
    if width > 400:
        width = 400
        height = int(width / aspect_ratio)
        print(f"dimension[{width} x {height}] changed for     [{new_image_name}]")

        im = im.resize((width, height))
        im.save(new_image_path)
    else:
        print(f"dimension[{width} x {height}] not changed for [{image_name}]")
        im.save(new_image_path)
