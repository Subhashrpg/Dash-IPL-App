from data_loader import delivery, matches
import pandas as pd

class Bowlers:
    # constructor==================
    def __init__(self, df1=delivery, df2=matches, bowler=None, season="Overall") -> None:
        self.df1 = df1
        self.df2 = df2
        self.bowler = bowler
        self.season = season

    # season dataframe=============
    def unique_bowlers(self):
        return self.df1.bowler.str.strip().unique().tolist()

    # bowlers played in ipl(years calculate)
    def bowler_year(self, bowler):
        ids = self.df1[self.df1.bowler == bowler].match_id.unique()
        return self.df2[self.df2["id"].isin(ids)]["season"].unique().tolist()

    # season dataframe
    def season_dataframe(self, season):
        if season != "Overall":
            season_df = self.df2[self.df2["season"] == season]
            season_values = self.df2[self.df2["season"] == season].id.values
            return self.df1[self.df1["match_id"].isin(season_values)], season_df
        else:
            temp_df1 = pd.merge(self.df1, self.df2, left_on="match_id", right_on="id", how="outer")
            return temp_df1, self.df2
        
    # bowler dataframe
    def bowler_dataframe(self, df1, bowler="JJ Bumrah"):
        return df1[df1.bowler == bowler]
    
    # match vs innings played
    def match_vs_innings_played(self, bowler="JJ Bumrah", season="Overall"):
        self.s_df1, self.s_df2 = self.season_dataframe(season=season)
        self.b_df = self.bowler_dataframe(df1=self.s_df1, bowler=bowler)

        matches_played = self.s_df2[(self.s_df2.Team1Players.str.contains(bowler)) | (self.s_df2.Team2Players.str.contains(bowler))].shape[0]
        innings = len(self.b_df.groupby("match_id")["bowler"].count().index.tolist())
        return matches_played, innings
    
    # balls,runs,wicket,economy,average
    def balls_runs_wicket_economy_avg(self, bowler="JJ Bumrah", season="Overall"):
        self.s_df1, self.s_df2 = self.season_dataframe(season=season)
        self.b_df = self.bowler_dataframe(df1=self.s_df1, bowler=bowler)

        total_balls = self.b_df["ball"].count()
        total_runs = self.b_df[~self.b_df["extras_type"].isin(["legbyes","byes","penalty"])]["total_runs"].sum()
        total_wicket = self.b_df[~self.b_df["dismissal_kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]["dismissal_kind"].count()

        if total_balls != 0 or total_wicket != 0:
            ecomomy = round((total_runs/total_balls)*6,2)
            average = round(total_runs/total_wicket,2)
        else:
            ecomomy = total_runs
            average = total_balls

        return total_balls, total_runs, total_wicket, ecomomy, average
    
    # getting 3w and 5w innings 
    def three_vs_five_wickets_bestinnings(self, bowler="JJ Bumrah", season="Overall"):
        s_df1, s_df2 = self.season_dataframe(season=season)
        b_df = self.bowler_dataframe(df1=s_df1, bowler=bowler)

        inning_runs = b_df[~b_df["extras_type"].isin(["legbyes","byes","penalty"])].groupby("match_id")["total_runs"].sum().reset_index()
        inning_wicket_df = b_df[~b_df["dismissal_kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
        inning_wicket = inning_wicket_df.groupby("match_id")["is_wicket"].sum().reset_index()

        bbi_df = inning_runs.merge(inning_wicket, on = "match_id").rename(columns= {"is_wicket": "wicket"})
        best_inning = bbi_df.sort_values(by = ["wicket","total_runs"], ascending = [False,True])

        try:
            bbi_run = best_inning["total_runs"].head(1).values[0]
            bbi_wicket = best_inning["wicket"].head(1).values[0]
        except IndexError:
            bbi_run = 0
            bbi_wicket = 0
        best_match = f"{bbi_run}/{bbi_wicket}"

        wicket_df = inning_wicket_df.groupby(["bowler", "match_id"])["is_wicket"].sum().reset_index()
        three_wicket = wicket_df[(wicket_df["is_wicket"] <= 4) & (wicket_df["is_wicket"] >= 3)]["is_wicket"].count()
        five_wicket = wicket_df[wicket_df["is_wicket"] >= 5]["is_wicket"].count()

        return best_match, three_wicket, five_wicket
    
    # getting records for bowlers against teams
    def match_played_against_teams(self, bowler="JJ Bumrah", season="Overall"):
        temp_df1, temp_df2 = self.season_dataframe(season=season)
        temp_df3 = self.bowler_dataframe(df1=temp_df1, bowler=bowler)
        
        return temp_df3.groupby(["match_id", "batting_team"])["bowler"].count().reset_index()["batting_team"].value_counts().reset_index().rename(columns={"count": "Matches"})
            
    # balls against teams
    def run_wickets_economy_avg_against_teams(self, bowler="JJ Bumrah", season="Overall"):
        temp_df1, temp_df2 = self.season_dataframe(season=season)
        temp_df3 = self.bowler_dataframe(df1=temp_df1, bowler=bowler)

        # getting runs
        ball_df = temp_df3.groupby(["batting_team"])["ball"].count().reset_index().rename(columns={"ball" : "Balls"})
        run_df = temp_df3[~temp_df3["extras_type"].isin(["legbyes","byes","penalty"])]
        run_df1 = run_df.groupby("batting_team").total_runs.sum().reset_index().rename(columns={"total_runs": "Runs"})

        # getting wickets
        wicket_df = temp_df3[~temp_df3["dismissal_kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
        wicket_df1 = wicket_df.groupby("batting_team").is_wicket.sum().reset_index().rename(columns={"is_wicket": "Wickets"})
        run_wicket_df = ball_df.merge(run_df1, on="batting_team", how="outer").merge(wicket_df1, on = "batting_team", how = "outer")

        # getting best innings
        best_run = run_df.groupby(["match_id","batting_team"]).total_runs.sum().reset_index()
        best_wicket = wicket_df.groupby(["match_id","batting_team"]).is_wicket.sum().reset_index()
        best_inning = best_run.merge(best_wicket, on = ["match_id","batting_team"], how = "outer").sort_values(
            by = ["is_wicket","total_runs"], ascending = [False,True]).drop(columns = "match_id")
        bbi_df = best_inning.loc[best_inning.groupby("batting_team").is_wicket.idxmax()]
        bbi_df["BBM"] = bbi_df.total_runs.astype("str") +"/" + bbi_df.is_wicket.astype("str")
        bbi_df = bbi_df.drop(columns = ["total_runs","is_wicket"])

        # three and five wickets df
        three_wicket = best_inning[(best_inning.is_wicket <= 4) & (best_inning.is_wicket >= 3)].groupby("batting_team").is_wicket.count().reset_index()
        five_wicket = best_inning[best_inning.is_wicket >= 5].groupby("batting_team").is_wicket.count().reset_index()
        three_five_df = three_wicket.merge(five_wicket, on = "batting_team", how = "outer")

        # merging all datas in one 
        final_df1 = run_wicket_df.merge(bbi_df, on="batting_team", how="outer")
        
        # getting economy and avg for bowlers
        final_df1["Economy"] = final_df1.apply(lambda row: round(round(row["Runs"] / row["Balls"], 2) * 6, 2) if row["Balls"] != 0 else 0, axis=1)
        final_df1["Average"] = final_df1.apply(lambda row : round(row["Runs"] / row["Wickets"],2) if row["Wickets"] != 0 else row["Runs"], axis = 1)

        return final_df1.merge(three_five_df, on="batting_team", how="outer").rename(
    columns = {"is_wicket_x":"3W","is_wicket_y": "5w"})

    # line chart data getting
    def process_season_df_line_chart(self,bowler="JJ Bumrah", season="Overall"):
        temp_df1, temp_df2 = self.season_dataframe(season=season)
        temp_df3 = self.bowler_dataframe(df1=temp_df1, bowler=bowler)

        # getting wickets, average, economy
        ball_df = temp_df3.groupby(["bowler", "season"])["ball"].count().reset_index()
        run_df = temp_df3[~temp_df3["extras_type"].isin(["legbyes","byes","penalty"])].groupby(["season", "bowler"])["total_runs"].sum().reset_index().rename(columns={"total_runs": "Runs"})
        # getting wickets for season
        wicket_df = temp_df3[~temp_df3["dismissal_kind"].isin(["run out","retired hurt","obstructing the field","retired out"])].groupby(["season", "bowler"])["dismissal_kind"].count().reset_index().rename(columns={'dismissal_kind' : 'Wickets'})

        # calculation economy and average
        final_df = run_df.merge(ball_df, on=["bowler", "season"], how="outer").merge(wicket_df, on=["bowler", "season"], how="outer")
        final_df["Economy"] = final_df.apply(lambda row: round(round(row["Runs"] / row["ball"], 2) * 6, 2) if row["ball"] != 0 else 0, axis=1)
        final_df["Average"] = final_df.apply(lambda row : round(row["Runs"] / row["Wickets"],2) if row["Wickets"] != 0 else row["Runs"], axis = 1)

        return final_df

