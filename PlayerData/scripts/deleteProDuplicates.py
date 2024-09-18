import json

# Filenames
vct_filename = 'players_data_vct.json'
challengers_filename = 'players_data_challengers.json'
output_filename = 'players_data_challengers_final.json'

# Load VCT player data
with open(vct_filename, 'r', encoding='utf-8') as vct_file:
    vct_data = json.load(vct_file)

# Load Challengers player data
with open(challengers_filename, 'r', encoding='utf-8') as challengers_file:
    challengers_data = json.load(challengers_file)

# Create a set of player names from VCT data for quick lookup
vct_player_names = set()
for player in vct_data:
    player_name = player.get('Player', '').strip().lower()
    vct_player_names.add(player_name)

print(f"Total players in VCT data: {len(vct_player_names)}")

# Filter out players from Challengers data who are also in VCT data
filtered_challengers_data = []
removed_players = []

for player in challengers_data:
    player_name = player.get('Player', '').strip().lower()
    if player_name not in vct_player_names:
        filtered_challengers_data.append(player)
    else:
        removed_players.append(player_name)

print(f"Total players in Challengers data before filtering: {len(challengers_data)}")
print(f"Players removed from Challengers data: {len(removed_players)}")
print(f"Total players in Challengers data after filtering: {len(filtered_challengers_data)}")

# Save the cleaned Challengers data to a new JSON file
with open(output_filename, 'w', encoding='utf-8') as output_file:
    json.dump(filtered_challengers_data, output_file, ensure_ascii=False, indent=4)

print(f"Cleaned Challengers data saved to {output_filename}")
