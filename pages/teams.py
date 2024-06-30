from data_loader import delivery, matches
import pandas as pd

class Teams():
    # constructor
    def __init__(self,df1=delivery, df2=matches) -> None:
        self.df1 = df1
        self.df2 = df2
        self.batting_team = None
        self.bowling_team = None
    
    # mergin dataframes(season dataframe)
    def season_dataframe(self, season):
        if season != "Overall":
            season_df = self.df2[self.df2["season"] == season]
            season_values = self.df2[self.df2["season"] == season].id.values
            return self.df1[self.df1["match_id"].isin(season_values)], season_df
        else:
            temp_df1 = pd.merge(self.df1, self.df2, left_on="match_id", right_on="id", how="outer")
            return temp_df1, self.df2
    
    # teams dataframe
    def teams_df(self, season, batting_team=None, bowling_team=None):
        season_df, _ = self.season_dataframe(season=season)
        if batting_team:
            r_df = season_df[season_df["batting_team"] == batting_team]
        elif bowling_team:
            r_df = season_df[season_df["bowling_team"] == bowling_team]
        
        return r_df
        
    # getting unique teams
    def total_teams(self):
        self.batting_team = self.df1["batting_team"].unique()
        self.bowling_team = self.df1["bowling_team"].unique()
        return list(set(self.batting_team)&set(self.bowling_team))
    
    # getting season played
    def get_played_season(self, team, df1=delivery, df2=matches):
        ids = df1[(df1["bowling_team"] == team) | (df1["batting_team"] == team)]["match_id"].unique()
        return df2[df2["id"].isin(ids)]["season"].unique().tolist()
    
    # best powerplay
    def best_vs_worst_powerplay(self, teams, season, ascending=False):
        batting_df = self.teams_df(season=season, batting_team=teams)
        r_df = batting_df[batting_df["over"].isin([0,1,2,3,4,5])]

        if season != "Overall":
            r_df = r_df.groupby(["match_id", "bowling_team"]).agg({"total_runs": "sum", "is_wicket": "sum"}).reset_index().sort_values(by="total_runs", ascending=ascending).head(1)
        else:
            r_df = r_df.groupby(["match_id", "bowling_team", "season"]).agg({"total_runs": "sum", "is_wicket": "sum"}).reset_index().sort_values(by="total_runs", ascending=ascending).head(1)   
        
        return r_df["bowling_team"].values[0], r_df["total_runs"].values[0], r_df["is_wicket"].values[0]
    
    # last five overs recors
    def last_five_overs(self, teams, season):
        bat_df = self.teams_df(season=season, batting_team=teams)
        lst_fv_df = bat_df[bat_df["over"].isin([15,16,17,18,19])]

        if season != "Overall":
            final_df = lst_fv_df.groupby(["match_id", "bowling_team"]).agg({"total_runs": "sum", "is_wicket": "sum"}).reset_index().sort_values(by="total_runs", ascending=False).head(1)
        else:
            final_df = lst_fv_df.groupby(["match_id", "bowling_team", "season"]).agg({"total_runs": "sum", "is_wicket": "sum"}).reset_index().sort_values(by="total_runs", ascending=False).head(1)    
        
        return final_df["bowling_team"].values[0], final_df["total_runs"].values[0], final_df["is_wicket"].values[0]
    
    # best score
    def best_vs_worst_score_teams(self, teams, season, ascending=False):
        batting_df = self.teams_df(season=season, batting_team=teams)
        # getting best score
        if season != "Overall":
            fn_df = batting_df.groupby(["match_id", "bowling_team"]).agg({"total_runs": "sum", "is_wicket": "sum"}).reset_index().sort_values(by="total_runs", ascending=ascending).head(1)
        else:
            fn_df = batting_df.groupby(["match_id", "bowling_team", "season"]).agg({"total_runs": "sum", "is_wicket": "sum"}).reset_index().sort_values(by="total_runs", ascending=ascending).head(1)

        return fn_df["bowling_team"].values[0], fn_df["total_runs"].values[0], fn_df["is_wicket"].values[0]
    
    # best individual score
    def best_individual_score(self, teams, season):
        ind_df = self.teams_df(season=season, batting_team=teams)

        # getting best score
        if season != "Overall":
            b_ind_df = ind_df.groupby(["match_id", "bowling_team", "batter"])["batsman_runs"].sum().reset_index().sort_values(by="batsman_runs", ascending=False).head(1)
        else:
            b_ind_df = ind_df.groupby(["match_id", "bowling_team", "batter", "season"])["batsman_runs"].sum().reset_index().sort_values(by="batsman_runs", ascending=False).head(1)
        
        return b_ind_df["bowling_team"].values[0], b_ind_df["batter"].values[0], b_ind_df["batsman_runs"].values[0]
    
    # best individual bowler
    def best_bowler_ind_df(self, teams, season):
        bt_df = self.teams_df(season=season, bowling_team=teams)
        bt_df = bt_df[~bt_df["dismissal_kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]

        # getting best score
        if season != "Overall":
            b_bt_df = bt_df.groupby(["match_id", "batting_team", "bowler"]).agg({"batsman_runs" : "sum", "is_wicket" : "sum"}).reset_index().sort_values(by= ["is_wicket", "batsman_runs"], ascending=[False,True]).head(1)
        else:
            b_bt_df = bt_df.groupby(["match_id", "batting_team", "bowler", "season"]).agg({"batsman_runs" : "sum", "is_wicket" : "sum"}).reset_index().sort_values(by= ["is_wicket", "batsman_runs"], ascending=[False,True]).head(1)
        
        return b_bt_df["batting_team"].values[0], b_bt_df["bowler"].values[0], b_bt_df["batsman_runs"].values[0], b_bt_df["is_wicket"].values[0]
    
    # Highest scorer
    def highest_scorer(self, teams, season):
        hs_df = self.teams_df(season=season, batting_team=teams)
        dff = hs_df.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False)

        return dff.index[0], dff.values[0]
    
    # highest wicket taker
    def highest_wicket_taker(self, teams, season):
        hs_wkt_df = self.teams_df(season=season, bowling_team=teams)
        hs_wkt_df = hs_wkt_df[~hs_wkt_df["dismissal_kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]

        dff_1 = hs_wkt_df.groupby("bowler")["is_wicket"].sum().sort_values(ascending=False)
        return dff_1.index[0], dff_1.values[0]
    
    # sixes in powerplay 
    def powerplay_sixes(self, teams, season, overs=None):
        pw_df = self.teams_df(season=season, batting_team=teams)
        if overs:
            pw_df = pw_df[pw_df["over"].isin(overs)]
        sx_df = pw_df[pw_df["batsman_runs"] == 6]

        return sx_df["batsman_runs"].count()
        
    # final played
    def total_final_played(self, teams, season="Overall"):
        if season == "Overall":
            final_df = self.df2[self.df2["match_type"] == "Final"]
            final_team_df = final_df[(final_df["team1"] == teams) | (final_df["team2"] == teams)]
            return final_team_df["match_type"].count()
        else:
            return None
    
    # final won
    def total_final_won(self, teams, season="Overall"):
        if season == "Overall":
            final_df = self.df2[self.df2["match_type"] == "Final"]
            final_team_df = final_df[final_df["winner"] == teams]
            return final_team_df["match_type"].count()
        else:
            return None
    
    # point table
    def point_table(self, team, season):
        point_df = pd.DataFrame()
        t_df1, t_df2 = self.season_dataframe(season=season)
        match_played = t_df2[(t_df2["team1"] == team) | (t_df2["team2"] == team)].shape[0]
        win_matches = t_df2[t_df2["winner"] == team].shape[0]
        no_result = t_df2[((t_df2["team1"] == team) | (t_df2["team2"] == team)) & (t_df2["winner"].isnull())].shape[0]
        win_percent = round((win_matches/match_played) * 100, 2)
        home_win = round((t_df2[(t_df2["winner"] == team) & (t_df2["team1"] == team)].shape[0]/ t_df2[t_df2["team1"] == team].shape[0]) * 100,2)
        away_win = round((t_df2[(t_df2["winner"] == team) & (t_df2["team2"] == team)].shape[0]/ t_df2[t_df2["team2"] == team].shape[0]) * 100,2)

        point_df[["Matches", "Win", "No Result", "Win%", "Home_win%", "Away_win%"]] = [[match_played, win_matches, no_result, win_percent, home_win, away_win]]

        point_df["Points"] = point_df["Win"] * 2 + point_df["No Result"]
        
        return point_df
    
    # head to head stats
    def head_to_head_match_played(self, team_1, season, team_2):
        t_df1, t_df2 = self.season_dataframe(season=season)
        head_df = t_df2[((t_df2["team1"] == team_1) | (t_df2["team2"] == team_1)) & ((t_df2["team1"] == team_2) | (t_df2["team2"] == team_2))]
        
        if head_df.empty:
            return None
        return head_df.groupby(["id"])["team1"].count().reset_index()["team1"].count()
    
    # head to head win
    def head_to_win(self, team_1, season, team_2):
        t_df1, t_df2 = self.season_dataframe(season=season)
        head_df = t_df2[((t_df2["team1"] == team_1) | (t_df2["team2"] == team_1)) & ((t_df2["team1"] == team_2) | (t_df2["team2"] == team_2))]
        win_df = head_df.groupby(["id", "winner"])["team1"].count().reset_index()["winner"].value_counts().reset_index()

        if win_df.empty:
            return None, None, None, None
        return win_df["winner"][0], win_df["winner"][1], win_df["count"][0], win_df["count"][1]
