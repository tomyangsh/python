#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, json, os

from torrentool.bencode import Bencode

dic = json.load(open(os.path.expanduser('~/.config/edittorrent.conf')))

torrent = Bencode.read_file(sys.argv[1])
torrent["info"].update({'source': sys.argv[2]})
torrent.update({'announce': dic.get(sys.argv[2])})

with open(sys.argv[1], mode='wb') as f:
    f.write(Bencode.encode(torrent))
