#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import binascii
import urllib.request

def totalPowerFromShellyJson(answer):
    if 'meters' in answer:
        meters = answer['meters'] # shelly
    else:
        meters = answer['emeters'] # shellyEM & shelly3EM
    total = 0
    # shellyEM has one meter, shelly3EM has three meters:
    for meter in meters:
        total = total + meter['power']
    return int(total)

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S shelly watty.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/status", timeout=3).read().decode("utf-8")))
aktpower = totalPowerFromShellyJson(answer)
relais = int(answer['relays'][0]['ison'])
powerc = 0
temp0 = '0.0'
temp1 = '0.0'
temp2 = '0.0'
try:
    temp0 = str(answer['ext_temperature'][0]['tC'])
    temp1 = str(answer['ext_temperature'][1]['tC'])
    temp2 = str(answer['ext_temperature'][2]['tC'])
except:
    pass
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + ',"temp0":' + str(temp0) + ',"temp1":' + str(temp1) + ',"temp2":' + str(temp2) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
