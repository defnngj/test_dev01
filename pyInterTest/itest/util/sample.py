import simplejson
import requests

body = '{"user":"zhiheng","pwd":198876}'

ss = simplejson.loads(body)
print(ss)