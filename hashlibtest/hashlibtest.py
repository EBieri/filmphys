#!/usr/bin/python

import hashlib
##
##m = hashlib.sha1()
##m.update(b'hallo')
##print(m.digest())
##print(m.hexdigest())
##
##print(type(b'hallo'))


with open("film01.iso", "rb") as f:
    data = f.read()
    sha1summe = hashlib.sha1()
    sha1summe.update(data)
    b = sha1summe.hexdigest()
    print(type(b))
    print(b[:10])
