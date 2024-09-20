import csv
import json
import os

def add_role_to_csv(csv_filename, role_value):
    # Read the CSV file
    with open(csv_filename, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Process each row
    updated_rows = []
    for row in rows:
        content_json = row['Content']
        # Parse the JSON content
        data = json.loads(content_json)
        # Add the new element based on the file
        data['Role'] = role_value
        # Serialize back to JSON string
        row['Content'] = json.dumps(data, ensure_ascii=False)
        updated_rows.append(row)

    # Write back to the CSV file
    with open(csv_filename, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow({'Content': row['Content']})

if __name__ == "__main__":
    # Define the roles for each file
    file_roles = {
        'players_data_challengers.csv': 'Challengers',
        'players_data_game_changer.csv': 'Game Changers',
        'players_data_vct.csv': 'VCT International'
    }

    for csv_file, role in file_roles.items():
        # Check if the CSV file exists
        if os.path.isfile(csv_file):
            add_role_to_csv(csv_file, role)
            print(f"Updated {csv_file} with role '{role}'.")
        else:
            print(f"File {csv_file} not found.")
