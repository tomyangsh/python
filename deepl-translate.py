#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, re, requests, os, time

source = open(sys.argv[1], 'r')
target = open(os.path.splitext(sys.argv[1])[0]+'-zh.srt', 'w')
url = 'https://api-free.deepl.com/v2/translate'

def get_translation(text):
    payload = {'auth_key': 'xxx', 'text': text, 'target_lang': 'ZH'}
    result = requests.post(url, data=payload).json()['translations'][0]['text']
    return result

source = re.sub(r'([a-zA-Z,])\n([a-zA-Z])', r'\1 \2', source.read())
line_list = list(source.split("\n"))

for line in line_list:
    if re.match('.*\d$', line):
        target.write(line+'\n')
    elif line == '':
        target.write(line+'\n')
    else:
        result = get_translation(line)
        target.write(result+'\n')
