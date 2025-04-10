import base64
import json
import requests
import struct
"""
https://docs.python.org/3/library/struct.html#format-characters

int: the signed integer value - 4 bytes - i
uint: the unsigned integer value - 4 bytes -  I
short: the decoded short value - 2 bytes - h
float: surprisingly, the float value - 4 bytes - f
double: the double value - shockingly - 8 bytes - d
big_endian_double: you get the idea by now! - 8 bytes -  >d
"""
URL = "https://hackattic.com/challenges/help_me_unpack"
PARAMS = {'access_token': "90fabb2a44afba20"}
r = requests.get(url = URL+"/problem", params = PARAMS)

data = r.json()

bytes = data['bytes']
decoded = base64.b64decode(bytes)


int_v = struct.unpack("i", decoded[:4])[0]
uint_v = struct.unpack("I", decoded[4:8])[0]
short_v = struct.unpack("hxx", decoded[8:12])[0]
float_v = struct.unpack("f", decoded[12:16])[0]
double_v = struct.unpack("d", decoded[16:24])[0]
big_endian_d_v = struct.unpack(">d", decoded[24:])[0]

result = {
    "int": int_v,
    "uint": uint_v,
    "short": short_v,
    "float": float_v,
    "double": double_v,
    "big_endian_double": big_endian_d_v,
}

res = requests.post(url=URL+"/solve", params = PARAMS, data=json.dumps(result))
print(res.text)

