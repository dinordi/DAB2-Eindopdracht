import plotly.graph_objects as go
from fillDB import F1Standings


def plot_standings(standings):
    drivers = []
    points = []
    for standing in standings['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
        driver = standing['Driver']['givenName'] + ' ' + standing['Driver']['familyName']
        point = standing['points']
        drivers.append(driver)
        points.append(point)

    points = points[::-1]
    drivers = drivers[::-1]

    fig = go.Figure(data=[go.Bar(
        x=drivers,
        y=points,
        text=points,
        textposition='auto',
    )])

    fig.update_layout(
        title_text='F1 Standings',
        xaxis=dict(autorange="reversed")  # This line reverses the y-axis
    )

    fig.show()

if __name__ == "__main__":
    standings = F1Standings()
    plot_standings(standings.get_standings("2023", "1"))