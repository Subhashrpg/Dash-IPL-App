from dash import html, dcc
from pages import batsmans as bt
import pandas as pd
import plotly.express as px


batsman_list = bt.batsman_names()

# batsman dropdown==============================================================
def batsman_dropdown():
    return dcc.Dropdown(
        id="batsman-dropdown",
        options=[{"label": name, "value": name} for name in batsman_list],
        value="V Kohli"
    )

# year dropdown=================================================================
def year_dropdown():
    return dcc.Dropdown(
        id='year-dropdown'
    )

# Heading div====================================================================
def create_batsman_heading(selected_batsman="V Kohli", selected_year="Overall"):
    if selected_year != "Overall":
        return html.Div(id="batsman-heading",className="heading",children=[
            f"{selected_batsman} in IPL {selected_year}"
        ])
    else:
        return html.Div(className="heading", id="batsman-heading",children=[
            f"{selected_batsman} in IPL"
        ])
    
# show batsman info==============================================================
def batsman_df_show(batsman, year):
    # dataframe show==
    match_played, innings = bt.match_inning_played(batsman=batsman, season=year)
    runs, highest_score,avg,strike_rate = bt.batsman_runs_score(batsman=batsman, season=year)
    fifty,hundred = bt.batsman_fifty_hundred(batsman=batsman, season=year)
    fours, sixes = bt.sixes_vs_fours(batsman=batsman, season=year)

    return {
        "Matches": match_played,
        "Innings": innings,
        "Runs": runs,
        "Highest_Score": highest_score,
        "Average": avg,
        "Strike_rate": strike_rate,
        "100s": hundred,
        "50s": fifty,
        "4s": fours,
        "6s": sixes
    }


# comparison figure=================
def create_comparison_figure(batsman, year, metric, comparison_batsman=None):
    if year != "Overall":
        title = f"{metric} Comparison in IPL-{year}"
        x_title = "Batsman"

        # main batsman dataframe
        cp = batsman_df_show(batsman, year)
        cp_df = pd.DataFrame([cp])
        cp_df["Batsman"] = batsman

        # getting data for comparison batsman
        comparison_dfs = []
        if comparison_batsman:
            for batsman in comparison_batsman:
                comparison_data = batsman_df_show(batsman, year)
                comparison_df = pd.DataFrame([comparison_data])
                comparison_df["Batsman"] = batsman
                comparison_dfs.append(comparison_df)        
            # combine all the data
            all_data_df = pd.concat([cp_df] + comparison_dfs, ignore_index=True)
        else:
            all_data_df = cp_df

        cp_fig = px.bar(all_data_df, x="Batsman", y=metric, title=title)
    else:
        title = f"{metric} Comparison in IPL"
        x_title = "Season"
        temp_data_df = bt.process_season_df_line_chart(batsman=batsman, season=year)

        if comparison_batsman:
            comparison_dfs = []
            for batsman in comparison_batsman:
                comparison_df = bt.process_season_df_line_chart(batsman=batsman, season= year)
                comparison_dfs.append(comparison_df)
            
            t_all_data_df = pd.concat([temp_data_df] + comparison_dfs, ignore_index=True)
        else:
            t_all_data_df = temp_data_df

        cp_fig = px.line(t_all_data_df, x="season", y=metric, color="batter", title=title)


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

#  creating layout========================================================================================
layout = html.Div([
    html.Div(className="dropdown-container", children=[
        html.Div(className="dropdown-pair", children=[
            html.Label("Select Batsman:", className="dropdown-label"),
            batsman_dropdown(),
        ]),
        html.Div(id="dropdown_year", className="dropdown-pair", children=[
            html.Label("Select Year:", className="dropdown-label"),
            year_dropdown()
        ])       
    ]),
    html.Div(className="line-text", children=[
        html.Div(className="line"),
        html.Div(id="heading",className="heading"),
        html.Div(className="line")
    ]),
    html.Div(id="batsman-data-container", className="data-table-container"),
    html.Div(id='batsman-against-teams-heading', className="subheading"),
    html.Div(id="batsman-against-teams-container", className="data-table-against-teams-container"),
    html.Div(html.H3("Graphical Represention"), className="heading"),
    html.Div(id="batsman-overall-graph"),
    html.Div(className="comparison-container", children=[
        html.Label("Compare with other batsman:", className="dropdown-label"),
        dcc.Dropdown(
            id="comparison-batsman-dropdown",
            options=[{"label": name, "value": name} for name in batsman_list],
            multi=True
        )
    ]),
    html.Div(id="comparison-graph-container")
])
#==================================================================================================