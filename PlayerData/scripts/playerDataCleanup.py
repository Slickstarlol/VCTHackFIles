import json

# List of JSON filenames
json_files = [
    'players_data_vct.json',
    'players_data_game_changer.json',
    'players_data_challengers.json'
]

for filename in json_files:
    print(f"Processing file: {filename}")
    # Read the JSON file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process each player
    for player in data:
        # 'Stats' is a list of dictionaries
        stats_list = player.get('Stats', [])
        for stat in stats_list:
            # Remove 'agents' key if present
            if 'Agents' in stat:
                del stat['Agents']
    
    # Save the cleaned data to a new file
    output_filename = filename.replace('.json', '_cleaned.json')
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved cleaned data to: {output_filename}")
