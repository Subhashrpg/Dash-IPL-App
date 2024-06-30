from bs4 import BeautifulSoup
import regex as re
import json
import os

# directory of containing html file
directory = "D:\Subhash\Projects\python\page_sources"

# all data dictionary
all_matches_data = {}

# defining base classes  =========
base_classes_type1 = r"flex gap-2 p-2 tb:p-5 border-b border-r-2 border-cbBorderGrey items-center h-\[80px\]"
optional_classes_type1 = r"(?: \bborder-t\b)?(?: \bbg-cbAntiFlash\b)?(?: \bbg-pink-50\b)?"

base_classes_type2 = r"flex gap-2 p-2 tb:p-5 border-b border-cbBorderGrey items-center justify-end text-right h-\[80px\]"
optional_classes_type2 = r"(?: \bborder-t\b)?(?: \bbg-cbAntiFlash\b)?(?: \bbg-pink-50\b)?"

# Compile the regex patterns
pattern_type1 = re.compile(base_classes_type1 + optional_classes_type1)
pattern_type2 = re.compile(base_classes_type2 + optional_classes_type2)


# iterate over all the file
left_matches = [3, 4, 10, 11, 17, 18, 22, 24, 25, 31, 32, 35, 38, 39, 45, 46, 52, 53] 
# for file_number in range(1,58):
for file_number in left_matches:
    file_path = os.path.join(directory, f"page{file_number}.html")

    with open(file_path, 'r', encoding='latin-1') as file:
        html = file.read()
   
    soup = BeautifulSoup(html, "html.parser")

    # extracting heading of the match
    heading = soup.find("h1", class_="py-2 px-4 flex").text
    match_number = heading.split(",")[1].split("\xa0")[0].strip()

    # extracting team names
    team_names = heading.split(",")[0]
    team_1_name, team_2_name = [name.strip() for name in team_names.split("vs")]

    # player data container
    team_container = soup.find("div", class_= "w-full flex")

    # both team container
    div_players = team_container.find_all("div", class_="w-1/2")
    div_1 = div_players[0]
    div_2 = div_players[1]

    # initialize team data 
    team1_data = {"name": team_1_name, "team1_players": []}
    team2_data = {"name": team_2_name, "team2_players": []}

    # Find all matching elements using the regex pattern and extracting teams data div
    elements_type1 = div_1.find_all("a", class_=pattern_type1)
    elements_type2 = div_2.find_all("a", class_=pattern_type2)

    # Extracting team 1 data
    for anchor in elements_type1:
        name = anchor.find("div", class_= "flex flex-row items-center justify-start").text
        team1_data["team1_players"].append(name)
    

    # Extracting team 2 data
    for anchor in elements_type2:
        name = anchor.find("div", class_= "flex flex-row items-center justify-end").text
        team2_data["team2_players"].append(name)

    # all match data 
    all_matches_data[match_number] = {
        "team1": team1_data,
        "team2": team2_data
    }

# Converting dictionary to a Json String
json_data = json.dumps(all_matches_data, indent=4)

# Saving the data
with open(rf"D:\Subhash\Projects\python\page_sources\all_matches.json", "w") as json_file:
    json_file.write(json_data)