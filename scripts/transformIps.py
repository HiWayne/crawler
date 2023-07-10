import json

file = open("./src/spiders/ips.json", 'r')
ips = json.loads(file.read())


def isActive(item):
    return item["active"]


activeAddress = []

for item in ips:
    if (item["active"]):
        activeAddress.append(f"{item['ip']}:{item['port']}")

activeAddress = list(set(activeAddress))

newFile = open("./addresses.py", 'a+')
newFile.write("addresses = [")
for address in activeAddress:
    newFile.write(f'\n"{address}",')
newFile.write("\n]")
