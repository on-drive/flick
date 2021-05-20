import requests
import json


def get_match_details(series_id, match_id):
    match_link = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&seriesId={series_id}&matchId={match_id}&latest=true".format(
        series_id=series_id, match_id=match_id
    )
    detail_res = requests.get(match_link).text

    match_detail_data = json.loads(detail_res)["match"]

    status_text = match_detail_data["statusText"]
    team_1_score = match_detail_data["teams"][0]["score"]
    team_2_score = match_detail_data["teams"][1]["score"]
    team_1_name = match_detail_data["teams"][0]["team"]["name"]
    team_2_name = match_detail_data["teams"][1]["team"]["name"]
    # team_1_abv = match_detail_data["teams"][0]["team"]["abbreviation"]
    # team_2_abv = match_detail_data["teams"][1]["team"]["abbreviation"]
    try:
        team_1_inning = int(match_detail_data["teams"][0]["inningNumbers"][0])
    except:
        team_1_inning = None
    try:
        team_2_inning = int(match_detail_data["teams"][1]["inningNumbers"][0])
    except:
        team_2_inning = None
    format = match_detail_data["format"]

    match_name = team_1_name + " vs " + team_2_name
    # print(
    #     status_text,
    #     team_1_score,
    #     team_2_score,
    #     team_1_name,
    #     team_2_name,
    #     team_1_inning,
    #     team_2_inning,
    #     format,
    # )

    # team_1_scrcard = team_1_abv + " - " + team_1_score
    # team_2_scrcard = team_2_abv + " - " + team_2_score
    if format == "TEST":
        if (
            match_name
            and team_1_score
            and team_2_score
            and status_text
            and team_1_inning
            and team_2_inning
        ):
            string = (
                match_name
                + "\n"
                + team_1_name
                + " "
                + str(team_1_inning)
                + "inning"
                + " - "
                + team_1_score
                + "\n"
                + team_2_name
                + " "
                + str(team_2_inning)
                + "inning"
                + " - "
                + team_2_score
                + "\n"
                + status_text
            )
            return string
        elif (
            match_name
            and team_1_score
            and status_text
            and team_1_inning
            and team_2_score == None
            and team_2_inning == None
        ):
            string = (
                match_name
                + "\n"
                + team_1_name
                + " "
                + str(team_1_inning)
                + "inning"
                + " - "
                + team_1_score
                + "\n"
                + status_text
            )
            return string

        elif (
            match_name
            and team_1_score == None
            and team_2_score
            and status_text
            and team_1_inning == None
            and team_2_inning
        ):
            string = (
                match_name
                + "\n"
                + team_2_name
                + " "
                + str(team_2_inning)
                + "inning"
                + " - "
                + team_2_score
                + "\n"
                + status_text
            )
            return string

        elif (
            match_name
            and team_1_score == None
            and team_2_score == None
            and status_text
            and team_1_inning == None
            and team_2_inning == None
        ):
            string = match_name + "\n" + status_text
            return string

    else:
        if match_name and team_1_score and team_2_score and status_text:
            string = (
                match_name
                + "\n"
                + team_1_name
                + " - "
                + team_1_score
                + "\n"
                + team_2_name
                + " - "
                + team_2_score
                + "\n"
                + status_text
            )
            return string

        elif team_2_score == None and status_text and match_name:
            string = (
                match_name
                + "\n"
                + team_1_name
                + " - "
                + team_1_score
                + "\n"
                + status_text
            )
            return string
        elif team_1_score == None and status_text and match_name:
            return (
                match_name
                + "\n"
                + team_2_name
                + " - "
                + team_2_score
                + "\n"
                + status_text
            )
        else:
            return "No Live Data"
        # return status_text


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
