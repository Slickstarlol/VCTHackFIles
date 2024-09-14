import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_player_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Fetching data from: {url}")  # Debug: print the URL being fetched
    
    # Send a GET request to the webpage with a timeout
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Request failed: {e}")  # Debug: print the exception
        return 'N/A', []

    print(f"Successfully retrieved page: {url}")  # Debug: confirm successful retrieval
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the player name from the h1 tag
    player_name_tag = soup.find('h1', class_='wf-title')
    player_name = player_name_tag.get_text(strip=True) if player_name_tag else 'N/A'
    print(f"Player Name: {player_name}")  # Debug: print the player name
    
    # Extract data from the table
    table = soup.find('table', class_='wf-table')
    table_data = []
    
    if table:
        # Find all rows within the table (inside <tr> tags)
        rows = table.find_all('tr')
        print(f"Found {len(rows)} rows in the table.")  # Debug: print the number of rows found
        
        for i, row in enumerate(rows[:4]):  # Limit to the first 3 rows
            cells = row.find_all('td')
            if cells:
                cell_data = []
                # Extract alt text from images in the first column
                first_column_image = cells[0].find('img')
                if first_column_image and 'alt' in first_column_image.attrs:
                    cell_data.append(first_column_image['alt'])
                else:
                    cell_data.append('N/A')  # Default if no image or alt text
                
                # Extract text from remaining cells
                cell_data.extend([cell.get_text(strip=True) for cell in cells[1:]])
                
                # Debug: Print data from each row
                print(f"Row data (length {len(cell_data)}): {cell_data}")
                
                table_data.append(cell_data)
            
            time.sleep(0.1)  # Sleep for 0.1 seconds between requests
            
    else:
        print("Table not found on the page.")  # Debug: if the table is not found
    
    return player_name, table_data

def process_csv_and_scrape_data(csv_filename):
    print(f"Processing file: {csv_filename}")  # Debug: print the CSV file being processed
    
    # Read the CSV file with relative links
    df = pd.read_csv(csv_filename)
    all_data = []
    
    # Base URL for constructing the full URL
    base_url = 'https://www.vlr.gg'
    
    for _, row in df.iterrows():
        relative_link = row['Link']
        full_url = f"{base_url}{relative_link}?timespan=all"
        print(f"Constructed URL: {full_url}")  # Debug: print the full URL being processed
        
        # Get player data from the URL
        player_name, table_data = get_player_data(full_url)
        
        # Check the column length and adjust accordingly
        for table_row in table_data:
            # Debug: Print the length of each row
            print(f"Table row length: {len(table_row)}")
            # Ensure table_row has exactly 15 columns (or whatever number matches the DataFrame structure)
            if len(table_row) < 15:
                table_row.extend(['N/A'] * (15 - len(table_row)))
        
        # Convert list of lists into DataFrame
        try:
            df_data = pd.DataFrame(table_data, columns=[
                "agent","games", "rounds", "rating", "acs", "k/d", "adr", "kast",
                "kpr", "apr", "fkpr", "fdpr", "kills", "deaths", "assist", "first bloods","first deaths"
            ])
        except ValueError as e:
            print(f"Error creating DataFrame: {e}")  # Debug: print the DataFrame creation error
            continue
        
        # Add player name to DataFrame
        df_data.insert(0, 'Player Name', player_name)
        
        # Append the results to the list
        all_data.append(df_data)
    
    # Concatenate all DataFrames into a single DataFrame
    if all_data:
        result_df = pd.concat(all_data, ignore_index=True)
        
        # Save the DataFrame to a CSV file
        result_csv_filename = csv_filename.replace('.csv', '_player_data.csv')
        result_df.to_csv(result_csv_filename, index=False)
        print(f"Data saved to {result_csv_filename}")  # Debug: print confirmation of data saved
    else:
        print(f"No data to save for {csv_filename}")

# Run the processing for each CSV file
csv_files = [
    'vlr_vct_links.csv',
    'vlr_game_changer_links.csv',
    'vlr_challengers_links.csv'
]

for csv_file in csv_files:
    process_csv_and_scrape_data(csv_file)
