import requests
import config
import crypto
import json
import random

def register(ver, os, ad = None, unique = None, key = None):
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
        url = config.gb_url + '/auth/sign_up'
        code = config.gb_code
    else:
        url = config.jp_url + '/auth/sign_up'
        code = config.jp_code
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-Language': config.lang,
        'User-Agent': dua
        }
    data = None
    acc_ad = None
    acc_unique = None
    if ad != None and unique != None and key != None:
        user_acc = {
            'ad_id': ad,
            'country': config.country,
            'currency': config.currency,
            'device': dn,
            'device_model': dm,
            'os_version': dv,
            'platform': os,
            'unique_id': unique
        }
        data = {'captcha_session_key': key, 'user_account': user_acc}
    else:
        unique = crypto.guid()
        acc_ad = unique[0]
        acc_unique = unique[1]
        user_acc = {
            'ad_id': unique[0],
            'country': config.country,
            'currency': config.currency,
            'device': dn,
            'device_model': dm,
            'os_version': dv,
            'platform': os,
            'unique_id': unique[1]
        }
        data = {'user_account': user_acc}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return [r.json(), acc_ad, acc_unique]

def login(ver, os, basic, first, key = None):
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
        url = config.gb_url + '/auth/sign_in'
        if first:
            code = '////'
        else:
            code = config.gb_code
    else:
        url = config.jp_url + '/auth/sign_in'
        if first:
            code = config.jp_code
        else:
            code = config.jp_code
    headers = {
        'Accept': '*/*',
        'Authorization': 'Basic ' + str(basic),
        'Content-Type': 'application/json',
        'X-UserCountry': config.country,
        'X-UserCurrency': config.currency,
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-Language': config.lang,
        'User-Agent': dua
    }
    if key != None:
        data = {'captcha_session_key': key, 'ad_id': config.ad, 'unique_id': config.uuid}
    else:
        data = {'ad_id': config.ad, 'unique_id': config.uuid}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()