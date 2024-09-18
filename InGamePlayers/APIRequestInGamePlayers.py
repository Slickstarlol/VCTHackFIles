import requests
from bs4 import BeautifulSoup
import json

# List of URLs to scrape
category_urls = [
    'https://liquipedia.net/valorant/Category:In-game_leaders',
    'https://liquipedia.net/valorant/index.php?title=Category:In-game_leaders&pagefrom=Tayhuhu#mw-pages'
]

# Function to fetch player details from their individual pages
def fetch_player_details(player_page_url):
    try:
        response = requests.get(player_page_url)
        response.raise_for_status()  # Check for HTTP request errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize default values
        team_name = 'Unknown'
        status = 'Unknown'
        
        # Check for player status
        infobox_divs = soup.find_all('div', class_='infobox-description')
        for infobox in infobox_divs:
            if infobox.get_text(strip=True) == 'Status:':
                status = infobox.find_next_sibling().get_text(strip=True)
                if status == 'Retired':
                    return None, status
        
        # Extract team name from the new location
        team_span = soup.find('span', class_='team-template-image-icon team-template-darkmode')
        if team_span:
            a_tag = team_span.find('a')
            if a_tag and 'title' in a_tag.attrs:
                team_name = a_tag['title']
        
        return team_name, status
    except Exception as e:
        print(f'Error fetching player details from {player_page_url}: {e}')
        return 'Unknown', 'Unknown'

# Function to scrape player links from a category page
def scrape_player_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all player links
        player_links = soup.select('div.mw-category-group ul li a')
        
        return player_links
    except requests.RequestException as e:
        print(f'Error fetching category page: {url} - {e}')
        return []

# List to store player data
players_data = []

# Process each URL
for category_url in category_urls:
    player_links = scrape_player_links(category_url)
    
    for link in player_links:
        player_name = link.get_text(strip=True)
        player_url = link.get('href')
        player_page_url = f'https://liquipedia.net{player_url}'
        
        try:
            # Fetch team information from player's page
            team_name, status = fetch_player_details(player_page_url)
            
            # Skip players with status 'Retired'
            if status == 'Retired':
                print(f'Skipped retired player: {player_name}')
                continue
            
            # Append data to list
            players_data.append({
                'In-Game Name': player_name,
                'Team': team_name
            })
            
            # Print added data with error handling for encoding issues
            try:
                print(f'Added data for player: {player_name}, Team: {team_name}')
            except UnicodeEncodeError as e:
                print(f'UnicodeEncodeError encountered: {e}. Data for player: {player_name}, Team: {team_name}')
        except requests.RequestException as e:
            print(f'Error fetching player details for {player_name}: {e}')

# Write to JSON file
try:
    with open('in_game_leaders.json', 'w', encoding='utf-8') as file:
        json.dump(players_data, file, ensure_ascii=False, indent=4)
    print("Data saved to in_game_leaders.json")
except IOError as e:
    print(f'Error writing JSON file: {e}')
