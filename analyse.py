import json
import re
import collections


def json_load_all(buf):
    while True:
        try:
            yield json.loads(buf)
        except json.JSONDecodeError as err:
            yield json.loads(buf[:err.pos])
            buf = buf[err.pos:]
        else:
            break


arr = []

with open('data.json') as fd:
    arr = list(json_load_all(fd.read()))

counter = []

for i in range(0, len(arr)):
    try:
        arr[i]['Target'][0]['IP4'][0]
        arr[i]['Source'][0]['IP4'][0]
    except KeyError:
        continue
    else:
        print(arr[i]['Source'][0]['IP4'][0], end=" ")
        print("->", end=" ")
        print(arr[i]['Target'][0]['IP4'][0])
        source_target = {
            "source": arr[i]['Source'][0]['IP4'][0], "target": arr[i]['Target'][0]['IP4'][0]}
        counter.append(source_target)


c = collections.Counter(json.dumps(l) for l in counter)
count_attackers = {}

for key, value in c.items():
    print(key, value)
    try:
        count_attackers[json.loads(key)['target']] += 1
    except KeyError:
        count_attackers[json.loads(key)['target']] = 1

print("Unique attackers on source (Only multiple unique attacker sources)")

for key, value in count_attackers.items():
    if(value > 1):
        print(key, value)
