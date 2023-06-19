#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from myfunc import media

file_path = sys.argv[1]

thumb = []

try:
    for i in [3, 6, 9, 12]:
        f = media.screenshot(file_path, f'{i}:00')
        thumb.append(media.upload_image(f, 'imgbb'))
    thumb = '[img]'+'[/img]\n[img]'.join(thumb)+'[/img]'
except Exception as e:
    pass

print(thumb)
