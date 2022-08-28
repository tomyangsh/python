from PIL import Image

import glob

for i in glob.iglob('/home/tomyang/.kodi/userdata/profiles/dmm/Thumbnails/*/*.jpg', recursive=True):
    image = Image.open(i)
    if image.width == 800:
        crop = image.crop((443, 0, 800, 536))
        crop.save(i)

