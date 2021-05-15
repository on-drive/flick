import requests
import json


def get_match_details(series_id, match_id):
    match_link = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&seriesId={series_id}&matchId={match_id}&latest=true".format(
        series_id=series_id, match_id=match_id
    )
    detail_res = requests.get(match_link).text

    match_detail_data = json.loads(detail_res)["match"]

    # detail_list = [
    #     {
    #         "status_text": detail["statusText"],
    #     }
    #     for detail in match_detail_data
    # ]

    status_text = match_detail_data["statusText"]

    print(status_text)


def get_match_list():
    response = requests.get(
        "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?latest=true"
    ).text

    match_data = json.loads(response)["matches"]

    match_list = [
        {
            "match_name": match["slug"],
            "match_id": match["objectId"],
            "series_id": match["series"]["objectId"],
        }
        for match in match_data
    ]
    print("Choose any one of the following: \n")
    for i in range(0, len(match_list)):
        print(str(i) + " " + match_list[i]["match_name"])

    user_choice = int(input("\nEnter match number to get recent updates: "))

    # print(str(match_list[user_choice]["match_id"]))

    get_match_details(
        match_list[user_choice]["series_id"], match_list[user_choice]["match_id"]
    )


get_match_list()
