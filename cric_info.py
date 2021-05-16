import requests
import json


def get_match_details(series_id, match_id):
    match_link = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&seriesId={series_id}&matchId={match_id}&latest=true".format(
        series_id=series_id, match_id=match_id
    )
    detail_res = requests.get(match_link).text

    match_detail_data = json.loads(detail_res)["match"]

    status_text = match_detail_data["statusText"]
    # print(status_text)
    if status_text:
        return status_text
    else:
        return "no live data"


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
            "team-1": match["teams"][0]["team"]["longName"],
            "team-2": match["teams"][1]["team"]["longName"],
        }
        for match in match_data
        if match["status"] == "Live"
    ]
    xyx = ""
    print("Choose any one of the following: \n")
    for i in range(0, len(match_list)):
        xyx += (
            str(i)
            + ". "
            + match_list[i]["team-1"]
            + " vs "
            + match_list[i]["team-2"]
            + "\n"
        )

    return xyx, match_list
