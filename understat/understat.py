from understat.constants import (BASE_URL, LEAGUE_URL, MATCH_URL, PLAYER_URL,
                                 TEAM_URL)
from understat.utils import (filter_by_positions, filter_data, get_data,
                             to_league_name)


class Understat():
    # def __init__(self):
    #     self.session = session

    def get_stats(self, options=None, **kwargs):
        """Returns a list containing stats of every league, grouped by month.

        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of dictionaries.
        :rtype: list
        """

        stats = get_data(BASE_URL, "statData")

        if options:
            kwargs = options

        filtered_data = filter_data(stats, kwargs)

        return filtered_data

    def get_teams(self, league_name, season, options=None, **kwargs):
        """Returns a list containing information about all the teams in
        the given league in the given season.

        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :type season: str or int
        :return: A list of the league's table as seen on Understat's
            league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        teams_data = get_data(url, "teamsData")

        if options:
            kwargs = options

        filtered_data = filter_data(list(teams_data.values()), kwargs)

        return filtered_data

    def get_league_players(
            self, league_name, season, options=None, **kwargs):
        """Returns a list containing information about all the players in
        the given league in the given season.

        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :type season: str or int
        :return: A list of the players as seen on Understat's league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        players_data = get_data(url, "playersData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

    def get_league_results(
            self, league_name, season, options=None, **kwargs):
        """Returns a list containing information about all the results
        (matches) played by the teams in the given league in the given season.

        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :type season: str or int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: A list of the results as seen on Understat's league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        dates_data = get_data(url, "datesData")
        results = [r for r in dates_data if r["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(results, kwargs)

        return filtered_data

    def get_league_fixtures(
            self, league_name, season,  options=None, **kwargs):
        """Returns a list containing information about all the upcoming
        fixtures of the given league in the given season.

        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :type season: str or int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: A list of the fixtures as seen on Understat's league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        dates_data = get_data(url, "datesData")
        fixtures = [f for f in dates_data if not f["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(fixtures, kwargs)

        return filtered_data

    def get_league_table(self, league_name, season, with_headers=True):
        """Returns the latest league table of a specified league in a specified year.

        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :type season: str or int
        :param with_headers: whether or not to include headers in the returned table.
        :type with_headers: bool
        :return: List of lists.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        stats = get_data(url, "teamsData")

        keys = ["wins", "draws", "loses", "scored", "missed",
                "pts", "xG", "npxG", "xGA", "npxGA", "npxGD", "xpts"]
        team_ids = [x for x in stats]

        data = [
            [stats[team_id]["title"], len(stats[team_id]["history"])] +
            [round(sum(x[key] for x in stats[team_id]["history"]), 2)
             for key in keys]
            for team_id in team_ids
        ]

        # sort by pts descending, followed by goal difference descending
        data = sorted(data, key=lambda x: (-x[7], x[6] - x[5]))

        if with_headers:
            data = [["Team", "M", "W", "D", "L", "G", "GA", "PTS", "xG",
                     "NPxG", "xGA", "NPxGA", "NPxGD", "xPTS"]] + data

        return data

    def get_player_shots(self, player_id, options=None, **kwargs):
        """Returns the player with the given ID's shot data.

        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the player's shot data.
        :rtype: list
        """

        url = PLAYER_URL.format(player_id)
        shots_data = get_data(url, "shotsData")

        if options:
            kwargs = options

        filtered_data = filter_data(shots_data, kwargs)

        return filtered_data

    def get_player_matches(self, player_id, options=None, **kwargs):
        """Returns the player with the given ID's matches data.

        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the player's matches data.
        :rtype: list
        """
        url = PLAYER_URL.format(player_id)
        matches_data = get_data(url, "matchesData")

        if options:
            kwargs = options

        filtered_data = filter_data(matches_data, kwargs)

        return filtered_data

    def get_player_stats(self, player_id, positions=None):
        """Returns the player with the given ID's min / max stats, per
        position(s).

        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :param positions: Positions to filter the data by, defaults to None.
        :param positions: list, optional
        :return: List of the player's stats per position.
        :rtype: list
        """
        url = PLAYER_URL.format(player_id)
        player_stats = get_data(url, "minMaxPlayerStats")

        player_stats = filter_by_positions(player_stats, positions)

        return player_stats

    def get_player_grouped_stats(self, player_id):
        """Returns the player with the given ID's grouped stats (as seen at
        the top of a player's page).

        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :return: Dictionary of the player's grouped stats.
        :rtype: dict
        """
        url = PLAYER_URL.format(player_id)
        player_stats = get_data(url, "groupsData")

        return player_stats

    def get_team_stats(self, team_name, season):
        """Returns a team's stats, as seen on their page on Understat, in the
        given season.

        :param team_name: A team's name, e.g. Manchester United.
        :type team_name: str
        :param season: A season / year, e.g. 2018.
        :type season: int or str
        :return: A dictionary containing a team's stats.
        :rtype: dict
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        team_stats = get_data(url, "statisticsData")

        return team_stats

    def get_team_results(
            self, team_name, season, options=None, **kwargs):
        """Returns a team's results in the given season.

        :param team_name: A team's name.
        :type team_name: str
        :param season: The season.
        :type season: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the team's results in the given season.
        :rtype: list
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        dates_data = get_data(url, "datesData")
        results = [r for r in dates_data if r["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(results, kwargs)

        return filtered_data

    def get_team_fixtures(
            self, team_name, season, options=None, **kwargs):
        """Returns a team's upcoming fixtures in the given season.

        :param team_name: A team's name.
        :type team_name: str
        :param season: The season.
        :type season: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the team's upcoming fixtures in the given season.
        :rtype: list
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        dates_data = get_data(url, "datesData")
        fixtures = [f for f in dates_data if not f["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(fixtures, kwargs)

        return filtered_data

    def get_team_players(
            self, team_name, season, options=None, **kwargs):
        """Returns a team's player statistics in the given season.

        :param team_name: A team's name.
        :type team_name: str
        :param season: The season.
        :type season: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the team's players' statistics in the given season.
        :rtype: list
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        players_data = get_data(url, "playersData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

    def get_match_players(self, match_id, options=None, **kwargs):
        """Returns a dictionary containing information about the players who
        played in the given match.

        :param fixture_id: A match's ID.
        :type fixture_id: int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: Dictionary containing information about the players who played
            in the match.
        :rtype: dict
        """

        url = MATCH_URL.format(match_id)
        players_data = get_data(url, "rostersData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

    def get_match_shots(self, match_id, options=None, **kwargs):
        """Returns a dictionary containing information about shots taken by
        the players in the given match.

        :param fixture_id: A match's ID.
        :type fixture_id: int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: Dictionary containing information about the players who played
            in the match.
        :rtype: dict
        """

        url = MATCH_URL.format(match_id)
        players_data = get_data(url, "shotsData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data
