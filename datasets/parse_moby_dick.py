from collections import Counter
import re

out = []
with open('moby_dick_raw.txt') as f:
    for line in f.readlines():
        line = re.sub('[!:,.;]', '', line)
        words = line.split()
        for w in words:
            out.append(w+'\n')

print('[+] saving file')
with open('moby_dick.txt', 'w+') as f:
    f.writelines(out)

