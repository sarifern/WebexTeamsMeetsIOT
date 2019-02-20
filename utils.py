import requests
import json
import sys
import subprocess
import requests
from bot import bearer

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}
def send_spark_get(url, payload=None,js=True):
    global headers
    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request


def send_spark_post(url, data):
    global headers
    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request
    
