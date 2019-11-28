import json
import requests
import datetime
from colorama import init, Fore, Style
import os as fs
import crypto
import api.transfer as transfer
import api.auth as auth
import api.outgame as outgame
import api.ingame as ingame
import api.farmbot as farmbot
import database
import webbrowser
import utils

init(autoreset=True)

farm = []

def checkDatabase(ver, os, token, secret):
    print('checking database versions...')
    store = outgame.getDatabase(ver, token, secret, None)
    version = store['version']
    if fs.path.isfile(ver + '-data.txt'):
        f = open(ver + '-data.txt', 'r')
        ver2 = f.readline().rstrip()
        f.close()
        if str(ver2) != str(version):
            print(str(version))
            fs.unlink(ver + '-data.txt')
            print('downloading database... (this may take awhile.)')
            database.download(ver, token, secret, version)
            print(Fore.GREEN + 'done.')
        else:
            print('no database to download.')
    else:
        print(str(version))
        print('downloading database... (this may take awhile.)')
        database.download(ver, token, secret, version)
        print(Fore.GREEN + 'done.')

def refresh():
    ver = farm[0][0]
    os = farm[0][1]
    iden = farm[0][2]
    store = auth.login(ver, os, crypto.basic(iden), False)
    if 'error' not in store:
        farm[0][3] = store['access_token']
        farm[0][4] = store['secret']
        print('client refreshed.')
    else:
        print(store)

def createSaveFile(ver, os, iden, save):
    if len(save) >= 1:
        if fs.path.isfile('./saves/'+save+'.txt'):
            print('save name already exists.\npicking default name...')
            f = open('./saves/save.txt', 'w')
            f.write(ver+':'+os+'\n')
            f.write(str(iden.replace('\n', '')) + '\n')
            f.close()
        else:
            f = open('./saves/'+save+'.txt', 'w')
            f.write(ver+':'+os+'\n')
            f.write(str(iden.replace('\n', '')) + '\n')
            f.close()
    else:
        print('save name is too small.\npicking default name...')
        f = open('./saves/save.txt', 'w')
        f.write(ver+':'+os+'\n')
        f.write(str(iden.replace('\n', '')) + '\n')
        f.close()

def checkTcLoop(ver, os, iden):
    global farm
    store = auth.login(ver, os, crypto.basic(iden), False)
    if 'error' not in store:
        if 'reason' not in store:
            store = transfer.create(ver, os, store['access_token'], store['secret'])
            if 'error' not in store:
                fc = '000000000'
                tc = str(store['link_code'])
                store = transfer.validate(ver, tc, fc)
                if 'error' not in store:
                    print(Fore.GREEN + tc)
                    return True
                else:
                    print('transfer code not found. making new code...')
                    checkTcLoop(ver, os, iden)
            else:
                print(store)
        else:
            url = store['captcha_url']
            key = store['captcha_session_key']
            webbrowser.open(url, new=1, autoraise=True)
            print('Complete CAPTCHA to login... Press ENTER when done.')
            input()
            checkTcLoop(ver, os, iden)
    else:
        print(store)

def Handler(msg):
    global farm
    args = msg.split(' ')
    #===== base =====
    #new
    if args[0].lower() == 'new' and len(farm) == 0:
        if len(args) == 3:
            if args[1] == 'gb' or args[1] == 'jp':
                if args[2] == 'ios' or args[2] == 'android':
                    store = auth.register(args[1], args[2])
                    if 'error' not in store:
                        print(store)
                        url = store[0]['captcha_url']
                        key = store[0]['captcha_session_key']
                        webbrowser.open(url, new=1, autoraise=True)
                        print('Complete CAPTCHA to continue... Press ENTER when done.')
                        input()
                        store = auth.register(args[1], args[2], store[1], store[2], key)
                        if 'error' not in store:
                            store = auth.login(args[1], args[2], crypto.basic(store[0]['identifier']), True)
                            if 'error' not in store:
                                farmbot.tutorial(args[1], args[2], store['access_token'], store['secret'])
                            else:
                                print(store)
                        else:
                            print(store)
                    else:
                        print(store)
                else:
                    print('invalid OS input.')
            else:
                print('invalid version input.')
        else:
            print('gb/jp ios/android')
        return 1
    #transfer
    if args[0].lower() == 'add' and len(farm) == 0:
        if len(args) == 3:
            if args[1] == 'gb' or args[1] == 'jp':
                ver = args[1]
                tc = args[2]
                fc = '000000000'
                store = transfer.validate(ver, tc, fc)
                if 'error' not in store:
                    if not store['platform_difference']:
                        os = 'android'
                    else:
                        os = 'ios'
                    store = transfer.use(ver, os, tc, fc)
                    if 'error' not in store:
                        print(Fore.YELLOW + 'identifier for recover.\n' + store['identifiers'].replace('\n', ''))
                        iden = store['identifiers']
                        store = auth.login(ver, os, crypto.basic(iden), False)
                        if 'error' not in store:
                            if 'reason' not in store:
                                print(Fore.WHITE + 'What would you like to name this save?')
                                save = input().lower()
                                createSaveFile(ver, os, iden, save)
                                farm.append([ver, os, iden, store['access_token'], store['secret'], save])
                                checkDatabase(ver, os, store['access_token'], store['secret'])
                                utils.help2()
                            else:
                                url = store['captcha_url']
                                key = store['captcha_session_key']
                                webbrowser.open(url, new=1, autoraise=True)
                                print('Complete CAPTCHA to login... Press ENTER when done.')
                                input()
                                store = auth.login(ver, os, crypto.basic(iden), False, key)
                                if 'error' not in store:
                                    print(Fore.WHITE + 'What would you like to name this save?')
                                    save = input().lower()
                                    createSaveFile(ver, os, iden, save)     
                                    farm.append([ver, os, iden, store['access_token'], store['secret'], save])                               
                                    checkDatabase(ver, os, store['access_token'], store['secret'])
                                    utils.help2()
                                else:
                                    print(store)
                        else:
                            print(store)
                    else:
                        print(store)
                else:
                    print(store)
            else:
                print('invalid version input.')
        else:
            print('gb/jp TC')
        return 0
    #load
    if args[0].lower() == 'load' and len(farm) == 0:
        if len(args) == 2:
            save = args[1].lower()
            if fs.path.isfile('./saves/'+save+'.txt'):
                f = open('./saves/'+save+'.txt', 'r')
                line1 = f.readline().rstrip().split(':')
                ver = line1[0]
                os = line1[1]
                iden = f.readline().rstrip()
                f.close()
                store = auth.login(ver, os, crypto.basic(iden), False)
                if 'error' not in store:
                    if 'reason' not in store:
                        farm.append([ver, os, iden, store['access_token'], store['secret'], save])
                        checkDatabase(ver, os, store['access_token'], store['secret'])
                        utils.help2()
                    else:
                        url = store['captcha_url']
                        key = store['captcha_session_key']
                        webbrowser.open(url, new=1, autoraise=True)
                        print('Complete CAPTCHA to login... Press ENTER when done.')
                        input()
                        store = auth.login(ver, os, crypto.basic(iden), False, key)
                        if 'error' not in store:
                            farm.append([ver, os, iden, store['access_token'], store['secret'], save])
                            checkDatabase(ver, os, store['access_token'], store['secret'])
                            utils.help2()
                        else:
                            print(store)
                else:
                    print(store)
            else:
                print('that save doesn\'t exist.')
        else:
            print('you didnt select a save.')
        return 1
    #===== tools =====
    #verify
    if args[0].lower() == 'verify' and len(farm) == 0:
        if len(args) == 4:
            if args[1] == 'gb' or args[1] == 'jp':
                if len(args[2]) == 9 or len(args[2]) == 10:
                    store = transfer.validate(args[1], args[3], args[2])
                    if 'error' not in store:
                        if not store['platform_difference']:
                            os = 'android'
                        else:
                            os = 'iOS'
                        if store['user_is_valid']:
                            matches = 'Yes'
                        else:
                            matches = 'No'
                        if store['link_code_is_valid']:
                            valid = 'Yes'
                        else:
                            valid = 'No'
                        print(Fore.GREEN + 'FC matches TC: ' + matches + '\nValid TC: ' + valid + '\nOS: ' + os + '\nName: ' + str(store['user_name']) + '\nRank: ' + str(store['user_rank']))
                    else:
                        print(store)
                else:
                    print('abnormal FC/ID size.')
            else:
                print('invalid version input.')
        else:
            print('gb/jp FC/ID TC')
        return 0
    #recover
    if args[0].lower() == 'recover' and len(farm) == 0:
        if len(args) == 4:
            if args[1] == 'gb' or args[1] == 'jp':
                if args[2] == 'ios' or args[2] == 'android':
                    if checkTcLoop(args[1], args[2], args[3]) == True:
                        print('account successfully recovered.')
                else:
                    print('invalid OS input.')
            else:
                print('invalid version input.')
        else:
            print('gb/jp ios/android identifier')
        return 0
    #renew
    if args[0].lower() == 'renew' and len(farm) == 0:
        if len(args) == 4:
            if args[1] == 'gb' or args[1] == 'jp':
                if len(args[2]) == 9 or len(args[2]) == 10:
                    store = transfer.validate(args[1], args[3], args[2])
                    if 'error' not in store:
                        if not store['platform_difference']:
                            os = 'android'
                        else:
                            os = 'ios'
                        store = transfer.use(args[1], os, args[3], args[2])
                        if 'error' not in store:
                            print(Fore.YELLOW + store['identifiers'].replace('\n', ''))
                            checkTcLoop(args[1], os, store['identifiers'])
                        else:
                            print(store)
                    else:
                        print(store)
                else:
                    print('abnormal FC/ID size.')
            else:
                print('invalid version input.')
        else:
            print('gb/jp FC/ID TC')
        return 0
    #host
    if args[0].lower() == 'host' and len(farm) == 0:
        if len(args) == 2:
            if args[1] == 'gb' or args[1] == 'jp':
                store = outgame.ping(args[1])
                print(Fore.GREEN + 'Host: ' + store['ping_info']['host'] + '\nPort: ' + str(store['ping_info']['port']) + '\nAPI port: ' + str(store['ping_info']['port_str']) + '\nCF URI Prefix: ' + store['ping_info']['cf_uri_prefix'])
            else:
                print('invalid version input.')
        else:
            print('gb/jp')
        return 0
    #===== other =====
    #support
    if args[0].lower() == 'support':
        url = 'https://discord.gg/nrjvK2J'
        webbrowser.open(url, new=1, autoraise=True)
        return 1
    #exit
    if args[0].lower() == 'exit':
        if len(farm) == 0:
            exit()
        else:
            farm = []
            utils.help1()
            return 1
    #===== farmbot =====
    #help
    if args[0].lower() == 'help' and len(farm) == 1:
        if len(farm) == 0:
            utils.help1()
        else:
            utils.help2()
        return 1
    #info
    if args[0].lower() == 'info' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.user(ver, os, token, secret, False)
        if 'error' not in store:
            user = store['user']
            print(Fore.YELLOW + 'Account information\nVersion: ' + ver + '\nOS: ' + os + '\nID: ' + str(user['id']) + '\nName: ' + user['name'] + '\nRank: ' + str(user['rank']) + '\nStones: ' + str(user['stone']) + '\nZeni: ' + str(user['zeni']) + '\nStamina: ' + str(user['act']) + '/' + str(user['act_max']) + '\nCapacity: ' + str(user['card_capacity']) + '/' + str(user['total_card_capacity']) + '\nTeam cost: ' + str(user['team_cost_capacity']) + '\nFriends capacity: ' + str(user['friends_capacity']))
        else:
            print(store)
        return 0
    #gift
    if args[0].lower() == 'gift' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        farmbot.gift(ver, os, token, secret)
        return 0
    #mission
    if args[0].lower() == 'mission' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        farmbot.mission(ver, os, token, secret)
        return 0
    #news
    if args[0].lower() == 'news' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.news(ver, os, token, secret)
        if 'error' not in store:
            titles = []
            for i in store['announcements']:
                print(i['title'] + ' - ' + str(i['id']))
        else:
            print(store)
        return 0
    #banners
    if args[0].lower() == 'banners' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.banners(ver, os, token, secret)
        if 'error' not in store:
            titles = []
            for i in store['gashas']:
                print(str(i['id']) + ' - ' + i['name'])
        else:
            print(store)
        return 0
    #events
    if args[0].lower() == 'events' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.events(ver, os, token, secret)
        if 'error' not in store:
            titles = []
            for i in store['events']:
                try:
                    print(str(i['id']) + ' - ' + database.fetch(ver + '.db', 'areas', 'id=' + str(i['id']))[4])
                except:
                    print(str(i['id']) + ' - unknown')
        else:
            print(store)
        return 0
    #summon
    if args[0].lower() == 'summon' and len(farm) == 1:
        if len(args) == 3:
            if args[2] == 's' or args[2] == 'm':
                ver = farm[0][0]
                os = farm[0][1]
                token = farm[0][3]
                secret = farm[0][4]
                if args[2] == 's': course = 1
                if args[2] == 'm': course = 2
                farmbot.summon(ver, os, token, secret, args[1], course)
            else:
                print('invalid single/multi input.')
        else:
            print('ID s/m')
        return 0
    #capacity
    if args[0].lower() == 'capacity' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.capacity(ver, os, token, secret)
        if 'error' not in store:
            print(Fore.GREEN + 'box size increased by 5+')
        else:
            print(store)
        return 0
    #name
    if args[0].lower() == 'name' and len(farm) == 1:
        if len(args) == 2:
            if len(args[1]) > 0 and len(args[1]) <= 10:
                ver = farm[0][0]
                os = farm[0][1]
                token = farm[0][3]
                secret = farm[0][4]
                name = str(args[1])
                store = ingame.changeName(ver, os, token, secret, name)
                if 'error' not in store:
                    print(Fore.GREEN + 'name set as: ' + str(name))
                else:
                    print(store)
            else:
                print('name too long! (' + str(len(args[1])) + '/10)')
        else:
            print('no name provided.')
        return 0
    #stam
    if args[0].lower() == 'stam' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        farmbot.restore(ver, os, token, secret)
        return 0
    #quicksell
    if args[0].lower() == 'quicksell' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        farmbot.sell(ver, os, token, secret)
        return 0
    #wallpaper
    if args[0].lower() == 'wallpaper' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.setWallpaper(ver, os, token, secret, args[1])
            if 'error' not in store:
                print(Fore.GREEN + 'wallpaper set as: ' + str(args[1]))
            else:
                print(store)
        else:
            print('no ID provided.')
        return 0
    #box
    if args[0].lower() == 'box' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.cards(ver, os, token, secret)
        if 'error' not in store:
            lr = []
            ur = []
            ssr = []
            sr = []
            r = []
            n = []
            for i in store['cards']:
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 5:
                    element = '?'
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = Fore.CYAN + 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = Fore.GREEN + 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = Fore.MAGENTA + 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = Fore.RED + 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = Fore.YELLOW + 'PHY'
                    lr.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[14]))
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 4:
                    element = '?'
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = Fore.CYAN + 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = Fore.GREEN + 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = Fore.MAGENTA + 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = Fore.RED + 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = Fore.YELLOW + 'PHY'
                    ur.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[14]))
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 3:
                    element = '?'
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = Fore.CYAN + 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = Fore.GREEN + 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = Fore.MAGENTA + 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = Fore.RED + 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = Fore.YELLOW + 'PHY'
                    ssr.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[14]))
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 2:
                    element = '?'
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = Fore.CYAN + 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = Fore.GREEN + 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = Fore.MAGENTA + 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = Fore.RED + 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = Fore.YELLOW + 'PHY'
                    sr.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[14]))
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 1:
                    element = '?'
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = Fore.CYAN + 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = Fore.GREEN + 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = Fore.MAGENTA + 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = Fore.RED + 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = Fore.YELLOW + 'PHY'
                    r.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[14]))
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 0:
                    element = '?'
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = Fore.CYAN + 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = Fore.GREEN + 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = Fore.MAGENTA + 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = Fore.RED + 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = Fore.YELLOW + 'PHY'
                    n.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[14]))
            print(Fore.WHITE + '==== ==== > LR < ==== ====\n\n' + ',\n'.join(lr) + Fore.WHITE + '\n\n==== ==== > UR < ==== ====\n\n' + ',\n'.join(ur) + Fore.WHITE + '\n\n==== ==== > SSR < ==== ====\n\n' + ',\n'.join(ssr) + Fore.WHITE + '\n\n==== ==== > SR < ==== ====\n\n' + ',\n'.join(sr) + Fore.WHITE + '\n\n==== ==== > R < ==== ====\n\n' + ',\n'.join(r) + Fore.WHITE + '\n\n==== ==== > N < ==== ====\n\n' + ',\n'.join(n))
        else:
            print(store)
        return 0
    #streamline
    if args[0].lower() == 'streamline' and len(farm) == 1:
        if len(args) == 2:
            if args[1] == 'quests' or args[1] == 'events':
                ver = farm[0][0]
                os = farm[0][1]
                iden = farm[0][2]
                token = farm[0][3]
                secret = farm[0][4]
                farmbot.streamline(ver, os, token, secret, iden, args[1])
            else:
                print('invalid choice.')
        else:
            print('missing argument. (quests/events)')
        return 0
    #finishall
    if args[0].lower() == 'finishall' and len(farm) == 1:
        if len(args) == 2:
            if args[1] == 'quests' or args[1] == 'events':
                ver = farm[0][0]
                os = farm[0][1]
                iden = farm[0][2]
                token = farm[0][3]
                secret = farm[0][4]
                farmbot.finishall(ver, os, token, secret, iden, args[1])
            else:
                print('invalid choice.')
        else:
            print('missing argument. (quests/events)')
        return 0
    #bossrush
    if args[0].lower() == 'bossrush' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        stages = [['701001', 3], ['701001', 4], ['701002', 4], ['701002', 5], ['701003', 5], ['701004', 5], ['701005', 5], ['701006', 5], ['701007', 5], ['701008', 5]]
        for i in stages:
            farmbot.complete_stage(ver, os, token, secret, i[0], i[1], None, iden)
        print('run the mission command to accept your stones.')
        return 0
    #area
    if args[0].lower() == 'area' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            iden = farm[0][2]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.quests(ver, os, token, secret)
            if 'error' not in store:
                maps = []
                for i in store['user_areas']:
                    if int(i['area_id']) == int(args[1]):
                        for j in i['user_sugoroku_maps']:
                            if int(j['cleared_count']) == 0:
                                farmbot.complete_stage(ver, os, token, secret, str(j['sugoroku_map_id'])[:-1], str(j['sugoroku_map_id'])[-1], None, iden)
            else:
                print(store)
        else:
            print('no area ID provided.')
        return 0
    #stage
    if args[0].lower() == 'stage' and len(farm) == 1:
        if len(args) == 4:
            ver = farm[0][0]
            os = farm[0][1]
            iden = farm[0][2]
            token = farm[0][3]
            secret = farm[0][4]
            if len(args[2]) == 1:
                if int(args[3]) != 0:
                    for i in range(int(args[3]) + 1):
                        if int(i) != 0:
                            farmbot.complete_stage(ver, os, token, secret, args[1], args[2], None, iden)
                else:
                    print('can\'t run stage 0 times!')
            else:
                print('difficulty is wrong.\n0=normal || 1=hard || 2=zhard || 3=super || 4=super2')
        else:
            print('missing stage ID, difficulty, & run amount arguments.')
        return 0
    #potential
    if args[0].lower() == 'potential' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.events(ver, os, token, secret)
        if 'error' not in store:
            for i in store['events']:
                if i['id'] >= 140 and i['id'] < 145:
                    try:
                        stage = database.fetch(ver + '.db', 'sugoroku_maps', 'quest_id=' + str(i['quests'][0]['id']))[0]
                        farmbot.complete_stage(ver, os, token, secret, str(stage)[0:-1], str(stage)[-1], None, iden)
                    except:
                        print('stage does not exist.')
        else:
            print(store)
        return 0
    #hercule
    if args[0].lower() == 'hercule' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        stages = [['711001', 1], ['711002', 1], ['711003', 1], ['711004', 1], ['711005', 1], ['711006', 1]]
        for i in stages:
            farmbot.complete_stage(ver, os, token, secret, i[0], i[1], None, iden)
        return 0
    #daily
    if args[0].lower() == 'daily' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        stages = [['130001', 0], ['131001', 0], ['132001', 0]]
        for i in stages:
            farmbot.complete_stage(ver, os, token, secret, i[0], i[1], None, iden)
        store = ingame.events(ver, os, token, secret)
        if 'error' not in store:
            for i in store['events']:
                if i['id'] >= 140 and i['id'] < 145:
                    try:
                        stage = database.fetch(ver + '.db', 'sugoroku_maps', 'quest_id=' + str(i['quests'][0]['id']))[0]
                        farmbot.complete_stage(ver, os, token, secret, str(stage)[0:-1], str(stage)[-1], None, iden)
                    except:
                        print('stage does not exist.')
        else:
            print(store)
        farmbot.gift(ver, os, token, secret)
        farmbot.mission(ver, os, token, secret)
        return 0
    #omegafarm
    if args[0].lower() == 'omegafarm' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        farmbot.gift(ver, os, token, secret)
        farmbot.mission(ver, os, token, secret)
        farmbot.streamline(ver, os, token, secret, iden, 'quests')
        refresh()
        farmbot.streamline(ver, os, token, secret, iden, 'events')
        refresh()
        farmbot.complete_unfinished_ezas(ver, os, token, secret, iden)
        refresh()
        farmbot.gift(ver, os, token, secret)
        farmbot.mission(ver, os, token, secret)
        return 0
    #items
    if args[0].lower() == 'items' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.getItems(ver, os, token, secret)
        if 'error' not in store:
            print(Fore.LIGHTYELLOW_EX + '==== ==== > Support < ==== ====\n')
            for i in store['support_items']['items']:
                try:
                    print(database.fetch(ver + '.db', 'support_items', 'id=' + str(i['item_id']))[1] + ' x' + str(i['quantity']))
                except:
                    print('Support x'+ str(i['quantity']))
            print('\n' + Fore.LIGHTYELLOW_EX + '==== ==== > Training < ==== ====\n')
            for i in store['training_items']:
                try:
                    print(database.fetch(ver + '.db', 'training_items', 'id=' + str(i['training_item_id']))[1] + ' x' + str(i['quantity']))
                except:
                    print('Training x'+ str(i['quantity']))
            print('\n' + Fore.LIGHTYELLOW_EX + '==== ==== > Potential < ==== ====\n')
            for i in store['potential_items']['user_potential_items']:
                try:
                    print(database.fetch(ver + '.db', 'potential_items', 'id=' + str(i['potential_item_id']))[1] + ' x' + str(i['quantity']))
                except:
                    print('Orb x'+ str(i['quantity']))
            print('\n' + Fore.LIGHTYELLOW_EX + '==== ==== > Treasure < ==== ====\n')
            for i in store['treasure_items']['user_treasure_items']:
                try:
                    print(database.fetch(ver + '.db', 'treasure_items', 'id=' + str(i['treasure_item_id']))[1] + ' x' + str(i['quantity']))
                except:
                    print('Treasure x'+ str(i['quantity']))
            print('\n' + Fore.LIGHTYELLOW_EX + '==== ==== > Special < ==== ====\n')
            for i in store['special_items']:
                try:
                    print(database.fetch(ver + '.db', 'special_items', 'id=' + str(i['special_item_id']))[1] + ' x' + str(i['quantity']))
                except:
                    print('Special x'+ str(i['quantity']))
        else:
            print(store)
        return 0
    #medals
    if args[0].lower() == 'medals' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.getMedals(ver, os, token, secret)
        if 'error' not in store:
            for i in store['awakening_items']:
                try:
                    print(database.fetch(ver + '.db', 'awakening_items', 'id=' + str(i['awakening_item_id']))[1] + ' x' + str(i['quantity']))
                except:
                    print('unknown medal x' + str(i['quantity']))
        else:
            print(store)
        return 0
    #wallpapers
    if args[0].lower() == 'wallpapers' and len(farm) == 1:
        ver = farm[0][0]
        d = database.fetch(ver + '.db', 'wallpaper_items', None)
        for i in d:
            print('ID: ' + str(i[0]) + '\n' + i[1] + '\n' + i[2])
        return 0
    #teams
    if args[0].lower() == 'teams' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        one = []
        two = []
        three = []
        four = []
        five = []
        six = []
        store = ingame.cards(ver, os, token, secret)
        store2 = ingame.getTeams(ver, os, token, secret)
        print('Current team: ' + str(store2['selected_team_num']))
        for i in store['cards']:
            if i['id'] in store2['user_card_teams'][0]['user_card_ids']:
                element = ''
                try:
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = 'PHY'
                    one.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(i['exp']))
                except:
                    one.append('unit not in database. ' + str(i['card_id']))
            if i['id'] in store2['user_card_teams'][1]['user_card_ids']:
                element = ''
                try:
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = 'PHY'
                    two.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(i['exp']))
                except:
                    two.append('unit not in database. ' + str(i['card_id']))
            if i['id'] in store2['user_card_teams'][2]['user_card_ids']:
                element = ''
                try:
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = 'PHY'
                    three.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(i['exp']))
                except:
                    three.append('unit not in database. ' + str(i['card_id']))
            if i['id'] in store2['user_card_teams'][3]['user_card_ids']:
                element = ''
                try:
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = 'PHY'
                    four.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(i['exp']))
                except:
                    four.append('unit not in database. ' + str(i['card_id']))
            if i['id'] in store2['user_card_teams'][4]['user_card_ids']:
                element = ''
                try:
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = 'PHY'
                    five.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(i['exp']))
                except:
                    five.append('unit not in database. ' + str(i['card_id']))
            if i['id'] in store2['user_card_teams'][5]['user_card_ids']:
                element = ''
                try:
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[13]
                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                        element = 'AGL'
                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                        element = 'TEQ'
                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                        element = 'INT'
                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                        element = 'STR'
                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                        element = 'PHY'
                    six.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[24]))[1] + '],\nSA: ' + str(i['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[15]) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(i['exp']))
                except:
                    six.append('unit not in database. ' + str(i['card_id']))
        print('--- Team 1 ---\n' + ',\n'.join(one))
        print('--- Team 2 ---\n' + ',\n'.join(two))
        print('--- Team 3 ---\n' + ',\n'.join(three))
        print('--- Team 4 ---\n' + ',\n'.join(four))
        print('--- Team 5 ---\n' + ',\n'.join(five))
        print('--- Team 6 ---\n' + ',\n'.join(six))
        return 0
    #deck
    if args[0].lower() == 'deck' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            token = farm[0][3]
            secret = farm[0][4]
            if int(args[1]) >= 1 and int(args[1]) <= 6:
                store = ingame.getTeams(ver, os, token, secret)
                if 'error' not in store:
                    teams = []
                    for x in store['user_card_teams']:
                        teams.append(x)
                    store2 = ingame.setTeam(ver, os, token, secret, args[1], teams)
                    if 'error' not in store2:
                        print(Fore.GREEN + 'team set to ' + str(args[1]))
                    else:
                        print(store)
                else:
                    print(store)
            else:
                print('invalid team number.')
        else:
            print('no team number provided.')
        return 0
    #ezas
    if args[0].lower() == 'ezas' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.events(ver, os, token, secret)
        if 'error' not in store:
            for x in store['z_battle_stages']:
                try:
                    print(str(x['id']) + ' ' + database.fetch(ver + '.db', 'z_battle_stage_views', 'z_battle_stage_id=' + str(x['id']))[3] + ' - ' + database.fetch(ver + '.db', 'z_battle_stage_views', 'z_battle_stage_id=' + str(x['id']))[2])
                except:
                    print(str(x['id']) + ' - unknown')
        else:
            print(store)
        return 0
    #zlevel
    if args[0].lower() == 'zlevel' and len(farm) == 1:
        if len(args) == 3:
            ver = farm[0][0]
            os = farm[0][1]
            iden = farm[0][2]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.events(ver, os, token, secret)
            if 'error' not in store:
                eza_pool = []
                for x in store['z_battle_stages']:
                    eza_pool.append(int(x['id']))
                if int(args[1]) in eza_pool:
                    farmbot.complete_zstage(ver, os, token, secret, int(args[1]), int(args[2]), iden)
                else:
                    print(Fore.LIGHTRED_EX + 'EZA event ID not in active pool!')
            else:
                print(store)
        else:
            print('missing EZA event ID & level.')
        return 0
    #eza
    if args[0].lower() == 'eza' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            iden = farm[0][2]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.events(ver, os, token, secret)
            if 'error' not in store:
                eza_pool = []
                for x in store['z_battle_stages']:
                    eza_pool.append(int(x['id']))
                if int(args[1]) in eza_pool:
                    store = ingame.quests(ver, os, token, secret)
                    for x in store['user_z_battles']:
                        if x['z_battle_stage_id'] == int(args[1]):
                            clear_count = x['max_clear_level']
                            while int(clear_count) <= 30:
                                farmbot.complete_zstage(ver, os, token, secret, int(args[1]), int(clear_count), iden)
                                clear_count = clear_count + 1
                else:
                    print(Fore.LIGHTRED_EX + 'EZA event ID not in active pool!')
            else:
                print(store)
        else:
            print('missing EZA event ID.')
        return 0
    #alleza
    if args[0].lower() == 'alleza' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        farmbot.complete_unfinished_ezas(ver, os, token, secret, iden)
        return 0
    #list
    if args[0].lower() == 'list' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.friends(ver, os, token, secret)
        if 'error' not in store:
            print(Fore.LIGHTYELLOW_EX + '==== ==== > Friends < ==== ====\n' + Fore.WHITE)
            for i in store['friendships']:
                element = '?'
                db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[13]
                if db_ele is 0 or db_ele is 10 or db_ele is 20:
                    element = Fore.CYAN + 'AGL'
                if db_ele is 1 or db_ele is 11 or db_ele is 21:
                    element = Fore.GREEN + 'TEQ'
                if db_ele is 2 or db_ele is 12 or db_ele is 22:
                    element = Fore.MAGENTA + 'INT'
                if db_ele is 3 or db_ele is 13 or db_ele is 23:
                    element = Fore.RED + 'STR'
                if db_ele is 4 or db_ele is 14 or db_ele is 24:
                    element = Fore.YELLOW + 'PHY'
                print(str(i['id']) + ', ' + str(i['user']['name']) + ', ' + str(i['user']['rank']) + '\n' + element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[24]))[1] + '],\nSA: ' + str(i['user']['leader']['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[15]) + ', Potential: ' + str(i['user']['leader']['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['user']['leader']['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[14]))
            print(Fore.LIGHTYELLOW_EX + '==== ==== > Pending < ==== ====\n' + Fore.WHITE)
            for i in store['pending_friendships']:
                element = '?'
                db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[13]
                if db_ele is 0 or db_ele is 10 or db_ele is 20:
                    element = Fore.CYAN + 'AGL'
                if db_ele is 1 or db_ele is 11 or db_ele is 21:
                    element = Fore.GREEN + 'TEQ'
                if db_ele is 2 or db_ele is 12 or db_ele is 22:
                    element = Fore.MAGENTA + 'INT'
                if db_ele is 3 or db_ele is 13 or db_ele is 23:
                    element = Fore.RED + 'STR'
                if db_ele is 4 or db_ele is 14 or db_ele is 24:
                    element = Fore.YELLOW + 'PHY'
                print(str(i['id']) + ', ' + str(i['user']['name']) + ', ' + str(i['user']['rank']) + '\n' + element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[24]))[1] + '],\nSA: ' + str(i['user']['leader']['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[15]) + ', Potential: ' + str(i['user']['leader']['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(i['user']['leader']['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['user']['leader']['card_id']))[14]))
        else:
            print(store)
        return 0
    #search
    if args[0].lower() == 'search' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.findFriend(ver, os, token, secret, int(args[1]))
            if 'error' not in store:
                element = '?'
                db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(store['user']['leader']['card_id']))[13]
                if db_ele is 0 or db_ele is 10 or db_ele is 20:
                    element = Fore.CYAN + 'AGL'
                if db_ele is 1 or db_ele is 11 or db_ele is 21:
                    element = Fore.GREEN + 'TEQ'
                if db_ele is 2 or db_ele is 12 or db_ele is 22:
                    element = Fore.MAGENTA + 'INT'
                if db_ele is 3 or db_ele is 13 or db_ele is 23:
                    element = Fore.RED + 'STR'
                if db_ele is 4 or db_ele is 14 or db_ele is 24:
                    element = Fore.YELLOW + 'PHY'
                print(str(store['user']['id']) + ', ' + str(store['user']['name']) + ', ' + str(store['user']['rank']) + '\n' + element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(store['user']['leader']['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(store['user']['leader']['card_id']))[24]))[1] + '],\nSA: ' + str(store['user']['leader']['skill_lv']) + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(store['user']['leader']['card_id']))[15]) + ', Potential: ' + str(store['user']['leader']['released_rate']) + '%, Lvl: ' + str(database.fetch(ver + '.db', 'card_exps', 'exp_total=' + str(store['user']['leader']['exp'])))[1] + '/' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(store['user']['leader']['card_id']))[14]))
            else:
                print(store)
        else:
            print('missing user/friend ID.')
        return 0
    #friend
    if args[0].lower() == 'friend' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.addFriend(ver, os, token, secret, args[1])
            if 'error' not in store:
                print(store)
            else:
                print(store)
        else:
            print('missing user/friend ID.')
        return 0
    #accept
    if args[0].lower() == 'accept' and len(farm) == 1:
        if len(args) == 2:
            ver = farm[0][0]
            os = farm[0][1]
            token = farm[0][3]
            secret = farm[0][4]
            store = ingame.acceptFriend(ver, os, token, secret, args[1])
            if 'error' not in store:
                if 'accepted' in store['friendship']['status']:
                    print(Fore.GREEN + 'friend accepted.')
                else:
                    print(Fore.RED + 'can\'t accept.')
            else:
                print(store)
        else:
            print('missing user/friend ID.')
        return 0
    #dragonballs
    if args[0].lower() == 'dragonballs' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.dragonballs(ver, os, token, secret)
        if 'error' not in store:
            print(Fore.GREEN + '==== ==== > Shenron < ==== ====\n' + Fore.WHITE)
            for i in store['dragonball_sets']:
                if i['ball_type'] == 0:
                    for x in i['dragonballs']:
                        print(str(x['num']) + ' - collected: ' + str(x['is_got']) + ' (' + str(x['quest_id']) + ':' + str(x['difficulties'][0]) + ')')
            print(Fore.GREEN + '\n==== ==== > Porunga < ==== ====\n' + Fore.WHITE)
            for i in store['dragonball_sets']:
                if i['ball_type'] == 1:
                    for x in i['dragonballs']:
                        print(str(x['num']) + ' - collected: ' + str(x['is_got']) + ' (' + str(x['description']) + ')')
                        if 'condition' in x['mission']:
                            print(str(x['mission']['conditions']))
        else:
            print(store)
        return 0
    #wish
    if args[0].lower() == 'wish' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        token = farm[0][3]
        secret = farm[0][4]
        store = ingame.dragonballs(ver, os, token, secret)
        if 'error' not in store:
            for i in store['dragonball_sets']:
                if i['ball_type'] == 0:
                    for x in i['dragonballs']:
                        if x['is_got'] == False:
                            farmbot.complete_stage(ver, os, token, secret, str(x['quest_id']), str(x['difficulties'][0]), None, iden)
        else:
            print(store)
        return 0
    #identifier
    if args[0].lower() == 'identifier' and len(farm) == 1:
        iden = farm[0][3]
        print(iden)
        return 0
    #refresh
    if args[0].lower() == 'refresh' and len(farm) == 1:
        refresh()
        return 0
    #transfer
    if args[0].lower() == 'transfer' and len(farm) == 1:
        ver = farm[0][0]
        os = farm[0][1]
        iden = farm[0][2]
        save = farm[0][5]
        if checkTcLoop(ver, os, iden) == True:
            fs.unlink('./saves/' + str(save) + '.txt')
            farm = []
            utils.help1()
        return 1