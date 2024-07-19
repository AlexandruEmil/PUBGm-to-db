# PUBGm-to-db

Real-Time Match Data Processor
This script fetches match data from an API endpoint, updates an SQLite database, and calculates total points for each team based on their performance. The script runs continuously, fetching and updating data every 2 seconds.

![Diagram](https://github.com/user-attachments/assets/6b63f99f-1401-4f2a-a2eb-32a5674e2da6)

Features
Connects to an SQLite database.
Creates tables for storing match data and final aggregated points if they do not exist.
Fetches JSON data from a specified API endpoint.
Parses the JSON data to extract relevant team and player information.
Updates or inserts data into the match table based on the fetched information.
Calculates total points for each team based on predefined rules.
Updates a final table that aggregates total points from multiple matches.
Runs continuously, fetching and updating data every 2 seconds.

team_name (TEXT): The name of the team.
kill_num (INTEGER): The number of kills by the team.
rank (INTEGER): The rank of the team.
total_points (INTEGER, DEFAULT 0): The total points for the team.
team_name (TEXT): The name of the team.
total_points (INTEGER): The aggregated total points from all matches.

Usage
python match_data_processor.py
