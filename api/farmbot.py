import requests
import config
import crypto
import json
import time
from threading import Timer
import api.ingame as ingame
import api.transfer as transfer
import api.auth as auth
import database
import commands
from colorama import init, Fore

init(autoreset=True)

def tutorial(ver, os, token, secret):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        code = config.gb_code
    else:
        code = config.jp_code
    if ver == 'gb':
        url = 'https://ishin-global.aktsk.com/tutorial/finish'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial/finish')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.put(url, data=None, headers=headers)
        print('Tutorial progress: 1/7 (Finish battle)')
        #######################2
        url = 'https://ishin-global.aktsk.com/tutorial/gasha'
        auth = crypto.mac(ver, token, secret, 'POST', '/tutorial/gasha')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print('Tutorial progress: 2/7 (Summon)')
        #######################
        url = 'https://ishin-global.aktsk.com/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        data = {'progress': 999}
        requests.put(url, data=json.dumps(data), headers=headers)
        print('Tutorial progress: 3/7 (Finish tutorial)')
        #######################
        url = 'https://ishin-global.aktsk.com/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        data = {'user': {'name': '6teen'}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print('Tutorial progress: 4/7 (Set name)')
        #######################5
        url = 'https://ishin-global.aktsk.com/missions/put_forward'
        auth = crypto.mac(ver, token, secret, 'POST', '/missions/put_forward')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print('Tutorial progress: 5/7 (Update missions)')
        #######################
        url = 'https://ishin-global.aktsk.com/apologies/accept'
        auth = crypto.mac(ver, token, secret, 'PUT', '/apologies/accept')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.put(url, data=None, headers=headers)
        print('Tutorial progress: 6/7 (Accept tutorial gifts)')
        #######################
        url = 'https://ishin-global.aktsk.com/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        data = {'user': {'is_ondemand': True}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print('Tutorial progress: 7/7 (Update user)')
        #######################
        store = ingame.user(ver, os, token, secret, False)
        j = json.dumps(store)
        store2 = transfer.create(ver, os, token, secret)
        if 'error' not in j:
            print(Fore.GREEN + str(store['user']['id']) + '\n' + store2['link_code'])
        else:
            print(store)
    else:
        url = 'https://ishin-production.aktsk.jp/tutorial/finish'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial/finish')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.put(url, data=None, headers=headers)
        print('Tutorial progress: 1/7 (Finish battle)')
        #######################2
        url = 'https://ishin-production.aktsk.jp/tutorial/gasha'
        auth = crypto.mac(ver, token, secret, 'POST', '/tutorial/gasha')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print('Tutorial progress: 2/7 (Summon)')
        #######################
        url = 'https://ishin-production.aktsk.jp/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        data = {'progress': 999}
        requests.put(url, data=json.dumps(data), headers=headers)
        print('Tutorial progress: 3/7 (Finish tutorial)')
        #######################
        url = 'https://ishin-production.aktsk.jp/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        data = {'user': {'name': '6teen'}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print('Tutorial progress: 4/7 (Set name)')
        #######################5
        url = 'https://ishin-production.aktsk.jp/missions/put_forward'
        auth = crypto.mac(ver, token, secret, 'POST', '/missions/put_forward')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print('Tutorial progress: 5/7 (Update missions)')
        #######################
        url = 'https://ishin-production.aktsk.jp/apologies/accept'
        auth = crypto.mac(ver, token, secret, 'PUT', '/apologies/accept')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.put(url, data=None, headers=headers)
        print('Tutorial progress: 6/7 (Accept tutorial gifts)')
        #######################
        url = 'https://ishin-production.aktsk.jp/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        data = {'user': {'is_ondemand': True}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print('Tutorial progress: 7/7 (Update user)')
        #######################
        store = ingame.user(ver, os, token, secret, False)
        j = json.dumps(store)
        store2 = transfer.create(ver, os, token, secret)
        if 'error' not in j:
            print(Fore.GREEN + str(store['user']['id']) + '\n' + store2['link_code'])
        else:
            print(store)

def restore(ver, os, token, secret):
    store = ingame.user(ver, os, token, secret, False)
    if int(store['user']['stone']) >= 1:
        print('refilling stamina...')
        store = ingame.actRefill(ver, os, token, secret)
        if 'error' not in store:
            print(Fore.GREEN + 'stamina restored.')
        else:
            print(store)
    else:
        print('not enough stones.')

def sell(ver, os, token, secret):
    store = ingame.cards(ver, os, token, secret)
    if 'error' not in store:
        print('gathering cards to sell...')
        store2 = ingame.getTeams(ver, os, token, secret)
        teams = []
        for x in store2['user_card_teams']:
            for j in x['user_card_ids']:
                teams.append(j)
        ids = []
        for i in store['cards']:
            if len(ids) <= 98 and i['id'] not in teams and i['is_favorite'] == False:
                # all N
                try:
                    if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 0:
                        ids.append(i['id'])
                except:
                    print('unit is not in database.')
                # all R
                try:
                    if database.fetch(ver + '.db', 'cards', 'id=' + str(i['card_id']))[6] is 1:
                        ids.append(i['id'])
                except:
                    print('unit is not in database.')
                # SR hercule
                if i['card_id'] is '1002640':
                    ids.append(i['id'])
                # SSR hercules
                if i['card_id'] is '1002630' or i['card_id'] is '1005480' or i['card_id'] is '1011480':
                    ids.append(i['id'])
        store = ingame.sell(ver, os, token, secret, ids)
        if 'error' not in store:
            print(Fore.GREEN + 'sold ' + str(len(ids)) + ' cards!')
        else:
            print(store)
    else:
        print(store)

def rewards(ver, os, token, secret, data):
    rewards = []
    if 'zeni' in data:
        rewards.append('Zeni: ' + str(data['zeni']))
    if 'gasha_point' in data:
        rewards.append('FP: ' + str(data['gasha_point']))
    if 'quest_clear_rewards' in data:
        for x in data['quest_clear_rewards']:
            if x['item_type'] == 'Point::Stone':
                rewards.append('Stone x' + str(x['amount']))
    if 'items' in data:
        for x in data['items']:
            if x['item_type'] == 'SupportItem':
                try:
                    rewards.append(database.fetch(ver + '.db', 'support_items', 'id=' + str(x['item_id']))[1] + ' x' + str(x['quantity']))
                except:
                    rewards.append('support x' + str(x['quantity']))
            if x['item_type'] == 'PotentialItem':
                try:
                    rewards.append(database.fetch(ver + '.db', 'potential_items', 'id=' + str(x['item_id']))[1] + ' x' + str(x['quantity']))
                except:
                    rewards.append('orb x' + str(x['quantity']))
            if x['item_type'] == 'TrainingItem':
                try:
                    rewards.append(database.fetch(ver + '.db', 'training_items', 'id=' + str(x['item_id']))[1] + ' x' + str(x['quantity']))
                except:
                    rewards.append('training item x' + str(x['quantity']))
            if x['item_type'] == 'AwakeningItem':
                try:
                    rewards.append(database.fetch(ver + '.db', 'awakening_items', 'id=' + str(x['item_id']))[1] + ' x' + str(x['quantity']))
                except:
                    rewards.append('medal x' + str(x['quantity']))
            if x['item_type'] == 'TreasureItem':
                try:
                    rewards.append(database.fetch(ver + '.db', 'treasure_items', 'id=' + str(x['item_id']))[1] + ' x' + str(x['quantity']))
                except:
                    rewards.append('treasure x' + str(x['quantity']))
            if x['item_type'] == 'Card':
                try:
                    element = ''
                    db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(x['item_id']))[13]
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
                    rewards.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(x['item_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(x['item_id']))[24]))[1] + '] x' + str(x['quantity']))
                except:
                    rewards.append('card x' + str(x['quantity']))
    if 'dragonballs' in data:
        for x in data['dragonballs']:
            rewards.append('Dragonball #' + str(x['num']))
    print(Fore.CYAN + ',\n'.join(rewards))

def zRewards(ver, os, token, secret, data):
    rewards = []
    if 'user' in data:
        if 'zeni' in data['user']:
            rewards.append('Zeni: ' + str(data['user']['zeni']))
        if 'gasha_point' in data['user']:
            rewards.append('FP: ' + str(data['user']['gasha_point']))
        if 'exchange_point' in data['user']:
            rewards.append('BP: ' + str(data['user']['exchange_point']))
        if 'stone' in data['user']:
            rewards.append('Stones: ' + str(1))
    if 'cards' in data:
        for x in data['cards']:
            try:
                element = ''
                db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(x['card_id']))[13]
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
                rewards.append(element + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(x['card_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(x['card_id']))[24]))[1] + '] x1')
            except:
                rewards.append('card x1')
    if 'awakening_items' in data:
        for x in data['awakening_items']:
            try:
                rewards.append(database.fetch(ver + '.db', 'awakening_items', 'id=' + str(x['awakening_item_id']))[1] + ' x' + str(x['quantity']))
            except:
                rewards.append('medal x' + str(x['quantity']))
    if 'potential_items' in data:
        for x in data['potential_items']:
            try:
                rewards.append(database.fetch(ver + '.db', 'potential_items', 'id=' + str(x['potential_item_id']))[1] + ' x' + str(x['quantity']))
            except:
                rewards.append('orb x' + str(x['quantity']))
    print(Fore.CYAN + ',\n'.join(rewards))

def gift(ver, os, token, secret):
    store = ingame.gifts(ver, os, token, secret)
    if 'error' not in store:
        presents = []
        for i in store['gifts']:
            presents.append(i['id'])
        if len(presents) != 0:
            store2 = ingame.acceptGifts(ver, os, token, secret, presents)
            if 'error' not in store2:
                print(Fore.GREEN + 'accepted ' + str(len(presents)) + ' gifts.')
            else:
                print(store2)
        else:
            print('no gifts to accept!')
    else:
        print(store)

def mission(ver, os, token, secret):
    store = ingame.missions(ver, os, token, secret)
    if 'error' not in store:
        missions = []
        db_ids = []
        accepted = []
        for i in store['missions']:
            if i['completed_at'] != None:
                missions.append(i['id'])
                db_ids.append(i['mission_id'])
        if len(missions) != 0:
            store2 = ingame.acceptMissions(ver, os, token, secret, missions)
            if 'error' not in store2:
                print(Fore.GREEN + 'claimed ' + str(len(missions)) + ' missions.')
                for i in db_ids:
                    try:
                        accepted.append(database.fetch(ver + '.db', 'missions', 'id='+str(i))[3] + '\n' + database.fetch(ver + '.db', 'mission_rewards', 'id='+str(i))[3] + ' x' + str(database.fetch(ver + '.db', 'mission_rewards', 'id='+str(i))[4]))
                    except:
                        accepted.append('unknown mission ID: ' + str(i))
                print(Fore.CYAN + ',\n'.join(accepted))
            else:
                print(store2)
                if 'already_accepted_mission_rewards' in store2['error']['code']:
                    print('you\'ve ready claimed.')
        else:
            print('no missions to claim!')
    else:
        print(store)

def summon(ver, os, token, secret, id, course):
    store = ingame.summon(ver, os, token, secret, id, course)
    if 'error' not in store:
        cards = []
        element = '?'
        rarity = '?'
        for i in store['gasha_items']:
            try:
                db_ele = database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[13]
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
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[6] is 0:
                    rarity = 'N'
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[6] is 1:
                    rarity = 'R'
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[6] is 2:
                    rarity = 'SR'
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[6] is 3:
                    rarity = 'SSR'
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[6] is 4:
                    rarity = 'UR'
                if database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[6] is 5:
                    rarity = 'LR'
                cards.append(element + ' ' + rarity + ' ' + database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[1] + ' [' + database.fetch(ver + '.db', 'leader_skills', 'id=' + str(database.fetch(ver + '.db', 'cards', 'id=' + str(i['item_id']))[24]))[1] + '] x' + str(i['quantity']))
            except:
                cards.append('unknown (' + str(i['item_id']) + ') x' + str(i['quantity']))
        print(',\n'.join(cards))
    else:
        print(store)

def complete_stage(ver, os, token, secret, stage, difficulty, kagi, iden):
    if stage != None and difficulty != None:
        # fetch area & stage name
        try:
            if len(stage) >= 6:
                area = database.fetch(ver + '.db', 'areas', 'id=' + str(stage[0:3]))[4]
                name = database.fetch(ver + '.db', 'quests', 'id=' + str(stage)[0:6])[2]
            else:
                if len(stage) == 5:
                    area = database.fetch(ver + '.db', 'areas', 'id=' + str(stage[0:2]))[4]
                    name = database.fetch(ver + '.db', 'quests', 'id=' + str(stage)[0:5])[2]
                else:
                    area = database.fetch(ver + '.db', 'areas', 'id=' + str(stage[0:1]))[4]
                    name = database.fetch(ver + '.db', 'quests', 'id=' + str(stage)[0:4])[2]
            match = str(area) + ' - ' + str(name) + ' (' + str(stage) + ':' + str(difficulty) + ')'
        except:
            area = 'unknown'
            name = 'unknown'
            match = str(name) + ' (' + str(stage) + ':' + str(difficulty) + ')'
        print(Fore.LIGHTYELLOW_EX + match)
        # pre define
        paces = []
        defeated = []
        # support unit
        store = ingame.getSupports(ver, os, token, secret, stage, difficulty)
        if 'error' not in store:
            difficulties = ['normal', 'hard', 'very_hard', 'super_hard1', 'super_hard2', 'super_hard3']
            if 'cpu_supporters' in store:
                if str(difficulties[int(difficulty)]) in store['cpu_supporters']:
                    if store['cpu_supporters'][str(difficulties[int(difficulty)])]['is_cpu_only'] == True:
                        if len(store['cpu_supporters'][str(difficulties[int(difficulty)])]['cpu_friends']) >= 1:
                            friend = store['cpu_supporters'][str(difficulties[int(difficulty)])]['cpu_friends'][0]['id']
                            friend_card = store['cpu_supporters'][str(difficulties[int(difficulty)])]['cpu_friends'][0]['card_id']
                        else:
                            #use friend supports if no CPUs
                            friend = store['supporters'][0]['id']
                            friend_card = store['supporters'][0]['leader']['card_id']
                    else:
                        #use friend supports if CPUs not allowed
                        friend = store['supporters'][0]['id']
                        friend_card = store['supporters'][0]['leader']['card_id']
                else:
                    #use friend supports if there's no CPUs in list
                    friend = store['supporters'][0]['id']
                    friend_card = store['supporters'][0]['leader']['card_id']
            else:
                #use friend supports if no CPU supports period
                friend = store['supporters'][0]['id']
                friend_card = store['supporters'][0]['leader']['card_id']
            # time stage clear
            timer_start = int(round(time.time(), 0))
            # start stage
            store = ingame.startStage(ver, os, token, secret, stage, difficulty, friend, friend_card)
            if 'error' not in store:
                data = crypto.decrypt_sign(store['sign'])
                stoken = data['token']
                for i in data['sugoroku']['events']:
                    paces.append(int(i))
                    if 'battle_info' in data['sugoroku']['events'][i]['content']:
                        for j in data['sugoroku']['events'][i]['content']['battle_info']:
                            defeated.append(j['round_id'])
                # finish stage
                store = ingame.finishStage(ver, os, token, secret, stage, difficulty, paces, defeated, stoken)
                if 'error' not in store:
                    timer_finish = int(round(time.time(), 0))
                    timer_total = timer_finish - timer_start
                    print(Fore.GREEN + 'completed: ' + name + ' in ' + str(timer_total) + ' seconds.')
                    data = crypto.decrypt_sign(store['sign'])
                    rewards(ver, os, token, secret, data)
                    #sell(ver, os, token, secret)
                else:
                    print('finish - ' + str(store))
            else:
                print('start - ' + str(store))
                if 'act_is_not_enough' in store['error']['code']:
                    restore(ver, os, token, secret)
                    complete_stage(ver, os, token, secret, stage, difficulty, kagi, crypto.basic(iden.replace('\n', '')))
                if 'the_number_of_cards_must_be_less_than_or_equal_to_the_capacity' in store['error']['code']:
                    sell(ver, os, token, secret)
                    complete_stage(ver, os, token, secret, stage, difficulty, kagi, crypto.basic(iden.replace('\n', '')))
                if 'no_condition_to_try_the_quest_is_fulfilled' in store['error']['code']:
                    print('this area is not unlocked or found!')
                if 'invalid_area_conditions_potential_releasable' in store['error']['code']:
                    print(Fore.LIGHTRED_EX + 'potential isn\'t unlocked!')
                if 'active_record/record_not_found' in store['error']['code']:
                    print(Fore.LIGHTRED_EX + 'stage not active or found!')
        else:
            print('support - ' + str(store))
            if 'invalid_token' in store['error']:
                    commands.refresh()
                    token = commands.farm[0][3]
                    secret = commands.farm[0][4]
                    complete_stage(ver, os, token, secret, stage, difficulty, kagi, crypto.basic(iden.replace('\n', '')))

def complete_zstage(ver, os, token, secret, eza, level, iden):
    if len(str(eza)) >= 1:
        try:
            area = database.fetch(ver + '.db', 'z_battle_stage_views', 'z_battle_stage_id=' + str(eza))[3]
        except:
            area = 'unknown #' + str(eza)
    print(Fore.LIGHTYELLOW_EX + str(area) + ' EZA - Level ' + str(level))
    em_hp = []
    em_atk = 0
    # support unit
    store = ingame.zSupports(ver, os, token, secret, eza)
    if 'error' not in store:
        friend = store['supporters'][0]['id']
        friend_card = store['supporters'][0]['leader']['card_id']
        timer_start = int(round(time.time(), 0))
        # start stage
        store = ingame.zStart(ver, os, token, secret, eza, level, friend, friend_card)
        if 'error' not in store:
            dec_sign = crypto.decrypt_sign(store['sign'])
            for i in dec_sign['enemies'][0]:
                em_hp.append(i['hp'])
                em_atk = int(em_atk) + int(i['attack'])
            stoken = dec_sign['token']
            # finish stage
            store = ingame.zFinish(ver, os, token, secret, eza, level, stoken, em_atk, em_hp)
            if 'error' not in store:
                timer_finish = int(round(time.time(), 0))
                timer_total = timer_finish - timer_start
                print(Fore.GREEN + 'completed level: ' + str(level) + ' in ' + str(timer_total) + ' seconds.')
                dec_sign = crypto.decrypt_sign(store['sign'])
                zRewards(ver, os, token, secret, dec_sign['user_items'])
            else:
                print('finish - ' + str(store))
        else:
            print('start - ' + str(store))
            if 'z_battle_check_point_does_not_exist' in store['error']['code']:
                print(Fore.LIGHTRED_EX + 'you haven\'t reached this level yet!')
    else:
        print('support - ' + str(store))
        if 'invalid_token' in store['error']:
            commands.refresh()
            token = commands.farm[0][3]
            secret = commands.farm[0][4]
            complete_zstage(ver, os, token, secret, eza, level, iden)

def complete_unfinished_quests(ver, os, token, secret, iden):
    store = ingame.user(ver, os, token, secret, False)
    if 'error' not in store:
        if int(store['user']['stone']) >= 1:
            areas = ingame.quests(ver, os, token, secret)
            # user_areas -> area_id -> user_sugoroku_maps -> sugoroku_map_id, cleared_count
            maps = []
            for i in areas['user_areas']:
                if i['area_id'] <= 27:
                    for j in i['user_sugoroku_maps']:
                        if j['cleared_count'] == 0:
                            maps.append(j['sugoroku_map_id'])
            if len(maps) == 0:
                print('no quests to complete.')
            else:
                if len(maps) == 15:
                    f = open('quests.txt', 'r')
                    content = f.read()
                    f.close()
                    quests = content.split('\n')
                    for i in quests:
                        complete_stage(ver, os, token, secret, str(i)[:-1], str(i)[-1], None, crypto.basic(iden.replace('\n', '')))
                else:
                    for map in maps:
                        complete_stage(ver, os, token, secret, str(map)[:-1], str(map)[-1], None, crypto.basic(iden.replace('\n', '')))
                    i = 0
                    while 1 == 0:
                        areas = ingame.quests(ver, os, token, secret)
                        maps_check = []
                        for user in areas['user_areas']:
                            for map in user['user_sugoroku_maps']:
                                if map['cleared_count'] == 0 and map['sugoroku_map_id'] < 999999 and map['sugoroku_map_id'] > 100:
                                    maps_check.append(map)
                        if maps_check == maps:
                            i = 1
                        else:
                            maps = maps_check
                            commands.refresh()
        else:
            print('not enough stones.')
    else:
        print(store)

def complete_unfinished_events(ver, os, token, secret, iden):
    store = ingame.user(ver, os, token, secret, False)
    if 'error' not in store:
        if int(store['user']['stone']) >= 1:
            events = ingame.events(ver, os, token, secret)
            if 'error' not in events:
                event_ids = []
                for event in events['events']:
                    event_ids.append(event['id'])
                event_ids = sorted(event_ids)
                try:
                    event_ids.remove(135)
                except:
                    None
                ### Complete areas if they are in the current ID pool
                areas = ingame.quests(ver, os, token, secret)
                i = 1
                for area in areas['user_areas']:
                    if area['area_id'] in event_ids:
                        for stage in area['user_sugoroku_maps']:
                            if stage['cleared_count'] == 0:
                                act = database.fetch(ver + '.db', 'sugoroku_maps', 'id=' + str(stage['sugoroku_map_id']))[7]
                                if int(store['user']['act']) <= int(act):
                                    store = ingame.actRefill(ver, os, token, secret)
                                    if 'error' not in store:
                                        complete_stage(ver, os, token, secret, str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1], None, crypto.basic(iden.replace('\n', '')))
                                    else:
                                        commands.refresh()
                                else:
                                    complete_stage(ver, os, token, secret, str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1], None, crypto.basic(iden.replace('\n', '')))
                                i+=1
                    if i % 30 == 0:
                        commands.refresh()
            else:
                print(events)
        else:
            print('not enough stones.')
    else:
        print(store)

def complete_unfinished_ezas(ver, os, token, secret, iden):
    store = ingame.events(ver, os, token, secret)
    if 'error' not in store:
        eza_pool = []
        for x in store['z_battle_stages']:
            eza_pool.append(int(x['id']))
        store = ingame.quests(ver, os, token, secret)
        for i in eza_pool:
            for x in store['user_z_battles']:
                if int(x['z_battle_stage_id']) == int(i):
                    clear_count = int(x['max_clear_level'])
                    if clear_count == 0:
                        clear_count = clear_count + 1
                    while int(clear_count) <= 30:
                        if clear_count != 0:
                            complete_zstage(ver, os, token, secret, int(i), int(clear_count), iden)
                            clear_count = clear_count + 1
    else:
        print(store)

def streamline(ver, os, token, secret, iden, which):
    if which == 'quests':
        complete_unfinished_quests(ver, os, token, secret, iden)
    if which == 'events':
        complete_unfinished_events(ver, os, token, secret, iden)

def finishall(ver, os, token, secret, iden, which):
    store = ingame.user(ver, os, token, secret, False)
    if 'error' not in store:
        if int(store['user']['stone']) >= 1:
            if which == 'quests':
                f = open('quests.txt', 'r')
                content = f.read()
                f.close()
                quests = content.split('\n')
                for i in quests:
                    act = database.fetch(ver + '.db', 'sugoroku_maps', 'id=' + str(i))[7]
                    if int(store['user']['act']) <= int(act):
                        store = ingame.actRefill(ver, os, token, secret)
                        if 'error' not in store:
                            complete_stage(ver, os, token, secret, str(i)[:-1], str(i)[-1], None, crypto.basic(iden.replace('\n', '')))
                        else:
                            commands.refresh()
                    else:
                        complete_stage(ver, os, token, secret, str(i)[:-1], str(i)[-1], None, crypto.basic(iden.replace('\n', '')))
            if which == 'events':
                events = ingame.events(ver, os, token, secret)
                event_ids = []
                for event in events['events']:
                    event_ids.append(event['id'])
                event_ids = sorted(event_ids)
                try:
                    event_ids.remove(135)
                except:
                    None
                ### Complete areas if they are in the current ID pool
                areas = ingame.quests(ver, os, token, secret)
                i = 1
                for area in areas['user_areas']:
                    if area['area_id'] in event_ids:
                        for stage in area['user_sugoroku_maps']:
                            act = database.fetch(ver + '.db', 'sugoroku_maps', 'id=' + str(stage['sugoroku_map_id']))[7]
                            if int(store['user']['act']) <= int(act):
                                store = ingame.actRefill(ver, os, token, secret)
                                if 'error' not in store:
                                    complete_stage(ver, os, token, secret, str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1], None, crypto.basic(iden.replace('\n', '')))
                                else:
                                    commands.refresh()
                            else:
                                complete_stage(ver, os, token, secret, str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1], None, crypto.basic(iden.replace('\n', '')))
                            i+=1
                    if i % 30 == 0:
                        commands.refresh()
        else:
            print('not enough stones.')
    else:
        print(store)