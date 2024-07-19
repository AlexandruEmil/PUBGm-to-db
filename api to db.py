import requests
import sqlite3
import time

# Connect to the SQLite database
conn = sqlite3.connect("Test.db")  # Replace with the actual database file name
cursor = conn.cursor()

# Function to create the final table and insert the sum of points
def update_final_table():
    # Create the final table if it doesn't exist
    create_final_table_statement = """
        CREATE TABLE IF NOT EXISTS final_table (
            team_name TEXT,
            total_points INTEGER
        )
    """
    cursor.execute(create_final_table_statement)

    # Delete existing data from the final table
    delete_data_statement = "DELETE FROM final_table"
    cursor.execute(delete_data_statement)

    # Insert the sum of points from the four tables into the final table
    insert_final_table_statement = """
        INSERT INTO final_table (team_name, total_points)
        SELECT team_name, SUM(total_points) AS total_points
        FROM (
            SELECT team_name, total_points FROM game1
            UNION ALL
            SELECT team_name, total_points FROM game2
            UNION ALL
            SELECT team_name, total_points FROM game3
            UNION ALL
            SELECT team_name, total_points FROM game4
        ) AS combined_data
        GROUP BY team_name;
    """
    cursor.execute(insert_final_table_statement)

    # Commit the changes
    conn.commit()

# Get the table name from user input
table_name = input("Enter the table name: ")

# Create the table if it doesn't exist
create_table_statement = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        team_name TEXT,
        kill_num INTEGER,
        rank INTEGER,
        total_points INTEGER DEFAULT 0
    )
"""
cursor.execute(create_table_statement)

while True:
    # Fetch the JSON data from the API endpoint for the match
    url = "http://127.0.0.1:5000/data1"  # Replace with the actual API endpoint URL for the match
    response = requests.get(url)
    data = response.json()

    # Parse the JSON data and extract the required information for the match
    team_data = data["allinfo"]["TeamInfoList"]
    player_data = data["allinfo"]["TotalPlayerList"]

    # Update the existing data or insert new data into the SQLite table for the match
    for team in team_data:
        team_name = team["teamName"]
        kill_num = team["killNum"]
        player = next((player for player in player_data if player["teamId"] == team["teamId"]), None)
        rank = player["rank"] if player else None

        # Check if the team already exists in the table for the match
        select_statement = f"SELECT * FROM {table_name} WHERE team_name = ?"
        cursor.execute(select_statement, (team_name,))
        existing_team = cursor.fetchone()

        if existing_team:
            # Team exists, update the data for the match
            update_statement = f"UPDATE {table_name} SET kill_num = ?, rank = ? WHERE team_name = ?"
            cursor.execute(update_statement, (kill_num, rank, team_name))
        else:
            # Team doesn't exist, insert new data for the match
            insert_statement = f"INSERT INTO {table_name} (team_name, kill_num, rank) VALUES (?, ?, ?)"
            cursor.execute(insert_statement, (team_name, kill_num, rank))

    # Commit the changes after each iteration
    conn.commit()

    # Calculate the total points based on the rules and update the corresponding rows
    update_points_statement = f"""
        UPDATE {table_name} SET total_points = kill_num +
            CASE
                WHEN rank = 1 THEN 10
                WHEN rank = 2 THEN 6
                WHEN rank = 3 THEN 5
                WHEN rank = 4 THEN 4
                WHEN rank = 5 THEN 3
                WHEN rank = 6 THEN 2
                WHEN rank IN (7, 8) THEN 1
                ELSE 0
            END
    """
    cursor.execute(update_points_statement)

    # Update the final table with the latest sum of points
    update_final_table()

    # Print a general message indicating that the data has been updated and total points calculated
    print("Data updated and total points calculated at:", time.strftime("%Y-%m-%d %H:%M:%S"))

    # Delay for 2 seconds before the next iteration
    time.sleep(2)

# Close the connection
conn.close()
