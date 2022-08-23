#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, re

srt = sys.argv[1]
u = b'\xef\xbb\xbf'+open(srt, 'rb').read().decode('gb2312', 'ignore').encode()
u = re.sub(b'\x0d', b'', u)
open(srt, 'wb').write(u)
