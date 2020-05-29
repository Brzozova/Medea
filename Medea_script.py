#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Medea - UpCloud Backup Notification Application
Python script to notify on Slack when backup was failed using UpCloud API.
"""

from requests.auth import HTTPBasicAuth
from collections import defaultdict
from socket import gethostname
import json
import requests

API_ID = 'username'
API_KEY = 'password'
URL_PATTERN = 'https://api.upcloud.com/1.3/server/'
URL_BACKUPS = 'https://api.upcloud.com/1.3/storage/backup'
URL_BACKUPS_DETAILS = 'https://api.upcloud.com/1.3/storage/'
SLACK_URL = ''

#Get list of all servers
srvlist = requests.get(URL_PATTERN, auth=HTTPBasicAuth(API_ID, API_KEY))
srvlist_json = srvlist.json()
data = srvlist.json()

#Get servers hostname and uuid
hosts = {}
for d in data['servers']['server']:
    srvhostname = d['title']
    srvuuid = d['uuid']
    hosts[srvuuid] = srvhostname

#Add server uuid to URL
#Create dictionary with storage uuid and server uuid
server_id_to_storage_id_map = {}
for id in list(hosts.keys()):
    url = URL_PATTERN + id
    print(url)
    serverdata = requests.get(url, auth=HTTPBasicAuth(API_ID, API_KEY))
    server_data = serverdata.json()
    storage_uuid = server_data['server']['storage_devices']['storage_device'][0]["storage"]
    server_id_to_storage_id_map[id] = storage_uuid

#Check all backups
backup_data = requests.get(URL_BACKUPS, auth=HTTPBasicAuth(API_ID, API_KEY))
backup_data_json = backup_data.json()
backups = backup_data.json()

#Check backups status
for b in backups['storages']['storage']:
    bkp_origin = b['origin']
    bkp_title = b['title']
    bkp_state = b['state']
    bkp_created = b['created']
    if bkp_origin:
        if bkp_title == "Scheduled Backup":
            print(bkp_origin + ' : ' + bkp_title)
            if bkp_state == "online":
                print(bkp_origin + ' was successfull backuped.')
            elif bkp_state == "maintenance":
                print(bkp_origin + ' Maintenance work is currently performed on the storage.')
            elif bkp_state == "cloning":
                print(bkp_origin + ' The storage resource is currently the clone source for another storage.')
            elif bkp_state == "backuping":
                print(bkp_origin + ' The storage resource is currently being backed up to another storage.')
            elif bkp_state == "error":
                print(bkp_origin + "The storage has encountered an error and is currently inaccessible.")
            else:
                print(bkp_origin + "Unknown state. Something went wrong.")
        else:
            continue
    else:
        print('No backups for server ' + bkp_origin)

#Backup details view
for buuid in list(server_id_to_storage_id_map.keys()):
    url = URL_backup_details + buuid


#Integration with Slack

#Payload for Slack
def create_message_payload(backup_summary):
    backup_details = ""

    message_payload = json.dumps(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ("Holly Molly @channel!\n"
                                 "Something went wrong with backup:"
                                 )
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": backup_details
                    }
                }
            ]
        }
    )

    return message_payload

def post_json_message(url, payload):
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=payload)


