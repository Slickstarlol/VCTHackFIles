import csv
import json
import os
from collections import OrderedDict

def load_team_data(team_files):
    team_data = {}
    for team_file in team_files:
        with open(team_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for team in data:
                team_name = team.get('Team Name')
                if team_name:
                    team_data[team_name] = team
    return team_data

def insert_country_after_team(content_json_str, team_data_dict):
    # Parse the player's JSON content
    data = json.loads(content_json_str)
    
    team_name = data.get('Team')
    if team_name and team_name in team_data_dict:
        country = team_data_dict[team_name].get('Country', 'Unknown')
    else:
        country = 'Unknown'

    # Return None if country is 'Unknown' to indicate the row should be skipped
    if country == 'Unknown':
        return None

    # Create an ordered dict to maintain the order and insert 'Country' after 'Team'
    ordered_data = OrderedDict()
    keys = list(data.keys())
    for i, key in enumerate(keys):
        ordered_data[key] = data[key]
        if key == 'Team':
            # Insert 'Country' after 'Team'
            ordered_data['Country'] = country

    # Serialize back to JSON string
    updated_content_json_str = json.dumps(ordered_data, ensure_ascii=False)
    return updated_content_json_str

def process_csv_file(csv_filename, team_data_dict):
    # Read the CSV file
    with open(csv_filename, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Process each row
    updated_rows = []
    for row in rows:
        content_json_str = row['Content']
        updated_content_json_str = insert_country_after_team(content_json_str, team_data_dict)
        if updated_content_json_str is not None:
            updated_rows.append({'Content': updated_content_json_str})
        else:
            # Skip the row if country is 'Unknown'
            continue

    # Write back to a new CSV file
    output_csv_filename = os.path.splitext(csv_filename)[0] + '_with_country_filtered.csv'
    with open(output_csv_filename, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow({'Content': row['Content']})

    print(f"Processed {csv_filename} and saved to {output_csv_filename}")
    print(f"Total rows after filtering: {len(updated_rows)}")

if __name__ == "__main__":
    # List of team data files
    team_files = [
        'team_data_asia-pacific.json',
        'team_data_brazil.json',
        'team_data_china.json',
        'team_data_europe.json',
        'team_data_group_challengers.json',
        'team_data_japan.json',
        'team_data_korea.json',
        'team_data_latin_america_north.json',
        'team_data_latin_america_south.json',
        'team_data_middle_east_north_africa.json',
        'team_data_north_america.json',
        'team_data_oceania.json'
    ]

    # Load team data into a dictionary
    team_data_dict = load_team_data(team_files)

    # List of player data CSV files to process
    csv_files = [
        'players_data_challengers.csv',
        'players_data_game_changer.csv',
        'players_data_vct.csv'
    ]

    # Process each CSV file
    for csv_file in csv_files:
        if os.path.isfile(csv_file):
            process_csv_file(csv_file, team_data_dict)
        else:
            print(f"File {csv_file} not found.")
