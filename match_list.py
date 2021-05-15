import requests
import json


headers = {
    'authority': 'hs-consumer-api.espncricinfo.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://www.espncricinfo.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.espncricinfo.com/',
    'accept-language': 'en-US,en;q=0.9',
}

params = (
    ('latest', 'true'),
)

response = requests.get('https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
response = requests.get('https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?latest=true', headers=headers).text

match_data = json.loads(response)["matches"]

match_list = [{
                "match_name": match["slug"],
                "match_id": match["objectId"],
                "series_id" : match["series"]["objectId"],
            } for match in match_data]

print(match_list)



