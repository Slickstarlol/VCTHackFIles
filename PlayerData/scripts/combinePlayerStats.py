import json

# List of JSON files to process
json_files = [
    'players_data_vct.json',
    'players_data_game_changer.json',
    'players_data_challengers.json'  # Assuming this is the cleaned Challengers file
]

def combine_player_stats(player):
    """
    Combines multiple stats entries for a player into one.
    - Sums up the 'Rnd' (rounds) values.
    - Computes weighted averages for other stats using 'Rnd' as weights.
    - Stores 'Rnd' as an integer in the final output.
    """
    combined_stats = {}
    total_rounds = 0

    # List of stats entries
    stats_list = player.get('Stats', [])
    if not stats_list:
        return player  # No stats to combine

    # Initialize sums for each stat
    stats_sums = {}
    for stat_entry in stats_list:
        # Extract rounds played as an integer
        rounds_str = stat_entry.get('Rnd', '0').replace(',', '')
        try:
            rounds = int(rounds_str)
        except ValueError:
            rounds = 0  # If rounds cannot be converted to int, set to 0

        total_rounds += rounds  # Sum up the rounds

        # Iterate over all stats
        for key, value in stat_entry.items():
            if key == 'Rnd':
                continue  # We'll add total 'Rnd' later

            # Convert value to float if possible
            value = value.replace('%', '').replace(',', '').strip()
            try:
                value = float(value)
            except ValueError:
                continue  # Skip non-numeric values

            # Weighted sum for each stat
            if key in stats_sums:
                stats_sums[key] += value * rounds
            else:
                stats_sums[key] = value * rounds

    if total_rounds == 0:
        return player  # Avoid division by zero

    # Compute weighted averages
    combined_stats = {}
    for key, weighted_sum in stats_sums.items():
        combined_stats[key] = round(weighted_sum / total_rounds, 2)  # Round to 2 decimal places

    # Add total rounds to the combined stats as an integer
    combined_stats['Rnd'] = total_rounds

    # Replace the player's stats with the combined stats
    player['Stats'] = [combined_stats]
    return player

def process_json_file(filename):
    print(f"Processing file: {filename}")
    # Read the JSON file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process each player
    for idx, player in enumerate(data):
        player = combine_player_stats(player)
        data[idx] = player  # Update the player data

    # Save the updated data to a new file
    output_filename = filename.replace('.json', '_final.json')
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Final combined data saved to: {output_filename}")

# Process each JSON file
for json_file in json_files:
    process_json_file(json_file)