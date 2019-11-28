import time
import os as fs

version = '1.0.1'

#request defaults
try:
    gb_url = 'https://' + open('gb-host.txt', 'r').readline().rstrip().split(':')[0]
    gb_port = open('gb-host.txt', 'r').readline().rstrip().split(':')[1]
    jp_url = 'https://' + open('jp-host.txt', 'r').readline().rstrip().split(':')[0]
    jp_port = open('jp-host.txt', 'r').readline().rstrip().split(':')[1]
except:
    print('=======================\n\n CODED BY K1MPL0S <3    \n\n=======================')

#account defaults
lang = 'en'
country = 'US'
currency = 'USD'
uuid = '0f97df48-01e3-4d8f-8ba0-a1e8cced278c:5bf18553fe25d277'
ad = '95c27e08-72bb-4760-83e8-9e878d1999f8'

#version code
gb_code = ''
jp_code = ''

#android
device_name1 = 'SM'
device_model1 = 'SM-S10'
device_ver1 = '9.0'
device_agent1 = 'Dalvik/2.1.0 (Linux; Android 9.0; SM-S10)'
#ios
device_name2 = 'iPhone'
device_model2 = 'iPhone XR'
device_ver2 = '13.0'
device_agent2 = 'CFNetwork/808.3 Darwin/16.3.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X)'

#client data
file_ts1 = str(int(round(time.time(), 0))) #asset
db_ts1 = str(int(round(time.time(), 0))) #database
file_ts2 = str(int(round(time.time(), 0)))
db_ts2 = str(int(round(time.time(), 0)))

#database keys
gdb = '9bf9c6ed9d537c399a6c4513e92ab24717e1a488381e3338593abd923fc8a13b'
jdb = '2db857e837e0a81706e86ea66e2d1633'