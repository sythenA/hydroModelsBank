
import pickle


f = open('infoMessage.txt', 'r')
dat = f.readlines()
f.close()

messageLog = dict()
info = dict()

paragraph = list()
message = list()
for line in dat:
    try:
        num = int(line)
        message = list()
        message.append(num)
        if message:
            paragraph.append(message)
    except:
        message.append(line)
paragraph.append(message)

print paragraph

for message in paragraph:
    text = list()
    for line in message:
        if type(line) == int:
            head = line
            info = dict()
        elif line.startswith('title:'):
            info.update({'title': line.replace('title:', '')})
        elif line == 'detail:\n':
            text = list()
        else:
            text.append(line)
    info.update({'detail': text})
    messageLog.update({head: info})

f = open('infoText.lang', 'wb')
pickle.dump(messageLog, f)
