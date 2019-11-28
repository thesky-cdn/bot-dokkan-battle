import requests
import json
import os as fs
from colorama import init, Fore
import re
import config
import webbrowser

def createSaves():
    if not fs.path.isdir('./saves'):
        try:
            fs.mkdir('./saves')
            print('"saves" directory created.')
        except:
            print('unable to create "saves" directory.')

def getVersionCodes():
    try:
        r = requests.get('https://raw.githubusercontent.com/K1mpl0s/16-pc/master/versions.json')
        jso = r.json()
        if str(jso['sixteen']) != config.version:
            print(Fore.CYAN + '16 > new update!\nwould you like to open discord? Press ENTER if so.')
            input()
            webbrowser.open(str(jso['discord']), new=1, autoraise=True)
            exit()
        config.gb_code = jso['gb']
        config.jp_code = jso['jp']
    except:
        print('can\'t fetch version codes.')
        exit()

def checkServers(ver):
    try:
        if ver == 'gb':
            url = 'https://ishin-global.aktsk.com/ping'
        else:
            url = 'https://ishin-production.aktsk.jp/ping'
        headers = {
            'X-Platform': 'android',
            'X-ClientVersion': '1.0.0',
            'X-Language': 'en',
            'X-UserID': '////'
        }
        r = requests.get(url, data=None, headers=headers)
        store = r.json()
        if 'error' in store:
            print(store)
        url = store['ping_info']['host']
        port = store['ping_info']['port_str']
        if fs.path.isfile(ver + '-host.txt'):
            fs.unlink(ver + '-host.txt')
            f = open(ver + '-host.txt', 'w')
            f.write(url + ':' + str(port) + '\n')
            f.close()
            #print(Fore.GREEN + '[' + ver + ' server] ' + url + ':' + str(port))
        else:
            f = open(ver + '-host.txt', 'w')
            f.write(url + ':' + str(port) + '\n')
            f.close()
            #print(Fore.GREEN + '[' + ver + ' server] ' + url + ':' + str(port))
        return True
    except:
        print(Fore.RED + '[' + ver + ' server] can\'t connect.')
        return False

def help1():
    f = open('mainpage.txt', 'r')
    txt = f.read().replace('{CYAN}', Fore.CYAN).replace('{LTYELLOW}', Fore.LIGHTYELLOW_EX).replace('{GREEN}', Fore.GREEN).replace('{YELLOW}', Fore.YELLOW).replace('\\n', '\n')
    for match in re.findall(r'\\x[0-9A-Fa-f]{2}', txt):
        txt = txt.replace(match, chr(int(match[2:], 16)))
    print(txt)
    f.close()

def help2():
    f = open('help.txt', 'r')
    txt = f.read().replace('{CYAN}', Fore.CYAN).replace('{LTYELLOW}', Fore.LIGHTYELLOW_EX).replace('{GREEN}', Fore.GREEN).replace('{YELLOW}', Fore.YELLOW).replace('\\n', '\n')
    for match in re.findall(r'\\x[0-9A-Fa-f]{2}', txt):
        txt = txt.replace(match, chr(int(match[2:], 16)))
    print(txt)
    f.close()