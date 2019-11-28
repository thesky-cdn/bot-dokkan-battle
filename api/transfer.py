import requests
import config
import crypto
import json

def validate(ver, tc, fc):
    if ver == 'gb':
        url = config.gb_url + '/auth/link_codes/' + str(tc) + '/validate'
        code = config.gb_code
    else:
        url = config.jp_url + '/auth/link_codes/' + str(tc) + '/validate'
        code = config.jp_code
    headers = {
        'Accept': '*/*',
        'X-Language': config.lang,
        'X-Platform': 'android',
        'X-ClientVersion': code,
        'Content-Type': 'application/json',
        'User-Agent': config.device_agent1
    }
    data = {'eternal': True,'user_account': {'platform': 'android','user_id': fc}}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

def use(ver, os, tc, fc):
    if os == 'android':
        dn = config.device_name1
        dm = config.device_model1
        dv = config.device_ver1
        dua = config.device_agent1
    else:
        dn = config.device_name2
        dm = config.device_model2
        dv = config.device_ver2
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/auth/link_codes/' + str(tc)
        code = config.gb_code
    else:
        url = config.jp_url + '/auth/link_codes/' + str(tc)
        code = config.jp_code
    headers = {
        'Accept': '*/*',
        'X-Language': config.lang,
        'X-Platform': os,
        'X-ClientVersion': code,
        'Content-Type': 'application/json',
        'User-Agent': dua
    }
    data = {'eternal': True,'old_user_id': '','user_account': {'device': dn,'device_model': dm,'os_version': dv,'platform': os,'unique_id': config.uuid}}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    return r.json()

def create(ver, os, token, secret):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/auth/link_codes'
        auth = crypto.mac(ver, token, secret, 'POST', '/auth/link_codes')
        code = config.gb_code
        asset = config.file_ts1
        db = config.db_ts1
    else:
        url = config.jp_url + '/auth/link_codes'
        auth = crypto.mac(ver, token, secret, 'POST', '/auth/link_codes')
        code = config.jp_code
        asset = config.file_ts2
        db = config.db_ts2
    headers = {
        'X-Platform': os,
        'X-Language': config.lang,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'User-Agent': dua
    }
    data = {'eternal':True}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()