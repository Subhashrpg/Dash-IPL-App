import dash
from dash import html
from dash.dependencies import Input, Output
from layout import dash_bowlers, dash_teams, dash_homes, dash_batsman
from dash import dcc
from pages import batsmans as bt
from pages.bowlers import Bowlers
from pages.teams import Teams
from pages.homes import Home
import plotly.express as px
import time

# setting up app ===============
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server = app.server

bowler = Bowlers()
tm = Teams()
hm = Home()

#===========================================================
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Ul(className="card-list", children=[
        html.Li(className="card", children=[
            dcc.Link(html.Img(src=app.get_asset_url("ipl.png"), className="card-img"), href="/home", className="card-link")
        ]),
        html.Li(className="card", children=[
            dcc.Link(html.Img(src=app.get_asset_url("teams.jpg"), className="card-img"), href="/teams", className="card-link")
        ]),
        html.Li(className="card", children=[
            dcc.Link(html.Img(src=app.get_asset_url("batters.jpg"), className="card-img"), href="/batsmans",
            className="card-link")
        ]),
        html.Li(className="card", children=[
            dcc.Link(html.Img(src=app.get_asset_url("bowlers.jpg"), className="card-img"), href="/bowlers",
            className="card-link")
        ]),
    ]),
    html.Div(id="page-content", children=dash_homes.initial_content)
])
# ==========================================================

# binding with navigation================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/teams":
        return dash_teams.layout
    elif pathname == "/batsmans":
        return dash_batsman.layout
    elif pathname == "/bowlers":
        return dash_bowlers.layout
    elif pathname == "/home" or pathname == "/":
        return dash_homes.initial_content
    else:
        return "404 Page Not Found"
# =======================================

# batsman callbacks==========================================================
@app.callback(
    [Output('year-dropdown', 'options'),
    Output('year-dropdown', 'value') ],
    [Input('batsman-dropdown', 'value')]
)
def update_year_dropdown(selected_batsman):
    seasons = bt.batsman_year(batsman=selected_batsman)
    seasons.append("Overall")
    default_value = seasons[0] if seasons else None
    options = [{'label': season, 'value': season} for season in seasons]
    return options, default_value

@app.callback(
    [Output("heading", "children"),
    Output("batsman-data-container", "children"),
    Output("batsman-against-teams-heading", "children"),
    Output("batsman-against-teams-container", "children")],
    [Input("batsman-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_batsman_heading(selected_batsman, selected_year):
    # creating batsman heading==
    batsman_heading = dash_batsman.create_batsman_heading(selected_batsman=selected_batsman,selected_year=selected_year)

    # creating heading==========
    stats = dash_batsman.batsman_df_show(batsman=selected_batsman, year=selected_year)

    table = html.Table([
        html.Thead(className="table-header", children=[
            html.Tr([html.Th(metric) for metric in stats.keys()])]
        ),
        html.Tbody(
            html.Tr([html.Td(value) for value in stats.values()])
        )
    ], className="stats-table")

    # setting teams heading======
    teams_heading = html.Div(html.H3(className="teams-subheading", children=[f"{selected_batsman}'s Record Against Teams"]))

    temp_df = bt.merge_teams_dataframe(batsman=selected_batsman, season=selected_year)
    batsman_against_teams = temp_df
    teams_table =html.Table([
        html.Thead(className="table-header",children=[
            html.Tr([html.Th(col) for col in batsman_against_teams.columns])]
        ),
        html.Tbody([
            html.Tr([
                html.Td(batsman_against_teams.iloc[i][col]) for col in batsman_against_teams.columns
            ]) for i in range(len(batsman_against_teams))
        ])
    ], className="stats-table")

    return batsman_heading, table, teams_heading, teams_table

# changing the graph of the visualization======
@app.callback(
    Output('batsman-overall-graph', 'children'),
    Input('batsman-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_batsman_graphs(selected_batsman, selected_year):
    bt_metrics = ["Runs", "Strike_rate", "Average", "Highest_score"]
    bt_graphs = []

    bt_stats = bt.merge_teams_dataframe(batsman=selected_batsman, season=selected_year)

    # creating graphs==
    def create_figure(batsman, year, metric):
        if year != "Overall":
            title = f"{batsman} - {metric} in IPL {year}"
        else:
            title = f"{batsman} - {metric} in IPL"
        time.sleep(.2)
        fig = px.bar(bt_stats, x='Teams', y=metric, title=title)

        # customize the layout
        fig.update_layout(
            title={
                'text': title,
                'y': .9,
                'x': .5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title = 'Teams',
            yaxis_title = metric.capitalize(),
            plot_bgcolor = "rgba(184, 243, 206, 0.7)",
            paper_bgcolor= "rgba(284, 243, 206, 0.7)"
        )
        return fig

    # plotting graph ======
    for metric in bt_metrics:
        main_fig = create_figure(batsman=selected_batsman, year=selected_year, metric=metric)
        bt_graphs.append(html.Div(className="graph-content-container", children=[
            dcc.Graph(figure=main_fig)
        ]))

    return bt_graphs

# comparison batsman container
@app.callback(
    Output('comparison-graph-container', 'children'),
    Input('batsman-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('comparison-batsman-dropdown', 'value')
)
def update_comparison_batsman(selected_batsman, selected_year, comparison_batsman):
    bt_men, bt_year = selected_batsman, selected_year
    cp_metric = ["Runs", "Strike_rate", "Average", "Highest_Score"]
    cp_graphs = []

    # creating figure

    for metric in cp_metric:
        cp_fig = dash_batsman.create_comparison_figure(bt_men, bt_year, metric, comparison_batsman)
        cp_graphs.append(html.Div(className="compare-batsman-graph", children=[
            dcc.Graph(figure=cp_fig)
        ]))
        
    # arrange graphs two per line
    graph_row = []
    for i in range(0, len(cp_graphs), 2):
        graph_row.append(
            html.Div(className='graph-row', children=cp_graphs[i:i+2])
        )

    return graph_row
# ===========================================================================

# bowler callbacks===========================================================
@app.callback(
    [Output('bowler-year-dropdown', 'options'),
    Output('bowler-year-dropdown', 'value')],
    [Input('bowler-dropdown', 'value')]
)
def update_year_dropdown(selected_bowler):
    seasons = bowler.bowler_year(selected_bowler)
    seasons.append("Overall")
    default_value = seasons[0] if seasons else None
    options = [{'label': season, 'value': season} for season in seasons]
    return options, default_value

@app.callback(
    [Output("bowler-heading", "children"),
     Output("bowler-data-container", "children"),
     Output("bowler-against-teams-heading", "children"),
     Output('bowler-against-teams-container', 'children')],
    [Input("bowler-dropdown", "value"),
     Input("bowler-year-dropdown", "value")]
)
def update_bowlers_heading(selected_bowler, selected_year):
    # creating batsman heading==
    bowler_heading = dash_bowlers.create_bowler_heading(selected_bowler=selected_bowler,selected_year=selected_year)

    # creating heading==========
    stats = dash_bowlers.bowler_df_show(bowler=selected_bowler, year=selected_year)

    table = html.Table([
        html.Thead(className="table-header", children=[
            html.Tr([html.Th(metric) for metric in stats.keys()])]
        ),
        html.Tbody(
            html.Tr([html.Td(value) for value in stats.values()])
        )
    ], className="stats-table")

    # setting teams heading======
    teams_heading = html.Div(html.H3(className="teams-subheading", children=[f"{selected_bowler}'s Record Against Teams"]))

    temp_bowlers_df = dash_bowlers.get_bowlers_data_against_teams(bowler=selected_bowler, year=selected_year)
    bowler_against_teams = temp_bowlers_df
    bowler_teams_table =html.Table([
        html.Thead(className="table-header",children=[
            html.Tr([html.Th(col) for col in bowler_against_teams.columns])]
        ),
        html.Tbody([
            html.Tr([
                html.Td(bowler_against_teams.iloc[i][col]) for col in bowler_against_teams.columns
            ]) for i in range(len(bowler_against_teams))
        ])
    ], className="stats-table")

    return bowler_heading, table, teams_heading, bowler_teams_table

# creating graphs 
@app.callback(
    Output('bowler-overall-graph', 'children'),
    Input('bowler-dropdown', 'value'),
    Input('bowler-year-dropdown', 'value')
)
def update_bowler_graphs(selected_bowler, selected_year):
    bw_metrics = ["Wickets", "Economy", "Average"]
    bw_graphs = []

    bw_stats = dash_bowlers.get_bowlers_data_against_teams(bowler=selected_bowler, year=selected_year)

    # creating graphs==
    def create_figure(bowler, year, metric):
        if year != "Overall":
            title = f"{bowler} - {metric} in IPL {year}"
        else:
            title = f"{bowler} - {metric} in IPL"
        time.sleep(.2)
        fig = px.bar(bw_stats, x='Teams', y=metric, title=title)

        # customize the layout
        fig.update_layout(
            title={
                'text': title,
                'y': .9,
                'x': .5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title = 'Teams',
            yaxis_title = metric.capitalize(),
            plot_bgcolor = "rgba(184, 243, 206, 0.7)",
            paper_bgcolor= "rgba(284, 243, 206, 0.7)"
        )
        return fig

    # plotting graph ======
    for metric in bw_metrics:
        main_fig = create_figure(bowler=selected_bowler, year=selected_year, metric=metric)
        bw_graphs.append(html.Div(className="graph-content-container", children=[
            dcc.Graph(figure=main_fig)
        ]))

    return bw_graphs

@app.callback(
    Output('comparison-bowler-graph-container', 'children'),
    Input('bowler-dropdown', 'value'),
    Input('bowler-year-dropdown', 'value'),
    Input('comparison-bowler-dropdown', 'value')
)
def update_comparison_bowler(selected_bowler, selected_year, comparison_bowler):
    bt_men, bt_year = selected_bowler, selected_year
    cp_bowler_metric = ["Wickets", "Economy", "Average"]
    cp_bowler_graphs = []

    # creating figure

    for metric in cp_bowler_metric:
        cp_fig = dash_bowlers.create_bowler_comparison_figure(bt_men, bt_year, metric, comparison_bowler)
        cp_bowler_graphs.append(html.Div(className="compare-bowler-graph", children=[
            dcc.Graph(figure=cp_fig)
        ]))
        
    # arrange graphs two per line
    graph_row = []
    for i in range(0, len(cp_bowler_graphs), 2):
        graph_row.append(
            html.Div(className='graph-row', children=cp_bowler_graphs[i:i+2])
        )

    return graph_row
# ===========================================================================

# teams callbacks============
@app.callback(
    [Output('teams-year-dropdown', 'options'),
    Output('teams-year-dropdown', 'value')],
    [Input('teams-dropdown', 'value')]
)
def update_teams_year(selected_team):
    seasons = tm.get_played_season(team=selected_team)
    seasons.append("Overall")
    default_value = seasons[0] if seasons else None
    options = [{'label': season, 'value': season} for season in seasons]
    return options, default_value

# teams heading change
@app.callback(
    Output('teams-heading', 'children'),
    [Input('teams-dropdown', 'value'),
    Input('teams-year-dropdown', 'value')]
)
def update_teams_heading(selected_teams, selected_year):
    return dash_teams.create_teams_heading(selected_team=selected_teams, selected_year=selected_year)

# updating card children
@app.callback(
    Output('card-container', 'children'),
    [Input('teams-dropdown', 'value'),
    Input('teams-year-dropdown', 'value')]
)
def update_card_children(selected_team, selected_season):
    team1, run_1, wkt_1 =  tm.best_vs_worst_powerplay(teams=selected_team, season=selected_season, ascending=False)
    team2, run_2, wkt_2 =  tm.best_vs_worst_powerplay(teams=selected_team, season=selected_season, ascending=True)
    team_3, run_3, wkt_3 = tm.last_five_overs(teams=selected_team, season=selected_season)
    team_4, run_4, wkt_4 = tm.best_vs_worst_score_teams(teams=selected_team, season=selected_season, ascending=False)
    team_5, run_5, wkt_5 = tm.best_vs_worst_score_teams(teams=selected_team, season=selected_season, ascending=True)
    team_6, bt_1, rn_1 = tm.best_individual_score(teams=selected_team, season=selected_season)
    bt_name, bt_runs = tm.highest_scorer(season=selected_season, teams=selected_team)
    team_7, bw_1, rn_2, wkt_6 = tm.best_bowler_ind_df(teams=selected_team, season=selected_season)
    wk_name, wk_wkt = tm.highest_wicket_taker(teams=selected_team, season=selected_season)
    pw_sixes = tm.powerplay_sixes(teams=selected_team, season=selected_season, overs=[0,1,2,3,4,5])
    l5_sixes = tm.powerplay_sixes(teams=selected_team, season=selected_season, overs=[15,16,17,18,19])
    ttl_sixes = tm.powerplay_sixes(teams=selected_team, season=selected_season)
    fnl_played = tm.total_final_played(teams=selected_team, season=selected_season)
    fnl_won = tm.total_final_won(teams=selected_team, season=selected_season)

    # creating cards 
    cards = [
        dash_teams.create_card(title="Best Powerplay Score", value=f"{team1} - {str(run_1)}/{str(wkt_1)}"),
        dash_teams.create_card(title="Lowest Powerplay Score", value=f"{team2} - {str(run_2)}/{str(wkt_2)}"),
        dash_teams.create_card(title="Best Last 5 Overs", value=f"{team_3} - {str(run_3)}/{str(wkt_3)}"),
        dash_teams.create_card(title="Best Score", value=f"{team_4} - {str(run_4)}/{str(wkt_4)}"),
        dash_teams.create_card(title="Lowest Score", value=f"{team_5} - {str(run_5)}/{str(wkt_5)}"),
        dash_teams.create_card(title="Best Individual Score", value=f"{str(bt_1)} ==> {str(rn_1)} ({team_6})"),
        dash_teams.create_card(title="Highest Scorer", value=f"{bt_name} - {bt_runs}"),
        dash_teams.create_card(title="Best Bowling", value=f"{str(bw_1)} ==> {str(rn_2)}/{str(wkt_6)} ({team_7})"),
        dash_teams.create_card(title="Highest Wicket Taker", value=f"{wk_name} - {wk_wkt}"),
        dash_teams.create_card(title="Sixes in Powerplay", value=f"{pw_sixes}"),
        dash_teams.create_card(title="Sixes in Last 5 Overs", value=f"{l5_sixes}"),
        dash_teams.create_card(title="Total Sixes", value=f"{ttl_sixes}")

    ]

    if fnl_played is not None:
        cards.append(dash_teams.create_card(title="Final Played", value=f'{str(fnl_played)}'))
    if fnl_won is not None:
        cards.append(dash_teams.create_card(title="Final Won", value=f'{str(fnl_won)}'))
    
    return cards

# showing point table
@app.callback(
    Output('teams-data-container', 'children'),
    [Input('teams-dropdown', 'value'),
    Input('teams-year-dropdown', 'value')]
)
def update_point_table(selected_team, selected_season):
    data = tm.point_table(team=selected_team, season=selected_season)

    point_table = html.Table([
        html.Thead(className="table-header", children=[
            html.Tr([html.Th(col) for col in data.columns])]
        ),
        html.Tbody(
            html.Tr([html.Td(data.iloc[0][value]) for value in data.columns])
        )
    ], className="stats-table")
    
    return point_table

# head to head contest
@app.callback(
    Output('head-to-head-container', 'children'),
    [Input('teams-dropdown', 'value'),
    Input('teams-year-dropdown', 'value'),
    Input('comparison-teams-dropdown', 'value')]
)
def update_head_to_head_stats(selected_team1, selected_season, selected_team2):
    if selected_team2:
        h_df = dash_teams.merge_head_to_head_df(team_1=selected_team1, season=selected_season, team_2=selected_team2)
        
        if h_df.empty:
            return html.Div(className="heading", children=["No head-to-head stats available for the selected teams and season."])
        
        head_table = html.Table([
            html.Thead(className="table-header", children=[
                html.Tr([html.Th(col) for col in h_df.columns])]
            ),
            html.Tbody(
                html.Tr([html.Td(h_df.iloc[0][value]) for value in h_df.columns])
            )
        ], className="stats-table")
    
        return head_table
    return html.Div(className="heading", children=["Please select teams to view head-to-head stats."])

# overall callbacks
@app.callback(
    Output('home-card-container', 'children'),
    Input('season-dropdown-overall', 'value')
)
def update_overall_analysis(selected_season):
    match_played = hm.match_played(selected_season)
    bat_1, rn_1 = hm.most_runs_batter(selected_season)
    bow_1, wkt_1 = hm.most_wicket_bowler(selected_season)
    tm_1, six_1 = hm.sixes_count(selected_season)
    bat_3, six_2 = hm.sixes_count(selected_season, metric="batter")

    if selected_season != "Overall":
        final_team_1, final_team_2, final_won_team = hm.final_played_won(selected_season)
        team_1, runs_1, wicket_1 = hm.team_best_score(selected_season)
        team_2, runs_2, wicket_2 = hm.team_best_score(selected_season, ascending=[True,False])
        bat_2, rn_2 = hm.best_individual_score(selected_season)
        bow_2, rn_3, wkt_2 = hm.best_bowling_figure(selected_season)
    else:
        most_final, final_num = hm.final_played_won(selected_season)
        team_1, runs_1, wicket_1, season_1 = hm.team_best_score(selected_season)
        team_2, runs_2, wicket_2, season_2 = hm.team_best_score(selected_season, ascending=[True,False])
        bat_2, rn_2, season_3 = hm.best_individual_score(selected_season)
        bow_2, rn_3, wkt_2, season_4 = hm.best_bowling_figure(selected_season)
        m_final_team, m_final_number = hm.most_final_won()

    # creating cards
    cards = [
        dash_teams.create_card(title="Total Matches", value=f"{match_played}"),
        dash_teams.create_card(title="Most Runs", value=f"{bat_1} - {rn_1}"),
        dash_teams.create_card(title="Most Wickets", value=f"{bow_1} - {wkt_1}"),
        dash_teams.create_card(title="Most Sixes Teams", value=f"{tm_1} - {six_1}"),
        dash_teams.create_card(title="Most Sixes Batsman", value=f"{bat_3} - {six_2}")
    ]

    # appending best score teams
    if selected_season != "Overall":
        cards.insert(1, dash_teams.create_card(title="Highest Score", value=f"{team_1} - {runs_1}/{wicket_1}"))
        cards.insert(2, dash_teams.create_card(title="Lowest Score", value=f"{team_2} - {runs_2}/{wicket_2}"))
        cards.insert(5, dash_teams.create_card(title="Best Score", value=f"{bat_2} - {rn_2}"))
        cards.insert(6, dash_teams.create_card(title="Best Bowling", value=f"{bow_2} - {rn_3}/{wkt_2}"))
        cards.append(dash_teams.create_card(title="Final Played", value=f"{final_team_1} VS {final_team_2}"))
        cards.append(dash_teams.create_card(title="Final Winning Team", value=f"{final_won_team}"))
    else:
        cards.insert(1, dash_teams.create_card(title="Highest Score", value=f"{team_1} - {runs_1}/{wicket_1} ==>({season_1})"))
        cards.insert(2, dash_teams.create_card(title="Lowest Score", value=f"{team_2} - {runs_2}/{wicket_2} ==>({season_2})"))
        cards.insert(5, dash_teams.create_card(title="Best Score", value=f"{bat_2} - {rn_2} ==> {season_3}"))
        cards.insert(6, dash_teams.create_card(title="Best Bowling", value=f"{bow_2} - {rn_3}/{wkt_2} ({season_4})"))
        cards.append(dash_teams.create_card(title="Most Final Played", value=f"{most_final} - {int(final_num)}"))
        cards.append(dash_teams.create_card(title="Most Final Win", value=f"{m_final_team} - {int(m_final_number)}"))

    return cards

@app.callback(
    Output('point-table', 'children'),
    Input('season-dropdown-overall', 'value')
)
def update_team_point_table(selected_season):
    point_table_df = hm.point_table(selected_season)
    
    point_table_team = html.Table([
        html.Thead(className="table-header", children=[
            html.Tr([html.Th(col) for col in point_table_df.columns])]
        ),
        html.Tbody([
            html.Tr([
                html.Td(point_table_df.iloc[i][col]) for col in point_table_df.columns
            ]) for i in range(len(point_table_df))
        ])
    ], className="stats-table")
    
    return point_table_team

@app.callback(
    Output('batsman-vs-bowler', 'children'),
    [Input('season-dropdown-overall', 'value'),
     Input('batsman-dropdown', 'value'),
     Input('bowler-dropdown', 'value')]
)
def update_batsman_bowler(selected_season, selected_batsman, selected_bowler):
    bat_vs_bow = hm.batsman_vs_bowler(selected_season, selected_batsman, selected_bowler)

    if bat_vs_bow.empty:
        return html.Div(className="heading", children=["No head to head data available"])
    
    bat_bow_table = html.Table([
        html.Thead(className="table-header", children=[
            html.Tr([html.Th(col) for col in bat_vs_bow.columns])]
        ),
        html.Tbody([
            html.Tr([
                html.Td(bat_vs_bow.iloc[i][col]) for col in bat_vs_bow.columns
            ]) for i in range(len(bat_vs_bow))
        ])
    ], className="stats-table")

    return bat_bow_table

# running the app========================================================
if __name__ == "__main__":
    app.run_server(debug=True)