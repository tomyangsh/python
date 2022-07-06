#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, json, os

from torrentool.bencode import Bencode

dic = {
        "phd": "https://tracker.privatehd.to/announce",
	    "cmz": "https://tracker.cinemaz.to/announce",
	    "avz": "https://tracker.avistaz.to/announce",
	    "exo": "https://tracker.exoticaz.to/announce" 
        }

torrent = Bencode.read_file(sys.argv[1])
site = ''
while not site in dic:
    site = input("Site: ({}) ".format('/'.join(list(i for i in dic))))
torrent["info"].update({'source': site})
torrent.update({'announce': dic.get(site)})
output = Bencode.encode(torrent)

with open(sys.argv[1], mode='wb') as f:
    f.write(output)
