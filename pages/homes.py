from data_loader import delivery, matches
import pandas as pd

class Home():

    # constructor
    def __init__(self, df1=delivery, df2=matches) -> None:
        self.df1 = df1
        self.df2 = df2

    # unique year
    def unique_years(self):
        return self.df2["season"].unique().tolist()
    
    # season dataframe filter
    def season_dataframe(self, season):
        if season != "Overall":
            season_df2 = self.df2[self.df2["season"] == season]
            season_df1 = pd.merge(self.df1, season_df2, left_on='match_id', right_on="id")
            
            return season_df1, season_df2
        else:
            temp_df1 = pd.merge(self.df1, self.df2, left_on="match_id", right_on="id", how="outer")
            return temp_df1, self.df2
        
    # total match_played
    def match_played(self, season):
        m_df1, m_df2 = self.season_dataframe(season=season)

        return m_df2["id"].value_counts().sum()

    # most run team
    def team_best_score(self, season, ascending = [False, True]):
        m_df1, m_df2 = self.season_dataframe(season=season)

        best_score = m_df1.groupby(["season", "batting_team", "match_id"]).agg({"total_runs" : "sum", "is_wicket" : "sum"}).reset_index().sort_values(by=["total_runs", "is_wicket"], ascending=ascending).head(1)
        
        if season != "Overall":
            return best_score["batting_team"].values[0], best_score["total_runs"].values[0], best_score["is_wicket"].values[0]
        else:
            return best_score["batting_team"].values[0], best_score["total_runs"].values[0], best_score["is_wicket"].values[0], best_score["season"].values[0]
    
    # most run individual
    def most_runs_batter(self, season):
        m_df1, m_df2 = self.season_dataframe(season=season)

        re_df = m_df1.groupby("batter")["batsman_runs"].sum().reset_index().sort_values(by="batsman_runs",ascending=False).head(1)
        return re_df["batter"].values[0], re_df["batsman_runs"].values[0]

    # most wicket
    def most_wicket_bowler(self, season):
        m_df1, m_df2 = self.season_dataframe(season=season)

        m_df3 = m_df1[~m_df1["dismissal_kind"].isin(["run out", "retired out", "retired hurt"])]
        bw_df = m_df3.groupby("bowler")["is_wicket"].sum().reset_index().sort_values(by="is_wicket", ascending=False).head(1)
        return bw_df["bowler"].values[0], bw_df["is_wicket"].values[0]

    # best individual Score
    def best_individual_score(self, season):
        m_df1, m_df2 = self.season_dataframe(season=season)

        ind_df = m_df1.groupby(["batter", "match_id", "season"])["batsman_runs"].sum().reset_index().sort_values(by="batsman_runs",ascending=False).head(1)

        if season == "Overall":
            return ind_df["batter"].values[0], ind_df["batsman_runs"].values[0], ind_df["season"].values[0]
        return ind_df["batter"].values[0], ind_df["batsman_runs"].values[0]
    
    # best bowling figure
    def best_bowling_figure(self, season):
        m_df1, m_df2 = self.season_dataframe(season=season)
        m_df3 = m_df1[~m_df1["dismissal_kind"].isin(["run out", "retired out", "retired hurt"])]

        bw_df = m_df3.groupby(["bowler", "season", "match_id"]).agg({"is_wicket" : "sum", "batsman_runs" : "sum"}).reset_index().sort_values(by=["is_wicket", "batsman_runs"], ascending=[False, True])

        if season != "Overall":
            return bw_df["bowler"].values[0], bw_df["batsman_runs"].values[0], bw_df["is_wicket"].values[0]
        return bw_df["bowler"].values[0], bw_df["batsman_runs"].values[0], bw_df["is_wicket"].values[0], bw_df["season"].values[0]
    
    # most sixes teams
    def sixes_count(self, season, metric="batting_team"):
        df_1, df_2 = self.season_dataframe(season)

        six_df_1 = df_1[df_1["batsman_runs"] == 6]
        r_six = six_df_1.groupby(metric)["batsman_runs"].count().reset_index().sort_values(by="batsman_runs",ascending=False).head(1)
        return r_six[metric].values[0], r_six["batsman_runs"].values[0]

    # final played
    def final_played_won(self, season):
        
        if season != "Overall":
            t_df = self.df2[(self.df2["season"] == season) & (self.df2["match_type"] == "Final")]
            return t_df["team1"].values[0], t_df["team2"].values[0], t_df["winner"].values[0]
        else:
            return self.most_final_played()
    
    # most final played
    def most_final_played(self):
        final_df1 = self.df2[self.df2.match_type == "Final"].groupby(["team1"])["match_type"].count().reset_index()
        final_df2 = self.df2[self.df2.match_type == "Final"].groupby(["team2"])["match_type"].count().reset_index()
        final_df = final_df1.merge(final_df2, how = "outer", left_on= "team1", right_on= "team2")
        final_df.fillna(0, inplace = True)
        final_df["final_played"] =  final_df["match_type_x"] + final_df["match_type_y"]
        final_df = final_df.sort_values(by="final_played", ascending=False).head(1)

        return final_df["team1"].values[0], final_df["final_played"].values[0]
    
    # most final won
    def most_final_won(self):
        m_final = self.df2[self.df2.match_type == "Final"]["winner"].value_counts().head(1)
        return m_final.index.values[0], m_final.values[0]
    
    # point table
    def point_table(self, season):
        p_df1, p_df2 = self.season_dataframe(season=season)

        t1 = p_df2["team1"].unique()
        t2 = p_df2["team2"].unique()
        teams = set(t1)&set(t2)
        new_df = pd.DataFrame()
        data = []
        
        for team in teams:
            match_played = p_df2[(p_df2["team1"] == team) | (p_df2["team2"] == team)].shape[0]
            win = p_df2[p_df2["winner"] == team].shape[0]
            no_result = p_df2[((p_df2["team1"] == team) | (p_df2["team2"] == team)) & (p_df2["winner"].isnull())].shape[0]

            data.append([team,match_played,win,no_result])
            
        new_df[["Team","Match","Win","No Result"]] = data
        new_df["Points"] = new_df["Win"] * 2 + new_df["No Result"]
        
        new_df.sort_values(by = "Points", ascending = False, inplace= True)
        return new_df
    
    # batsman vs bowler
    def batsman_vs_bowler(self, season, batter=None, bowler=None):
        return_df = pd.DataFrame()
        return_data = []
        p_df1, _ = self.season_dataframe(season=season)
        bat_bow_df = p_df1[(p_df1["batter"] == batter) & (p_df1["bowler"] == bowler)]

        matches = len(bat_bow_df["match_id"].unique())
        runs = bat_bow_df["batsman_runs"].sum()
        balls = bat_bow_df["ball"].count()

        wk_df = bat_bow_df[~bat_bow_df["dismissal_kind"].isin(["run out", "retired out", "retired hurt"])]
        wicket = wk_df["is_wicket"].sum()
        strike_rate = round((runs/balls)*100) if balls != 0 else 0
        value_counts = bat_bow_df["batsman_runs"].value_counts()
        sixes = value_counts.get(6, 0)
        fours = value_counts.get(4, 0)
        
        return_data.append([matches, runs, balls, strike_rate, wicket, sixes, fours])
        return_df[["Match", "Runs", "Balls", "Strike_rate", "Wicket", "Sixes", "Fours"]] = return_data

        return return_df
        