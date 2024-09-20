import json
import csv
import os

# List of input JSON files and their corresponding output filenames
file_info = [
    {
        'input_json': 'players_data_vct.json',
        'output_csv': 'players_data_vct.csv',
        'metadata_json': 'players_data_vct.csv.metadata.json'
    },
    {
        'input_json': 'players_data_game_changer.json',
        'output_csv': 'players_data_game_changer.csv',
        'metadata_json': 'players_data_game_changer.csv.metadata.json'
    },
    {
        'input_json': 'players_data_challengers.json',
        'output_csv': 'players_data_challengers.csv',
        'metadata_json': 'players_data_challengers.csv.metadata.json'
    }
]

def create_csv_and_metadata(input_json_file, output_csv_file, metadata_json_file):
    print(f"Processing file: {input_json_file}")

    # Read the JSON data
    with open(input_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prepare CSV data
    csv_rows = []
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

        # Prepare a row dictionary
        row = {
            'Content': content,
            'Player': player_name,
            'Team': team_name,
            'Agents Played': agents_played_str
        }
        # Add stats to the row
        for stat_key, stat_value in stats.items():
            row[stat_key] = stat_value

        csv_rows.append(row)

    # Get all unique field names for the CSV header
    fieldnames = set()
    for row in csv_rows:
        fieldnames.update(row.keys())
    fieldnames = list(fieldnames)

    # Optional: Define desired field order
    desired_order = ['Content', 'Player', 'Team', 'Agents Played']
    remaining_fields = sorted(set(fieldnames) - set(desired_order))
    fieldnames = desired_order + remaining_fields

    # Write the CSV file
    with open(output_csv_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data rows
        for row in csv_rows:
            writer.writerow(row)

    print(f"CSV file '{output_csv_file}' has been created.")

    # Create the metadata JSON file
    # Specify 'Content' as the content field and other fields as metadata
    metadata_json = {
        "metadataAttributes": {},
        "documentStructureConfiguration": {
            "type": "RECORD_BASED_STRUCTURE_METADATA",
            "recordBasedStructureMetadata": {
                "contentFields": [
                    {
                        "fieldName": "Content"
                    }
                ],
                "metadataFieldsSpecification": {
                    "fieldsToInclude": [
                        {
                            "fieldName": "Player"
                        },
                        {
                            "fieldName": "Team"
                        },
                        {
                            "fieldName": "Agents Played"
                        }
                        # Add other metadata fields if needed
                    ]
                }
            }
        }
    }

    # Save the metadata JSON file
    with open(metadata_json_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_json, f, ensure_ascii=False, indent=4)

    print(f"Metadata JSON file '{metadata_json_file}' has been created.")


def main():
    for file in file_info:
        create_csv_and_metadata(
            input_json_file=file['input_json'],
            output_csv_file=file['output_csv'],
            metadata_json_file=file['metadata_json']
        )

if __name__ == "__main__":
    main()
