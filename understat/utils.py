import codecs
import json
import re
import requests
from bs4 import BeautifulSoup

from understat.constants import PATTERN


def to_league_name(league_name):
    """Maps league name to the league name used by Understat for ease of use.
    """

    league_mapper = {
        "epl": "EPL",
        "la_liga": "La_liga",
        "bundesliga": "Bundesliga",
        "serie_a": "Serie_A",
        "ligue_1": "Ligue_1",
        "rfpl": "RFPL"
    }
    try:
        return league_mapper[league_name]
    except KeyError:
        return league_name


def fetch(url):
    response = requests.get(url)
    return response.text


def find_match(scripts, pattern):
    """Returns the first match found in the given scripts."""

    for script in scripts:
        match = re.search(pattern, script.string)
        if match:
            break

    return match


def decode_data(match):
    """Returns data in the match's first group decoded to JSON."""

    byte_data = codecs.escape_decode(match.group(1))
    json_data = json.loads(byte_data[0].decode("utf-8"))

    return json_data

def get_data(url, data_type):
    """Returns data from the given URL of the given data type."""

    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")

    pattern = re.compile(PATTERN.format(data_type))
    match = find_match(scripts, pattern)
    data = decode_data(match)

    return data


def filter_data(data, options):
    """Filters the data by the given options."""
    if not options:
        return data

    return [item for item in data if
            all(key in item and options[key] == item[key]
                for key in options.keys())]


def filter_by_positions(data, positions):
    """Filter data by positions."""
    relevant_stats = []

    for position, stats in data.items():
        if not positions or position in positions:
            stats["position"] = position
            relevant_stats.append(stats)

    return relevant_stats
