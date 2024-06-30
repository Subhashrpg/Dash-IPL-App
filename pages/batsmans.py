from data_loader import delivery, matches
import pandas as pd

# getting batsman's name=============
def batsman_names(df=delivery):
    return df.batter.str.strip().unique().tolist()

# getting batsman's played year======
def batsman_year(df1=delivery, df2=matches, batsman="V Kohli"):
    ids = df1[df1.batter == batsman].match_id.unique()
    return df2[df2["id"].isin(ids)]["season"].unique().tolist()

# seson dataframe====================
def season_dataframe(df1=delivery, df2=matches, season="Overall"):
    if season != "Overall":
        season_df = df2[df2["season"] == season]
        season_values = df2[df2["season"] == season].id.values
        return df1[df1["match_id"].isin(season_values)], season_df
    else:
        temp_df1 = pd.merge(df1, df2, left_on="match_id", right_on="id", how="outer")
        return temp_df1, df2

# retun batsman dataframe============
def batsman_dataframe(df1="delivery",batsman="V Kohli"):
    return df1[df1.batter == batsman]

# processing the dataframe
def process_batsman_data(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    b_df1, b_df2 = season_dataframe(df1=df1, season=season)
    temp_df1 = batsman_dataframe(df1=b_df1, batsman=batsman)
    return temp_df1

# matches and innings played=========
def match_inning_played(df1=delivery, df2=matches,batsman="V Kohli", season="Overall"):
    temp_df1, temp_df2 = season_dataframe(df1=df1, df2=df2, season=season)
    matches_played = temp_df2[(temp_df2.Team1Players.str.contains(batsman)) | (temp_df2.Team2Players.str.contains(batsman))].shape[0]
    temp_df = batsman_dataframe(df1=temp_df1,batsman=batsman)
    innings = len(temp_df.groupby("match_id")["batter"].count().index.tolist())
    return matches_played, innings

# Batsman's runs and highest score===
def batsman_runs_score(df1=delivery, batsman="V kohli", season="Overall"):
    temp_df1 = process_batsman_data(df1=df1, batsman=batsman, season=season)
    total_runs = temp_df1["batsman_runs"].sum()

    balls_played = temp_df1.groupby("batter")["batsman_runs"].count().values[0]
    out = temp_df1[~temp_df1["dismissal_kind"].isin(["retired hurt","retired out"])]["is_wicket"].sum()

    if (balls_played != 0) or (type(balls_played)!= int):
        strike_rate = round((total_runs/balls_played)*100,2)
    else:
        strike_rate = "-"

    if out != 0:
        avg = round(total_runs/out, 2)
    else:
        avg = total_runs

    highest_score = temp_df1.groupby("match_id")["batsman_runs"].sum().max()
    return total_runs, highest_score, avg, strike_rate


# processing season dataframe for line chart
def process_season_df_line_chart(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    temp_df1 = pd.merge(df1, df2, left_on="match_id", right_on="id", how="outer")
    temp_df1 = temp_df1[temp_df1["batter"] == batsman]
    s_df = temp_df1.groupby(["season", "batter"])
    runs = s_df["batsman_runs"].sum().reset_index().rename(columns={"batsman_runs": "Runs"})
    balls = s_df["batsman_runs"].count().reset_index().rename(columns={"batsman_runs": "balls"})
    hs = temp_df1.groupby(["season", "match_id", "batter"])["batsman_runs"].sum().reset_index().groupby(["season", "batter"])["batsman_runs"].max().reset_index().rename(columns={"batsman_runs": "Highest_Score"})
    out_df = temp_df1[~temp_df1["dismissal_kind"].isin(['retired_out', 'retired_hurt'])].groupby(["season", "batter"])["is_wicket"].sum().reset_index().rename(columns={"is_wicket": "out"})

    # merging all dfs
    result_df = pd.merge(runs, balls, on=["season", "batter"], how="outer").merge(hs, on=["season", "batter"], how="outer").merge(out_df, on=["season", "batter"], how="outer")

    # getting strike_rate and avg
    result_df["Strike_rate"] = result_df.apply(lambda row: round((row["Runs"]/row["balls"])*100,2) if row["balls"] > 0 else row["Runs"], axis=1) 
    result_df["Average"] = result_df.apply(lambda row: round((row["Runs"]/row["out"]),2) if row["out"] > 0 else row["Runs"], axis=1)

    return result_df

# Batsman's fifty and century=====
def batsman_fifty_hundred(df1=delivery, batsman="V Kohli", season="Overall"):
    b_df1, _ = season_dataframe(df1=df1,season=season)
    temp_df1 = batsman_dataframe(df1=b_df1, batsman=batsman)

    new_df = temp_df1.groupby("match_id")["batsman_runs"].sum().reset_index()
    fifties = new_df.query("batsman_runs >= 50 and batsman_runs < 100")["batsman_runs"].count()
    hundreds = new_df.query("batsman_runs >= 100")["batsman_runs"].count()

    return fifties, hundreds

# Batsman fours and sixes==========
def sixes_vs_fours(df1=delivery, batsman="V Kohli", season="Overall"):
    b_df1, _ = season_dataframe(df1=df1,season=season)
    temp_df1 = batsman_dataframe(df1=b_df1, batsman=batsman)

    four_six_df = temp_df1[(temp_df1["batsman_runs"] == 4) | (temp_df1["batsman_runs"] == 6)]

    try:
        fours = four_six_df.groupby(["batter","batsman_runs"])["batsman_runs"].count().unstack()[4].values[0]
    except KeyError:
        fours = 0
    try:
        sixes = four_six_df.groupby(["batter","batsman_runs"])["batsman_runs"].count().unstack()[6].values[0]
    except KeyError:
        sixes = 0

    return fours, sixes

# against teams records==================================================
# match played==================
def batsman_record_vs_teams_match_played(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    # temp_df1 = process_batsman_data(df1=delivery, df2=matches, batsman="V Kohli", season="Overall")
    return df1.groupby(["match_id","bowling_team"])["batter"].count().reset_index().bowling_team.value_counts().reset_index().rename(columns={"count": "Match"})

# runs made=====================
def batsman_record_vs_teams_runs_balls_played(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    r_df = df1.groupby(["bowling_team"])
    o_df = df1[~df1["dismissal_kind"].isin(['retired_out', 'retired_hurt'])].groupby(["bowling_team"])
    runs_df = r_df["batsman_runs"].sum().reset_index().rename({"batsman_runs": "Runs"}, axis=1)
    balls_df = o_df["batsman_runs"].count().reset_index().rename({"batsman_runs": "balls"}, axis=1)
    out_df = r_df["is_wicket"].sum().reset_index().rename({"is_wicket": "out"}, axis=1)
    highest_score_df = df1.groupby(["bowling_team", "match_id"])["batsman_runs"].sum().reset_index().groupby("bowling_team")["batsman_runs"].max().reset_index().rename(columns={"batsman_runs": "Highest_score"})

    # merging both dataframe
    result_df = pd.merge(runs_df, balls_df, on="bowling_team", how="outer").merge(out_df, on="bowling_team", how="outer").merge(highest_score_df, on="bowling_team", how="outer")

    result_df["Strike_rate"] = result_df.apply(lambda row: round((row["Runs"]/row["balls"])*100,2) if row["balls"] > 0 else row["Runs"], axis=1) 
    result_df["Average"] = result_df.apply(lambda row: round((row["Runs"]/row["out"]),2) if row["out"] > 0 else row["Runs"], axis=1)

    return result_df

# fifty and hundred getting========
def fifty_and_hundred(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    hundred_fifty_df = df1.groupby(["bowling_team", "match_id"])["batsman_runs"].sum().reset_index()

    h_df = hundred_fifty_df.query("batsman_runs >=100").groupby("bowling_team")["batsman_runs"].count().reset_index().rename(columns={"batsman_runs": "100s"})
    
    f_df = hundred_fifty_df.query("batsman_runs >=50 and batsman_runs <= 100").groupby("bowling_team")["batsman_runs"].count().reset_index().rename(columns={"batsman_runs": "50s"})

    return pd.merge(h_df, f_df, on="bowling_team", how="outer")

# sixes and fours getting===========
def sixes_fours_against_teams(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    # fours ======
    fours_df = df1[df1.batsman_runs == 4]
    fours = fours_df.groupby("bowling_team")["batsman_runs"].count().reset_index().rename(columns={"batsman_runs": "4s"})

    # sixes ====
    sixes_df = df1[df1.batsman_runs == 6]
    sixes = sixes_df.groupby("bowling_team")["batsman_runs"].count().reset_index().rename(columns={"batsman_runs": "6s"})

    return pd.merge(fours, sixes, on="bowling_team", how="outer")

# mergin the dataframe for overall team==============
def merge_teams_dataframe(df1=delivery, df2=matches, batsman="V Kohli", season="Overall"):
    temp_df1 = process_batsman_data(df1=delivery, df2=matches, batsman=batsman, season=season)

    result_df1 = batsman_record_vs_teams_match_played(df1=temp_df1,batsman=batsman, season=season)
    result_df2 = batsman_record_vs_teams_runs_balls_played(df1=temp_df1,batsman=batsman, season=season)
    result_df3 = fifty_and_hundred(df1=temp_df1, batsman=batsman, season=season)
    result_df4 = sixes_fours_against_teams(df1=temp_df1, batsman=batsman, season=season)

    result = pd.merge(result_df1, result_df2, on="bowling_team", how="outer").merge(result_df3, on="bowling_team", how="outer").merge(result_df4, on="bowling_team",how="outer")

    result.drop(columns=["balls", "out"], inplace=True)
    result.fillna(0, inplace=True)
    result = result.astype({"100s":"int", "50s": "int", "4s": "int", "6s": "int"})
    result.rename(columns={"bowling_team": "Teams"}, inplace=True)
    return result