import json
import pandas as pd

def merge_json_file(input_file, output_file):
    merged_data = {}
    for path in input_file:
        with open(path, "r") as in_file:
            data = json.load(in_file)
            merged_data.update(data)
    
    with open(output_file, "w") as out_file:
        json.dump(merged_data, out_file, indent=4)

# input json file paths
input_file_paths = [r"page_sources\all_matches_data.json", r"page_sources\all_matches.json"]
# output json file paths
output_file_paths = r"page_sources\full_matches.json"
# excel file path
excel_file = r"page_sources\matches_data.xlsx"

# calling the function
# merge_json_file(input_file_paths, output_file_paths)

# Reading json file
with open(output_file_paths, "r") as file:
    data = json.load(file)

# preparing data for dataframe
rows = []

for match_number, match_data in data.items():
    team1_name = match_data["team1"]["name"]
    team2_name = match_data["team2"]["name"]
    team1_players = match_data["team1"]["team1_players"]
    team2_players = match_data["team2"]["team2_players"]

    row = {
        "match_number": match_number,
        "team1": team1_name,
        "team2": team2_name,
        "team1_players": team1_players,
        "team2_players": team2_players
    }
    rows.append(row)

# create dataframe
df = pd.DataFrame(rows)

# write dataframe to excel file 
df.to_excel(excel_file, index=False)

print(f"Data has been written to {excel_file}")