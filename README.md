# IPL Statistics Dashboard

## Table of Contents
- [Project Overview](#project-overview)
- [Motivation](#motivation)
- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Installation](#Installation)
- [Project Structure](#project-structure)
- [Data](#data)
- [Visualizations](#visualizations)
- [Examples](#examples)
- [Contributing](#contributing)
- [Future Work](#future-work)
- [License](#license)
- [Contact](#contact)

## Project Overview
- What is the IPL Team Statistics Dashboard?
  - It is IPL Dashboard cosists of four pages :-
      - **Batsman Page** - It displays detailed information about all the batsmen who have played in the IPL.
      - **Bowler Page** - It displays detailed information about all the bowler who have played in the IPL.
      - **Team Page** - It displays detailed information about all the teams who have played in the IPL.
      - **Home Page** - It displays detailed information related to IPL overall.
- What problem does it solve
  - Currently, IPL data is decentralized, requiring you to visit different pages or sources for complete information. This app consolidates all IPL information in one place, offering a time-saving and highly interactive dashboard.
- Who is it for?
  - Anyone who is interested in cricket.

## Motivation
Motivation behind the project:
- Why did I create this dashboard
  I am a die-hard fan of cricket and wanted to have all the information and records of the IPL in one place.
- What inspired me
  I draw inspiration from real-world projects and my profound passion for cricket, particularly in delving into its statistics and analysis. This drive fuels my ambition to create meaningful contributions in the realm of sports analytics.
- What are the benefits of using this dashboard?
  - 1. **Comprehensive Information**: Access detailed statistics and insights about IPL teams, matches, and player performances, all in one centralized platform.

  - 2. **Time Efficiency**: Save time by finding all IPL-related information conveniently in one dashboard instead of searching multiple sources.
    
  - 3. **Interactive Visualization**: Explore interactive charts and graphs that enhance understanding and analysis of cricket data.
    
  - 4. **Ease of Use**: Designed with a user-friendly interface, the dashboard is accessible to cricket enthusiasts and analysts alike, making complex data more approachable.
    
  - 5. **Decision Support**: Empower yourself to make informed decisions based on robust data insights, whether for fan engagement or strategic analysis.
    
  - 6. **Continuous Updates**: Stay informed with up-to-date information and analytics, reflecting ongoing IPL seasons and developments.
    
    Overall, the IPL Team Statistics Dashboard enriches the user experience and serves as a valuable tool for anyone passionate about cricket analysis and insights.

## Features
Key features of project:
- **Team Statistics**: Detailed statistics for each IPL team.
- **Interactive Visualizations**: Dynamic charts and graphs for a better understanding of data.
- **Season Comparisons**: Analyze and compare team performance across different seasons.
- **User-Friendly Interface**: Easy navigation and intuitive design.

## Demo
Short video of the project:
- [Live Demo](#)

Here is a screenshot of the dashboard:

##### Batsman Page 
<img src="https://github.com/Subhashrpg/Dash_Ipl_App/blob/main/assets/screen%20shots/batsman_page.png" width="400" hspace="20">

##### Bowler Page 
<img src="https://github.com/Subhashrpg/Dash_Ipl_App/blob/main/assets/screen%20shots/bowler_page.png" width="400" hspace="20">

##### Team Page 
<img src="https://github.com/Subhashrpg/Dash_Ipl_App/blob/main/assets/screen%20shots/teams_page.png" width="400" hspace="20">

##### Home Page 
<img src="https://github.com/Subhashrpg/Dash_Ipl_App/blob/main/assets/screen%20shots/home%20page.png" width="400" hspace="20">

## Technologies Used
List the technologies and libraries used in the project:
- **Dash**: Used for frotend of the application.
- **pandas**: Used for data manipulation and analysis.
- **plotly**: Used for creating interactive plots.
- **BeautifulSoup**: Used for scraping of the misssing data.
- **Regex**: Used for finding pattern for data scraping.
- **Selenuim**: Used for automation of webpages from which data were scraped.
- **Python**: The core programming language for the project.

## Installation
Hit this link in your browser and you will get the wepage.
1. **Website**:
   ```sh
   git clone https://github.com/yourusername/ipl-dashboard.git

## Project Structure
```
Dash_app:.
├───analysis
├───assets
│   └───screen shots
├───datasets
├───layout
├───pages
└───page_source
    └───processed data
```

## Data
The data used in this project is sourced from various publicly available IPL datasets. Here are the details:

#### Source
- The primary data source is [Kaggle IPL Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020).
- Additional data is sourced from [Cricbuzz](https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/stats).
- 
##### Data Files
- delivery.csv - this file contains ball by ball record for each match like batsman name, non striker, bowler , runs on that ball an so on.
- matches.csv - in this file there is overall information related to match like venue, toss, umpire, winning margin and so on.

## Visualizations
The dashboard includes various visualizations such as bar charts and line graphs to represent different aspects of IPL statistics.

## Examples
```
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
```

## Contributing
This communicates that while contributions are not actively sought at the moment, you are open to feedback and ideas. It also provides a contact point for anyone who wants to get in touch regarding the project. Adjust the email address as per your preference.

## Future Work
- coding the batsman.py file using OOP
- Utilize encapsulation and inheritance to reduce redundancy, as many functionalities are repeated.
- Enhance data sharing among callbacks, as the same data is used in various parts of the callbacks.
- Separate functions according to different use cases. Currently, a single function handles all tasks, but functionality needs to be divided
- Some data is missing from files and needs completion using scraping from various sources.
These modifications aim to improve code organization, reduce redundancy, and enhance data handling and functionality.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries, please contact me at [subhashrs1997@gmail.com].
