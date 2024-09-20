import json
import csv
import os

def process_file(json_filename):
    # Determine the CSV filename
    csv_filename = os.path.splitext(json_filename)[0] + '.csv'
    metadata_filename = csv_filename + '.metadata.json'

    # Read the JSON data
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Define the single content field
    fieldnames = ['Content']

    # Write CSV file with one content field
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for item in data:
            # Serialize the entire item as a JSON string
            content = json.dumps(item, ensure_ascii=False)
            writer.writerow({'Content': content})

    # Create metadata JSON file with only one content field
    metadata = {
        "metadataAttributes": {
            "source": "Converted from JSON",
            "author": "Your Name or Organization"
        },
        "documentStructureConfiguration": {
            "type": "RECORD_BASED_STRUCTURE_METADATA",
            "recordBasedStructureMetadata": {
                "contentFields": [
                    {
                        "fieldName": "Content"
                    }
                ],
                "metadataFieldsSpecification": {
                    "fieldsToInclude": [],
                    "fieldsToExclude": []
                }
            }
        }
    }

    # Write metadata JSON file
    with open(metadata_filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    json_files = [
        'players_data_challengers.json',
        'players_data_game_changer.json',
        'players_data_vct.json'
    ]

    for json_file in json_files:
        process_file(json_file)
