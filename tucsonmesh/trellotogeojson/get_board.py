"""Command-line script to create GeoJSON from Trello cards for Tucson Mesh installs"""

import json
import logging
import os
import re
import sys

import requests
from trello import TrelloClient


# See https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/
API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")


def get_coordinates(description: str) -> tuple[float, float]:
    """
    Parse coordinates from a Trello card's description

    Raises ValueError if coordinates aren't present or there is some
    other parse error.

    """

    # Matches URL like
    # https://www.google.com/maps/place/BICAS/@32.246221,-110.9707685,20.36z/data=!4m6!3m5!1s0x86d6711f35286f23:0xf345ecfca1e8eda2!8m2!3d32.2462729!4d-110.9707784!16s%2Fg%2F1td00y9l?entry=ttu
    gmaps_regex = (
        # URL prefix
        r"https?:\/{2}(?:www.){0,1}google.com\/maps\/place\/"
        # Usually the place name, e.g. "BICAS"
        r".*\/"
        # The coordinates. Usually these are prefixed with a '@', but we also
        # need to check for '%40' in case the URL is encoded when it's
        # part of a parameter in a redirect that won't resolve without
        # completing a CAPTCHA, like
        # https://www.google.com/sorry/index?continue=https://www.google.com/maps/place/Everybody/%4032.25063,-110.9643449,21z/data%3D!4m6!3m5!1s0x86d6711f4fc6b1cb:0x342c112552274344!8m2!3d32.25063!4d-110.9642081!16s%252Fg%252F11cssglsq4%3Fentry%3Dtts%26shorturl%3D1&q=EgRDAaYeGP2y7LwGIjCBsbQKf-o-Mi78HUuklGFwmv1c34MVbrUNxpOUKJH0xhHvOe-nfTcoS4rTtOurahwyAXJaAUM
        r"(?:@|%40)(?P<lat>-?\d+\.\d+),(?P<lon>-?\d+\.\d+)"
    )

    # Matches URL like http://goo.gl/maps/4CgSeMNn5Ed38pSH6
    gmaps_shortened_regex = r"https?:\/{2}goo.gl\/maps\/(?P<slug>[a-zA-Z0-9]*)"

    coord_url_match = re.search(gmaps_regex, description)

    if coord_url_match:
        lat = float(coord_url_match.group("lat"))
        lon = float(coord_url_match.group("lon"))
        return lat, lon

    shortened_url_match = re.search(gmaps_shortened_regex, description)

    if shortened_url_match:
        # The URL is a Google Maps short URL -
        # something like http://goo.gl/maps/4CgSeMNn5Ed38pSH6.
        # Let's take this and follow the redirects until we get
        # the proper lat / lon
        r = requests.get(
            f"https://goo.gl/maps/{shortened_url_match.group('slug')}",
            timeout=30
        )

        coord_url_match = re.search(gmaps_regex, r.url)

        if not coord_url_match:
            raise ValueError(f"Could not parse coordinates from URL {r.url}")

        lat = float(coord_url_match.group("lat"))
        lon = float(coord_url_match.group("lon"))
        return lat, lon

    raise ValueError(
        "No link containing coordinates",
    )


def main():
    """Create GeoJSON from Trello cards for Mesh installs"""
    if API_KEY is None:
        logging.error(
            "You must specify a Trello API key in the TRELLO_API_KEY "
            "environment variable"
        )
        sys.exit(1)

    if TOKEN is None:
        logging.error(
            "You must specify a Trello authorization token in the "
            "TRELLO_TOKEN environment variable"
        )
        sys.exit(1)

    client = TrelloClient(api_key=API_KEY, token=TOKEN)

    install_board = [x for x in client.list_boards() if x.id == "63d97168f73272de7991a055"][0]

    valid_columns = {
        "63d9730582ad36a97d94a504": "Purgatory",
        "63d97280256779e2b996ab22": "Submitted Requests",
        "63d97284e43b7eadf779e1a2": "Ready for Contact & Survey",
        "63d972f119a3e4fd2c36acae": "Surveyed",
        "63d972f6ee88656e0f4c0545": "Ready for Install",
        "63d972f8255fa9c3d6b6375c": "Installed",
        "64f6835bd298f24f2e94fa46": "Needs Maintenance or realignment",
    }

    feature_list = []

    for card_column in install_board.list_lists():
        try:
            card_status = valid_columns[card_column.id]

        except KeyError:
            # Column ID isn't one of the valid ones.
            # Skip it.
            continue

        for card in card_column.list_cards():
            try:
                lat, lon = get_coordinates(card.desc)

            except ValueError as e:
                logging.warning(
                    "Could not get coordinates for card %s (%s, %s): %s",
                    card.id,
                    card_status,
                    card.name,
                    e,
                )
                continue


            feature_list.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "title": card.name,
                        "link": card.url,
                        "status": card_status
                    },
                }
            )

    json.dump(
        {"type": "FeatureCollection", "features": feature_list},
        sys.stdout,
        indent=4
    )


if __name__ == "__main__":
    main()
