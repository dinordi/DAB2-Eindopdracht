import requests
import pandas as pd


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
        # Define the data types for each column
        dtype = {
            'raceId': int,
            'year': int,
            'round': int,
            'circuitId': int,
            'name': str,
            'date': str,  # You might want to parse dates later
            'time': str,  # You might want to parse times later
            # 'url': str,
            # 'fp1_date': str,
            # 'fp1_time': str,
            # 'fp2_date': str,
            # 'fp2_time': str,
            # 'fp3_date': str,
            # 'fp3_time': str,
            # 'quali_date': str,
            # 'quali_time': str,
            # 'sprint_date': str,
            # 'sprint_time': str
        }
        #Specify the columns to be read
        # usecols = ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time']
        # Replace 'your_file.csv' with the path to your actual CSV file
        # df = pd.read_csv('f1db_csv/races.csv', dtype=dtype, usecols=usecols)


        # Filter the DataFrame for races in 2022
        # df_2022 = df[df['year'] == 2022]
        # Print the first 5 rows of the DataFrame
        # print(df_2022)

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
