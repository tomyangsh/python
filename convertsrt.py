#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

srt = sys.argv[1]
u = b'\xef\xbb\xbf'+open(srt, 'rb').read().decode('gb2312', 'ignore').encode()
open(srt, 'wb').write(u)
