import csv
import json
import os

def add_igl_info_single_file(player_csv_file_path, igl_json_file_path, output_csv_file_path):
    # Read IGL data
    with open(igl_json_file_path, 'r', encoding='utf-8') as igl_file:
        igl_data = json.load(igl_file)

    # Build a set of IGL names (normalized to lowercase for comparison)
    igl_names = set()
    for igl in igl_data:
        igl_name = igl.get('In-Game Name', '').lower()
        igl_names.add(igl_name)

    # List to hold modified player data
    modified_rows = []

    # Process the player data CSV file
    if not os.path.isfile(player_csv_file_path):
        print(f"File not found: {player_csv_file_path}")
        return

    with open(player_csv_file_path, 'r', encoding='utf-8', newline='') as player_csv_file:
        csv_reader = csv.reader(player_csv_file)
        for row in csv_reader:
            json_str = row[0]  # Each row contains a JSON string
            try:
                player_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for row {row} in file {player_csv_file_path}: {e}")
                continue
            player_name = player_data.get('Player', '').lower()
            is_igl = player_name in igl_names
            # Add "IGL": true/false to the player's data
            player_data['IGL'] = is_igl
            # Convert back to JSON string
            modified_json_str = json.dumps(player_data)
            modified_rows.append([modified_json_str])

    # Write modified data to the output CSV file with one column
    with open(output_csv_file_path, 'w', encoding='utf-8', newline='') as output_csv_file:
        csv_writer = csv.writer(output_csv_file)
        for row in modified_rows:
            csv_writer.writerow(row)

    print(f"Successfully added IGL info to {output_csv_file_path}")

# Example usage:
igl_json_file_path = 'vct-git\VCTHackFIles\InGamePlayers\in_game_leaders.json'  # Path to your IGL JSON file

# Process each player CSV file individually
player_csv_file_paths = [
    'vct-git\VCTHackFIles\PlayerData\CSV\players_data_challengers.csv',  # Path to your first player data CSV file
    'vct-git\VCTHackFIles\PlayerData\CSV\players_data_game_changer.csv',  # Path to your second player data CSV file
    'vct-git\VCTHackFIles\PlayerData\CSV\players_data_vct.csv'            # Path to your third player data CSV file
]

# Corresponding output CSV file paths
output_csv_file_paths = [
    'modified_players_data_challengers.csv',
    'modified_players_data_game_changer.csv',
    'modified_players_data_vct.csv'
]

# Process each file
for input_file, output_file in zip(player_csv_file_paths, output_csv_file_paths):
    add_igl_info_single_file(input_file, igl_json_file_path, output_file)
