import requests

class F1Standings():
    def __init__(self):
        pass

    def get_f1_standings(self, season, round):
        url = f"https://ergast.com/api/f1/{season}/{round}/driverStandings.json"
        response = requests.get(url)
        if response.status_code == 200:
            standings = response.json()
            return standings
        else:
            print("Error fetching data:", response.status_code)

    def get_standings(self, season, round):
        return self.get_f1_standings(season, round)

# if __name__ == "__main__":
#     season = "2023" 
#     round = "1"
#     standings = get_f1_standings(season, round)
#     if standings:
#         for standing in standings['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
#             position = standing['position']
#             points = standing['points']
#             wins = standing['wins']
#             driver = standing['Driver']['givenName'] + ' ' + standing['Driver']['familyName']
#             team = standing['Constructors'][0]['name']
#             print(f"Position: {position}, Driver: {driver}, Team: {team}, Points: {points}, Wins: {wins}")
#     else:
#         print("No standings data available for the specified season.")
