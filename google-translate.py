import sys, re, requests, os

source = open(sys.argv[1], 'r')
target = open(os.path.splitext(sys.argv[1])[0]+'-zh.srt', 'w')
url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-cn&&dt=t&q='

source = re.sub(r'([a-zA-Z])\n([a-zA-Z])', r'\1 \2', source.read())
line_list = list(source.split("\n"))

for line in line_list:
    if re.match('\d.*\d$', line):
        target.write(line+'\n')
    elif line == '':
        target.write(line+'\n')
    else:
        result = requests.get(url+requests.utils.quote(line)).json()[0][0][0]
        target.write(result+'\n')
    sleep(1)
