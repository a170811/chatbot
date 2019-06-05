import requests as req
import pickle
from sys import argv
import random


if len(argv)<2:
    print('你這樣問，我很難回答。')
    exit()
resp = req.get(f"http://140.116.156.234:5000/{argv[1]}")

data = pickle.load(open('./model/data/answer.pkl', 'rb'))

try:
    buff = pickle.load(open('./buff.pkl', 'rb'))
except FileNotFoundError:
    buff = {}

res = resp.text.split()[1]

if res == '黃火木舊台味冰店推薦給你':
    res = '大碗公一直都很有名、在長榮路上、不用排隊哦。'
if res == 'flask!':
    res = '我不知道你在說什麼'

if random.randint(0, 100) < 30:
    res = data[random.randint(0, len(data))]

if argv[1] in buff:
    res = buff[argv[1]]
else:
    buff[argv[1]] = res

pickle.dump(buff, open('./buff.pkl', 'wb'))
print(res)

