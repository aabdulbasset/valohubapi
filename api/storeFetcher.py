import requests
def translateSkins(skinList):
    skinsDict = {}
    for item in skinList:
        url = f"https://valorant-api.com/v1/weapons/skinlevels/{item}"
        response = requests.get(url).json()
        response = response['data']
        skinsDict[response['displayName']] = response['displayIcon']
    return skinsDict
def main(authToken,entToken,unique):
    url = f"https://pd.eu.a.pvp.net/store/v2/storefront/{unique}"
    headers = {
        'Authorization':f'Bearer {authToken}',
        'X-Riot-Entitlements-JWT' : entToken,
    }
    skins = requests.get(url,headers=headers).json()
    skinsDict = translateSkins(skins['SkinsPanelLayout']['SingleItemOffers'])
    return skinsDict
if __name__ == "__main__":
    main()