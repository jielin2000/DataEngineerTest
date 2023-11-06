import psycopg2
import pandas as pd


# Database connection parameters
db_params = {
    "dbname": "roaddata",
    "user": "user1",
    "password": "12345",
    "host": "db",
    "port": "5432"
}

# Path to the text file containing data
file_path = '/data/sample_file.txt'  # Update with the actual path to your text file

# Function to check if a table exists in the PostgreSQL database
def table_exists(cursor, table_name):
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
    return cursor.fetchone()[0]

# Function to format data to be saved in database
def parse_road_link(line):
    # Split the line by spaces
    parts = line.strip().split()

    # Check if the line contains at least three parts (road_id, direction, and polyline)
    if len(parts) < 3:
        return None

    # Extract the road_id, direction, and polyline parts
    road_id = parts[0]
    direction = parts[1]
    polyline = " ".join(parts[2:])

    return {
        "road_id": road_id,
        "direction": direction,
        "polyline": polyline,
    }

# Function to load data from the text file
def load_data(file_path):
    # Read the text file into a Pandas DataFrame
    parsed_data = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                parsed_line = parse_road_link(line)
                if parsed_line:
                    parsed_data.append(parsed_line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(1)
    return parsed_data

# Function to create table in the PostgreSQL database
def create_table_to_postgresql( conn):
    cursor = conn.cursor()

    # Insert data into the PostgreSQL table
    create_query = """ CREATE TABLE IF NOT EXISTS road_links (
                road_id INTEGER NOT NULL,
                direction INTEGER,
                polyline TEXT,
                PRIMARY KEY (road_id)
        )"""
    cursor.execute(create_query)

    conn.commit()
    cursor.close()

# Function to save data to the PostgreSQL database
def save_to_postgresql(dataframe, conn):
    cursor = conn.cursor()

    for data in dataframe:
        road_id = data["road_id"]
        direction = data["direction"]
        polyline = data["polyline"]

        # Insert data into the PostgreSQL table
        insert_query = "INSERT INTO road_links (road_id, direction, polyline) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (road_id, direction, polyline))

    conn.commit()
    cursor.close()

if __name__ == "__main__":
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)

        # Load data from the text file
        data = load_data(file_path)
        

        # Save data to the PostgreSQL database
        if table_exists(conn.cursor(), "road_links"):
            print("Table already exists, skipping data insertion.")
        else:
            create_table_to_postgresql(conn)
            save_to_postgresql(data, conn)
            print("Data loaded into PostgreSQL successfully.")
        conn.close()
        
    except Exception as e:
        print("Error:", e)
            