import plotly.graph_objects as go
from fillDB import F1Standings

def plot_standings(standings, rounds):
    fig = go.Figure()

    # Define the color for each driver
    colors = {
        'Max Verstappen': 'orange',
        # Add other drivers here
    }

    for round in range(1, rounds):
        if standings[round] is not None:
            drivers = []
            points = []
            driver_colors = []
            for standing in standings[round]['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
                driver = standing['Driver']['givenName'] + ' ' + standing['Driver']['familyName']
                point = standing['points']
                drivers.append(driver)
                points.append(point)

                driver_colors.append(colors.get(driver, 'blue'))

            points = points[::-1]
            drivers = drivers[::-1]
            driver_colors = driver_colors[::-1]
        else:
            print(f"No data for round {round}")
            return
        fig.add_trace(go.Bar(
            x=drivers,
            y=points,
            text=points,
            textposition='auto',
            visible=False if round > 1 else True,
            name=f'Round {round}',
            marker_color=driver_colors  # Use the assigned colors
        ))

    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"F1 Standings - Round {i+1}"}],
            label=f'Round {i+1}'
        )
        step["args"][0]["visible"][i] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Round: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
        title_text='F1 Standings - Round 1',
        xaxis=dict(autorange="reversed"),
        yaxis=dict(type="linear")
    )

    fig.show()

if __name__ == "__main__":
    standings = F1Standings()
    rounds = 22
    all_standings = {round: standings.get_standings("2021", str(round)) for round in range(1, rounds)}
    # standings.get_f1_standings("2021", "1")
    plot_standings(all_standings, rounds)