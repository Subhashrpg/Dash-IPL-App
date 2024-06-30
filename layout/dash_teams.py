from dash import html, dcc
from pages.teams import Teams
import pandas as pd

tm = Teams()
teams_list = tm.total_teams()

# teams dropdown
def teams_dropdown():
    return dcc.Dropdown(
        id="teams-dropdown",
        options=[{"label": name, "value": name} for name in teams_list],
        value="Chennai Super Kings"
    )

# year dropdown
def team_year_dropdown():
    return dcc.Dropdown(
        id='teams-year-dropdown'
    )

# teams heading
def create_teams_heading(selected_team="Chennai Super Kings", selected_year="Overall"):
    if selected_year != "Overall":
        return html.Div(id="teams-heading",className="heading",children=[
            f"{selected_team}'s Record in IPL - {selected_year}"
        ])
    else:
        return html.Div(className="heading", id="teams-heading",children=[
            f"{selected_team}'s Record in IPL"
        ])

# creating card layout
def create_card(title, value):
    return html.Div(className="card-child", children=[
        html.Div(className="card-title", children=title),
        html.Div(className="short-line"),
        html.Div(className='card-value', children=value)
    ])

# merge head to head df
def merge_head_to_head_df(team_1, season, team_2):
    m_played = tm.head_to_head_match_played(team_1=team_1, season=season, team_2=team_2)
    t1, t2, w1, w2 = tm.head_to_win(team_1=team_1, team_2=team_2, season=season)

    if m_played is None or t1 is None or t2 is None or w1 is None or w2 is None:
        return pd.DataFrame()
    
    empty_df = pd.DataFrame()
    empty_df[["Matches", t1, t2]] = [[m_played, w1, w2]]
    return empty_df

layout = html.Div([
    html.Div(className="dropdown-container", children=[
        html.Div(className="dropdown-pair", children=[
                html.Label("Select Teams:", className="dropdown-label"),
                teams_dropdown(),
        ]),
        html.Div(id="teams-dropdown_year", className="dropdown-pair", children=[
            html.Label("Select Year:", className="dropdown-label"),
            team_year_dropdown()
        ])
    ]),
    html.Div(className="line-text", children=[
        html.Div(className="line"),
        html.Div(id="teams-heading",className="heading"),
        html.Div(className="line")
    ]),
    html.Div(id="card-container", className="card-container", children=[]),
    html.Div(className="line-text", children=[
        html.Div(className="line"),
        html.Div(id="point-table-heading",className="heading",children=[
            f"Point Table"
        ]),
        html.Div(className="line")
    ]),
    html.Div(id="teams-data-container", className="data-table-container"),
    html.Div(className="comparison-container", children=[
        html.Label("Head to Head:", className="dropdown-label"),
        dcc.Dropdown(
            id="comparison-teams-dropdown",
            options=[{"label": name, "value": name} for name in teams_list]
        )
    ]),
    html.Div(id="head-to-head-container")
])