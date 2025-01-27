import os
import re
import json

import requests
from trello import TrelloClient

GMAPS_REGEX = r"https?:\/{2}(?:www.google.com\/maps\/place\/.*\/@(\d+\.\d+\,\-\d+\.\d+)|goo.gl\/maps\/([a-zA-Z0-9]*))"

# Comes from trello_env.sh
api_key = os.getenv("TRELLO_API_KEY")
token   = os.getenv("TRELLO_TOKEN")

client = TrelloClient(api_key=api_key, token=token)

def main():
    install_board = [x for x in client.list_boards() if x.id == "63d97168f73272de7991a055"][0]

    valid_columns = {
        "63d9730582ad36a97d94a504": "Purgatory",
        "63d97280256779e2b996ab22": "Submitted Requests",
        "63d97284e43b7eadf779e1a2": "Ready for Contact & Survey",
        "63d972f119a3e4fd2c36acae": "Surveyed",
        "63d972f6ee88656e0f4c0545": "Ready for Install",
        "63d972f8255fa9c3d6b6375c": "Installed",
    }

    feature_list = []

    for card_column in install_board.list_lists():
        if card_column.id in valid_columns:
            card_status = valid_columns[card_column.id]

            for card in card_column.list_cards():

                coord_regex_result = re.findall(GMAPS_REGEX, card.desc)

                if coord_regex_result:

                    last_entry = coord_regex_result[-1]

                    if last_entry[0]:
                        lat_lon_str = last_entry[0]

                    # if this matches our second regex pattern, not our first, it's
                    # a google maps short URL- something like http://goo.gl/maps/4CgSeMNn5Ed38pSH6.
                    # let's take this and follow the redirects until we get the proper lat / lon
                    else:
                        r = requests.get(f"https://goo.gl/maps/{last_entry[1]}")

                        try:
                            lat_lon_str = re.findall(GMAPS_REGEX, r.url)[0][0]
                        except IndexError as e:
                            print(e)

                    lat, lon = [float(n) for n in lat_lon_str.split(",")]

                else:
                    print(f"No geocode link found for card {card.id} ({card_status}, {card.name})")

                if coord_regex_result:
                    feature_list.append(
                        {
                            "type": "Feature",
                            "geometry": {"type": "Point", "coordinates": [lon, lat]},
                            "properties": {"title": card.name, "link": card.url, "status": card_status},
                        }
                    )

    with open("out.geojson", "w") as outfile:
        json.dump(
            {"type": "FeatureCollection", "features": feature_list}, outfile, indent=4
        )


if __name__ == "__main__":
    main()

