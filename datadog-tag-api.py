import sys
import getopt
import re as regex
import requests
import urllib.parse as urlEncode
import json

def gentlyExit(text='Exited'):
    print(text)
    sys.exit()

# Logic Starts

baseTagAPIEndpoint = 'https://api.datadoghq.com/api/v1/tags/hosts'
baseHostAPIEndpoint = 'https://api.datadoghq.com/api/v1/hosts'
mode = 'testing'
manualConfirmText = '[Y] Yes   [N] No   (default is "N"): '
tags = None
actionList = {
    1: 'Get tags',
    2: 'Get host tags',
    3: 'Add tags to hosts',
    4: 'Update host tags',
    5: 'Remove host tags'
}
listOfActions = ''
for actionOrder, actionName in actionList.items():
    listOfActions += f'{actionOrder}: {actionName}\n\t'

scriptUsage = 'Usage: py datadog-tag-api.py [--prod]\n\nOptions:\n\t--prod\t\tRun script in Production mode'

# Read configuration

try:
    f = open('config.json', 'r')
except OSError:
    gentlyExit('Could not open/read file: "config.json"')

configuration = f.read()
f.close()
configuration = json.loads(configuration)

# Set mode - default: Testing (using testing account API)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['prod','help'])
except getopt.GetoptError:
    print('Bad option\n' + scriptUsage)
    sys.exit()

for opt, arg in opts:
    if opt == '--prod':
        mode = 'production'
    elif opt == '-h' or opt == '--help'  :
        print(scriptUsage)
        sys.exit()

headers = {
    "Content-Type": "application/json",
    "DD-API-KEY": configuration[mode]['apiKey'],
    "DD-APPLICATION-KEY": configuration[mode]['appKey']
}

# Functions

def beautifyResponse(input):
    return json.dumps(input.json(), indent=4)

def restAPIRequest(method, endPoint, headers=headers, payload=None, successCode=200, getResponse=None):
    r = requests.request(method, endPoint, headers=headers, json=payload)
    if r.status_code == successCode:
        if getResponse:
            return r
        else:
            if method == 'DELETE':
                print('success')
            else:
                print('success')
                print(beautifyResponse(r))
    else:
        print('failed')
        print(f'{r}, code {r.status_code} from api: {endPoint}')
        gentlyExit()

def getHost(filter):
    filter = urlEncode.quote(filter, safe="&")
    url = f'{baseHostAPIEndpoint}?filter={filter}'
    return restAPIRequest('GET', url, getResponse=True)

def getTagForHost(host):
    print(f'Getting tags for host: "{host}" ...')
    restAPIRequest('GET', f'{baseTagAPIEndpoint}/{host}')

def getTagForOrganization():
    print(f'Getting tags for organization ...')
    restAPIRequest('GET', baseTagAPIEndpoint)

def addTag(host, tags):
    print(f'Creating tags for host:{host} ...')
    payload = {
        "host": host,
        "tags": tags
    }
    restAPIRequest('POST', f'{baseTagAPIEndpoint}/{host}', payload=payload, successCode=201)

def updateTag(host, tags):
    print(f'Updating tags for host:{host} ...')
    payload = {
        "host": host,
        "tags": tags
    }
    restAPIRequest('PUT', f'{baseTagAPIEndpoint}/{host}', payload=payload, successCode=201)

def deleteTag(host):
    print(f'Removing tags for host:{host} ...')
    restAPIRequest('DELETE', f'{baseTagAPIEndpoint}/{host}', successCode=204)

# Welcome Text

accountName = configuration[mode]['account']
print(f'\nDatadog Tag API - {accountName}\n')

# Start

startOver = 1

while startOver:
    hosts = []
    hostsRegex = None

    action = int(input(f'List of actions \n\t{listOfActions}\nYour choice is [1-5]: '))
    
    if action != 1:
        hostsInput = input("Select Hosts (filterbytag|regex)\n example: host:azurevm,zone:apac|^azvm.*[0-9]$\n example: host:azurevm\nEnter your hosts (Leave empty to select ALL): ")
        hostsInputParts = hostsInput.split("|")
        hostsFilter = hostsInputParts[0]
        if(len(hostsInputParts) > 1):
            hostsRegex = hostsInputParts[1]

        r = getHost(hostsFilter).json()
        total = r['total_returned']

        if total:
            for host in r['host_list']:
                hostname = host['host_name']
                if hostsRegex:
                    if regex.search(hostsRegex, hostname):
                        hosts.append(hostname)
                else:
                    hosts.append(hostname)
        else:
            print("No hosts matched")
            gentlyExit()

    if action in [3, 4]:
        tags = input("Tags: ").split(",")

        for tag in tags:
            if len(tag.split(':')) != 2:
                print(f'Tag "{tag}" is invalid')
                gentlyExit()

    confirmText = f'Are you sure you want to perform this action ?\nPerforming the operation "{actionList[action]}"'

    if hosts:
        hostsList = ''
        for hostname in hosts:
            hostsList += f'\t{hostname}\n'
        confirmText += f' on hosts (total: {len(hosts)})\n{hostsList}'
    if tags:
        confirmText += f'with tags {tags}'


    confirmText += f'\n{manualConfirmText}'

    confirm = input(confirmText)

    if confirm == 'Y':
        if action == 1:
            getTagForOrganization()
        elif action == 2:
            for host in hosts:
                getTagForHost(host)
        elif action == 3:
            for host in hosts:
                addTag(host, tags)
        elif action == 4:
            for host in hosts:
                updateTag(host, tags)
        elif action == 5:
            for host in hosts:    
                deleteTag(host)
    else:
        print("Canceled")
    
    again = input(f'---\nStart over ?\n{manualConfirmText}')

    if again != 'Y':
        startOver = 0
        gentlyExit('Bye')
    else:
        print('---\n')