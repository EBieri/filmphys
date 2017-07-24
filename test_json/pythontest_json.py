import json

data = {
   'name' : 'ÄCME',
   'shares' : 100,
   'price' : 542.23
}

data2 = {
   'name' : 'Töst',
   'shares' : 200,
   'price' : 99
}

json_str = json.dumps(data)

liste = []

liste.append(data)
liste.append(data2)

print(liste)

with open('data.json', 'w') as f:
     json.dump(liste, f)


meinarray = []

meinarray.append([1,2,3])
meinarray.append([2,3,4])
meinarray.append(["hallö","du","!"])

print(meinarray)

with open('meinarray.json', 'w') as f:
     json.dump(meinarray, f)
