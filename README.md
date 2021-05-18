# Flick

A telegram bot to fetch cricket scores of ongoing live matches.

## Installation

Follow the following guidelines to setup the project.

Clone the repo with the following command   ``` git clone https://github.com/on-drive/flick.git ```

### Setup

Create a vritual enviornement ``` python3 -m venv venv ```

Activate the virtual enviornemnt ``` source venv/bin/activate ```

Install all the required dependencies ```pip install -r requirements.txt```

Run the bot with ```python app.py```

--------------

## Project Structure

The project basically has 3 files the functionaliy of all of them are listed below.

* `cric_info.py` - Fetches all data for us from https://www.espncricinfo.com/ and gives output in 2 form:
  * `match_list` - a simple string that contains all live matches formatted in a list along with index.  
  * `match_dict_list` - a list of dict containing all information about these matches.

* `app.py` - This contains the code for setting up the telegram bot to take command form users and send output acccordingly. All of it's code is refred from [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/en/stable/index.html)
* `constants.py` - This file just contains the API_KEY for our telegram bot.

### Maintainer

@abhinav72610
