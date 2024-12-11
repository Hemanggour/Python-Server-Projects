import json
from . import getPath

def api(apiName):
    api = ''
    with open(getPath.getPath("APIs.json")) as file:
        api = json.load(file)[apiName]
    return api

def mail(email=False, password=False):
    res=''
    if email:
        with open(getPath.getPath("APIs.json")) as file:
            res = json.load(file)['email']
        return res
    if password:
        with open(getPath.getPath("APIs.json")) as file:
            res = json.load(file)['emailPassword']
        return res
    return None