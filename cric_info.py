import requests
import json


def get_match_details(series_id, match_id):
    match_link = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&seriesId={series_id}&matchId={match_id}&latest=true".format(
        series_id=series_id, match_id=match_id
    )
    detail_res = requests.get(match_link).text

    match_detail_data = json.loads(detail_res)["match"]

    status_text = match_detail_data["statusText"]
    if status_text:
        return status_text
    else:
        return "No live data"


def get_match_dict_list():
    match_dict_list = []
    try:
        response = requests.get(
            "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?latest=true"
        ).text

        match_data = json.loads(response)["matches"]

        match_dict_list = [
            {
                "match_name": match["slug"],
                "match_id": match["objectId"],
                "series_id": match["series"]["objectId"],
                "team-1": match["teams"][0]["team"]["longName"],
                "team-2": match["teams"][1]["team"]["longName"],
            }
            for match in match_data
            if match["status"] == "Live"
        ]
    except Exception:
        pass    
    match_list = ""
    # print("Choose any one of the following: \n")
    for i in range(0, len(match_dict_list)):
        match_list += (
            str(i)
            + ". "
            + match_dict_list[i]["team-1"]
            + " vs "
            + match_dict_list[i]["team-2"]
            + "\n"
        )
    if match_list:
        return match_list, match_dict_list
    else: 
        return "No Live Matches", match_dict_list
