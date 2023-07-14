import json

file = open("./src/spiders/ips_ip3366.json", 'r')
ips = json.loads(file.read())


def isActive(item):
    return item["active"]


activeAddress = []

for item in ips:
    if (item["active"]):
        activeAddress.append(
            f"{item['type'].lower()}://{item['ip']}:{item['port']}".lower())

activeAddress = list(set(activeAddress))

newFile = open("./src/ipPool.py", 'a+')

for address in activeAddress:
    newFile.write(f'\n"{address}",')
