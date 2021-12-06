import requests
import re

from requests.api import get
class user:
    def __init__(self,username,id):
        self.username = username
        self.skins = {}
        self.id = id

def userSession():
    s = requests.Session()
    url = "https://auth.riotgames.com/api/v1/authorization"
    data = {"acr_values": "","claims": "","client_id": "riot-client","code_challenge": "","code_challenge_method": "","nonce": "HDewORkVWVNXvZJLwvQlzA","redirect_uri": "http://localhost/redirect","response_type": "token id_token","scope": "openid link ban lol_region"}
    response = s.post(url,json=data)
    return s

def login(s,username,password):
    data = {
        'type': 'auth',
        'username': username,
        'password': password,
    }
    url = "https://auth.riotgames.com/api/v1/authorization"
    response = s.put(url,json=data).json()
    try:
        pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        response = pattern.findall(response['response']['parameters']['uri'])[0]
    except:
        return "Wrong"
        print(response)
    access_token = response[0]
    return access_token
def ENT_token(s,authToken):
    headers = {
        'Authorization': f'Bearer {authToken}',
    }
    response = s.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}).json()
    entitlements_token = response['entitlements_token']
    return entitlements_token

def GetPUID(headers):
    url = "https://auth.riotgames.com/userinfo"
    response = requests.post(url,headers=headers).json()
    print(response)
    return [response['acct']['game_name'],response['sub']]

def main(username,password):
    session = userSession()
    authToken = login(session,username,password)
    if authToken == "Wrong":
        return "0"
    ENTtoken = ENT_token(session,authToken)
    headers = {
        'Authorization':f'Bearer {authToken}',
        'X-Riot-Entitlements-JWT' : ENTtoken,
    }
    userName = GetPUID(headers)
    return {'riotAuth':authToken,'entToken':ENTtoken,'userName':userName[0],'uid':userName[1]}
    
if __name__ == '__main__':
    main()