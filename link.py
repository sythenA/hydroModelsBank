import re
import os.path

f = open(os.path.join(os.path.dirname(__file__), 'link.set'), 'r')

links = dict()

for line in f.readlines():
    row = re.split('[|]', line)
    print(row)
    links.update({int(row[0]): row[1]})
