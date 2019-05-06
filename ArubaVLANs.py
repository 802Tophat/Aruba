import requests
import json
import argparse
from pprint import pprint
import urllib3

# Surpress error messages for controllers without SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, help="Controller IP address")
parser.add_argument('--user', type=str, help="Username")
parser.add_argument('--password', type=str, help="Password")
parser.add_argument('--vlan', type=str, help="VLAN")
args = parser.parse_args()

# Log into Aruba Controller and retrieve UIDARUBA for API access
r = requests.get(url='https://' + args.ip + ':4343/v1/api/login?username=' \
+ args.user +'&password=' + args.password, verify=False)
logindata = r.json()
uid = logindata['_global_result']['UIDARUBA']
cookies = {'SESSION': uid}
print("Our UID for this sessions is: " + uid)

# GET API to retrieve what VLANs are active on the controller
print("Retreiving Existing VLAN Information \n")
getvlan_id = requests.get(url="https://" + args.ip + ":4343/v1/configuration/object/vlan_id?config_path=%2Fmm&UIDARUBA=" + uid, verify=False, cookies=cookies)
vlandata = getvlan_id.json()
pprint(vlandata, indent=3)

# POST API to create a new VLAN
print("Creating VLAN: " + args.vlan)
body = {'id': args.vlan}
headers = {'content-type': 'application/json'}
postvlan_id = requests.post(url='https://' + args.ip + ":4343/v1/configuration/object/vlan_id?config_path=%2Fmm&UIDARUBA=" + uid, data=json.dumps(body), headers=headers, verify=False, cookies=cookies)
print(postvlan_id)

# POST API to save the configuration
print("Saving Configuration")
w = requests.post(url="https://" + args.ip + ":4343/v1/configuration/object/write_memory?config_path=%2Fmm&UIDARUBA=" + uid, verify=False, cookies=cookies)
print("Complete!")

# Get API to retrieve the updated VLAN list
print("Retreiving Existing VLAN Information \n")
getvlan_id = requests.get(url="https://" + args.ip + ":4343/v1/configuration/object/vlan_id?config_path=%2Fmm&UIDARUBA=" + uid, verify=False, cookies=cookies)
vlandata = getvlan_id.json()
pprint(vlandata, indent=3)
