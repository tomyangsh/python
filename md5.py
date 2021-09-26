import hashlib, base64, sys

#string = sys.argv[1]

for num1 in range(1, 50000):
    for num2 in range(1, 50000):
        try:
            string = chr(num1)+chr(num2)
            byte = string.encode('UTF-8')
        except:
            continue
        md5 = hashlib.md5(byte).hexdigest()
        if md5 == 'e60422e0d43a4e254499b34c17d48fd2':
            print(chr(string))
            break
