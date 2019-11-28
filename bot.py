import sys
import os as fs
import commands
from colorama import init, Fore
import utils

init(autoreset=True)

utils.createSaves()

def getInput():
    while True:
        if commands.Handler(input()) == 0:
            print(Fore.LIGHTYELLOW_EX + 'type "help" for a list of commands.')
            getInput()
        if commands.Handler(input()) == 1:
            getInput()

print(Fore.YELLOW + 'fetching version(s)...')
utils.getVersionCodes()
print(Fore.YELLOW + 'connecting to akatsuki server(s)...')
if utils.checkServers('gb') and utils.checkServers('jp'):
    utils.help1()
    getInput()
else:
    print('can\'t reach servers. check your connection.')