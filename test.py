import json
import sys
fname=sys.argv[1]
f=open(fname)
data=json.load(f)
# print(data[0]['price'])