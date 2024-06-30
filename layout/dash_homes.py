from dash import html, dcc
from pages.homes import Home
from layout.dash_batsman import batsman_dropdown
from layout.dash_bowlers import bowler_dropdown

hm = Home()
# fucntion setup here
year_list = hm.unique_years()
year_list.append("Overall")

# defining initial content
initial_content = html.Div([
    html.Div(className="line-text", children=[
        html.Div(className="line"),
        html.Div(className="heading", children=["IPL Dashboard (Overall Analysis)"]),
        html.Div(className="line")
    ]),
    html.Div(className="comparison-container", children=[
        html.Label("Select season:", className="dropdown-label"),
        dcc.Dropdown(
            id = "season-dropdown-overall",
            options=[{"label": name, "value": name} for name in year_list],
            value = "Overall",
        )
    ]),
    html.Div([
        html.Div(className="line"),
        html.Div(id="home-card-container", className="card-container", children=[]),
        html.Div(className="line"),
    ]),
    html.Div([
        html.Div(className="heading", children=["IPL Point Table"]),
        html.Div(className="line")
    ]),
    html.Div(id="point-table", children=[]),
    html.Div(className="line-text", children=[
        html.Div(className="line"),
        html.Div(className="heading", children=["Batsman Vs Bowler Record"]),
        html.Div(className="line")
    ]),
    html.Div(className="dropdown-container", children=[
        html.Div(id="vs-batsman",className="dropdown-pair", children=[
                html.Label("Select Batsman:", className="dropdown-label"),
                batsman_dropdown(),
        ]),
        html.Div(id="vs-bowler", className="dropdown-pair", children=[
            html.Label("Select Bowler:", className="dropdown-label"),
            bowler_dropdown()
        ])
    ]),
    html.Div(className="line"),
    html.Div(id="batsman-vs-bowler")
])