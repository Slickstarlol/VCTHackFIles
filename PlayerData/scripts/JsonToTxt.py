import json

# List of input JSON files and their corresponding output filenames
file_info = [
    {
        'input_json': 'players_data_vct.json',
        'output_text': 'players_data_vct_content.txt',
    },
    {
        'input_json': 'players_data_game_changer.json',
        'output_text': 'players_data_game_changer_content.txt',
    },
    {
        'input_json': 'players_data_challengers.json',
        'output_text': 'players_data_challengers_content.txt',
    }
]

def create_content_text_file(input_json_file, output_text_file):
    print(f"Processing file: {input_json_file}")

    # Read the JSON data
    with open(input_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Open the output text file
    with open(output_text_file, 'w', encoding='utf-8') as textfile:
        # Iterate over each player
        for player in data:
            player_name = player.get('Player', '')
            team_name = player.get('Team', '')
            agents_played = player.get('Agents Played', [])
            stats = player.get('Stats', [{}])[0]  # Get the combined stats dictionary

            # Convert agents played list to a comma-separated string
            agents_played_str = ', '.join(agents_played)

            # Construct the content field as a textual summary of the player's stats
            content_parts = [f"Player {player_name} from team {team_name} has the following stats:"]
            for stat_key, stat_value in stats.items():
                content_parts.append(f"{stat_key}: {stat_value}")
            content = ' '.join(content_parts)

            # Write the content to the text file
            textfile.write(content + '\n\n')  # Add a newline between players

    print(f"Text file '{output_text_file}' has been created.")

def main():
    for file in file_info:
        create_content_text_file(
            input_json_file=file['input_json'],
            output_text_file=file['output_text'],
        )

if __name__ == "__main__":
    main()
