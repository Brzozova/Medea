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

#Backup details view
for buuid in list(server_id_to_storage_id_map.keys()):
    url = URL_backup_details + buuid

