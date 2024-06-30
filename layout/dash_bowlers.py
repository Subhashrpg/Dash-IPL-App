from dash import html, dcc
from pages.bowlers import Bowlers
import pandas as pd
import plotly.express as px

bw = Bowlers()
bowler_list = bw.unique_bowlers()

# bowler dropdown===================================
def bowler_dropdown():
    return dcc.Dropdown(
        id="bowler-dropdown",
        options=[{"label": name, "value": name} for name in bowler_list],
        value="JJ Bumrah"
    )

# year dropdown=======================================
def year_dropdown():
    return dcc.Dropdown(
        id='bowler-year-dropdown'
    )

# Heading div====================================================================
def create_bowler_heading(selected_bowler="JJ Bumrah", selected_year="Overall"):
    if selected_year != "Overall":
        return html.Div(id="bowler-heading",className="heading",children=[
            f"{selected_bowler} in IPL {selected_year}"
        ])
    else:
        return html.Div(className="heading", id="bowler-heading",children=[
            f"{selected_bowler} in IPL"
        ])
    
# show batsman info==============================================================
def bowler_df_show(bowler, year):
    # dataframe show==
    match_played, innings = bw.match_vs_innings_played(bowler=bowler, season=year)
    total_balls, total_runs, total_wicket, ecomomy, average = bw.balls_runs_wicket_economy_avg(bowler=bowler, season=year)
    bbi, three_wickets, five_wickets = bw.three_vs_five_wickets_bestinnings(bowler=bowler, season=year)

    return {
        "Matches": match_played,
        "Innings": innings,
        "Balls": total_balls,
        "Runs": total_runs,
        "Wickets": total_wicket,
        "BBM": bbi,
        "Economy": ecomomy,
        "Average": average,
        "3W": three_wickets,
        "5W": five_wickets
    }

# gathering bowler's information in one place
def get_bowlers_data_against_teams(bowler, year):
    df1_temp = bw.match_played_against_teams(bowler=bowler, season=year)
    df2_temp = bw.run_wickets_economy_avg_against_teams(bowler=bowler, season=year)

    return_df = df1_temp.merge(df2_temp, on="batting_team", how="outer").rename(columns={'batting_team': 'Teams'})
    return_df.fillna(0, inplace=True)

    return return_df

def create_bowler_comparison_figure(bowler, year, metric, comparison_bowler=None):
    if year != "Overall":
        title = f"{metric} Comparison in IPL-{year}"
        x_title = "Bowler"

        # main batsman dataframe
        cp = bowler_df_show(bowler, year)
        cp_df1 = pd.DataFrame([cp])
        cp_df1["Bowler"] = bowler

        # getting data for comparison batsman
        comparison_bw_dfs = []
        if comparison_bowler:
            for bowler in comparison_bowler:
                comparison_data = bowler_df_show(bowler, year)
                comparison_df = pd.DataFrame([comparison_data])
                comparison_df["Bowler"] = bowler
                comparison_bw_dfs.append(comparison_df)        
            # combine all the data
            all_data_df = pd.concat([cp_df1] + comparison_bw_dfs, ignore_index=True)
        else:
            all_data_df = cp_df1

        cp_fig = px.bar(all_data_df, x="Bowler", y=metric, title=title)
    else:
        title = f"{metric} Comparison in IPL"
        x_title = "Season"
        temp_data_bw_df = bw.process_season_df_line_chart(bowler=bowler, season=year)

        if comparison_bowler:
            comparison_bw_dfs = []
            for batsman in comparison_bowler:
                comparison_df = bw.process_season_df_line_chart(bowler=bowler, season= year)
                comparison_bw_dfs.append(comparison_df)
            
            t_all_data_df = pd.concat([temp_data_bw_df] + comparison_bw_dfs, ignore_index=True)
        else:
            t_all_data_df = temp_data_bw_df

        cp_fig = px.line(t_all_data_df, x="season", y=metric, color="bowler", title=title)


    cp_fig.update_layout(
        title={
            'text': title,
            'y': .9,
            'x': .5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=f"{x_title}",
        yaxis_title=metric.capitalize(),
        plot_bgcolor="rgba(184, 243, 206, 0.7)",
        paper_bgcolor="rgba(284, 243, 206, 0.7)"
    )
    return cp_fig

# layout setup============================================================================
layout = html.Div([
    html.Div(className="dropdown-container", children=[
        html.Div(className="dropdown-pair", children=[
            html.Label("Select Bowler:", className="dropdown-label"),
            bowler_dropdown(),
        ]),
        html.Div(id="dropdown_year", className="dropdown-pair", children=[
            html.Label("Select Year:", className="dropdown-label"),
            year_dropdown()
        ])       
    ]),
    html.Div(className="line-text", children=[
        html.Div(className="line"),
        html.Div(id="bowler-heading",className="heading"),
        html.Div(className="line")
    ]),
    html.Div(id="bowler-data-container", className="data-table-container"),
    html.Div(id='bowler-against-teams-heading', className="subheading"),
    html.Div(id="bowler-against-teams-container", className="data-table-against-teams-container"),
    html.Div(html.H3("Graphical Represention"), className="heading"),
    html.Div(id="bowler-overall-graph"),
    html.Div(className="comparison-container", children=[
        html.Label("Compare with other bowler:", className="dropdown-label"),
        dcc.Dropdown(
            id="comparison-bowler-dropdown",
            options=[{"label": name, "value": name} for name in bowler_list],
            multi=True
        )
    ]),
    html.Div(id="comparison-bowler-graph-container")
])
# layout end===============================================================================