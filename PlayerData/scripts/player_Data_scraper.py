import requests
from bs4 import BeautifulSoup
import time
import json
import sys

# Configure standard output to handle UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# URLs for each category
urls = {
    "vct": [
        "https://www.vlr.gg/stats/?event_group_id=61&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=45&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=14&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=3&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all"
    ],
    "game_changer": [
        "https://www.vlr.gg/stats/?event_group_id=8&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=17&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=38&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=62&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all"
    ],
    "challengers": [
        "https://www.vlr.gg/stats/?event_group_id=31&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=59&event_id=all&region=all&min_rounds=200"
        "&min_rating=1550&agent=all&map_id=all&timespan=all"
    ]
}

def scrape_player_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    print(f"Sending request to {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"Error requesting URL {url}: {e}")
        return []

    if response.status_code == 200:
        print(f"Successfully retrieved page: {url}")
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the stats table
        table = soup.find('table', class_='wf-table mod-stats mod-scroll')

        if table:
            print("Table found, processing rows...")

            # Extract table headers
            headers_list = []
            header_row = table.find('tr')
            if header_row:
                header_cells = header_row.find_all('th')
                for th in header_cells:
                    header_text = th.get_text(strip=True)
                    headers_list.append(header_text)
            print(f"Original table headers: {headers_list}")

            data_list = []

            rows = table.find_all('tr')
            print(f"Found {len(rows)} rows in the table.")

            for row in rows:
                if row.find('th'):
                    continue  # Skip header row
                cells = row.find_all('td')
                if not cells:
                    continue

                cell_data = {}

                for i in range(len(cells)):
                    cell = cells[i]
                    if i == 0:
                        # Process the player cell
                        link_tag = cell.find('a')
                        if link_tag and 'href' in link_tag.attrs:
                            relative_link = link_tag['href']
                            full_url = 'https://www.vlr.gg' + relative_link + "?timespan=all"
                            print(f"Fetching player data from: {full_url}")

                            # Fetch player name, team, and agents played from player page
                            try:
                                player_response = requests.get(full_url, headers=headers, timeout=10)
                                if player_response.status_code == 200:
                                    player_soup = BeautifulSoup(player_response.content, 'html.parser')

                                    # Extract player name
                                    h1_tag = player_soup.find('h1', class_='wf-title')
                                    player_name = h1_tag.get_text(strip=True) if h1_tag else 'N/A'

                                    # Extract team name using style="font-weight: 500;"
                                    team_name_tag = player_soup.find(style="font-weight: 500;")
                                    team_name = team_name_tag.get_text(strip=True) if team_name_tag else 'N/A'

                                    # Extract agents played from the player's page
                                    agents_played = []
                                    agent_table = player_soup.find('div', class_='wf-card mod-table mod-dark')
                                    if agent_table:
                                        agent_rows = agent_table.find_all('tr')
                                        # Skip the header row
                                        agent_rows = agent_rows[1:]
                                        for agent_row in agent_rows[:3]:  # Get first 3 rows
                                            agent_cell = agent_row.find('td')
                                            if agent_cell:
                                                img_tag = agent_cell.find('img')
                                                if img_tag and 'alt' in img_tag.attrs:
                                                    agents_played.append(img_tag['alt'])
                                    else:
                                        print("Agent table not found on player page.")
                                        agents_played = []

                                    print(f"Player: {player_name}, Team: {team_name}, Agents Played: {agents_played}")
                                else:
                                    print(f"Failed to retrieve player page: {full_url}")
                                    player_name = 'N/A'
                                    team_name = 'N/A'
                                    agents_played = []
                            except Exception as e:
                                print(f"Error fetching player data from {full_url}: {e}")
                                player_name = 'N/A'
                                team_name = 'N/A'
                                agents_played = []
                        else:
                            print("No player link found, using defaults.")
                            player_name = 'N/A'
                            team_name = 'N/A'
                            agents_played = []
                        cell_data['Player'] = player_name
                        cell_data['Team'] = team_name
                        cell_data['Agents Played'] = agents_played
                    else:
                        # Map the cell data to the corresponding header
                        if i < len(headers_list):
                            header = headers_list[i]
                        else:
                            header = f'Column{i+1}'
                        text = cell.get_text(strip=True)
                        if text == '':
                            text = '0'
                        cell_data[header] = text
                data_list.append(cell_data)
                print(f"Extracted data: {cell_data}")
            return data_list
        else:
            print(f"Table not found on the page: {url}")
            return []
    else:
        print(f"Failed to retrieve page: {url}. Status code: {response.status_code}")
        return []

def main():
    for category, urls_list in urls.items():
        print(f"Processing category: {category}")
        all_players_data = {}
        for url in urls_list:
            data = scrape_player_data(url)
            for player_data in data:
                player_name = player_data.get('Player', 'Unknown')
                if player_name not in all_players_data:
                    all_players_data[player_name] = {
                        'Player': player_name,
                        'Team': player_data.get('Team', 'N/A'),
                        'Agents Played': player_data.get('Agents Played', []),
                        'Stats': []
                    }
                else:
                    # Update Agents Played if not already present
                    if not all_players_data[player_name].get('Agents Played'):
                        all_players_data[player_name]['Agents Played'] = player_data.get('Agents Played', [])
                # Remove 'Player', 'Team', and 'Agents Played' before adding to 'Stats'
                stats = {k: v for k, v in player_data.items() if k not in ['Player', 'Team', 'Agents Played']}
                all_players_data[player_name]['Stats'].append(stats)
            print(f"Processed data from {url}")

        # Convert the dictionary to a list
        players_list = list(all_players_data.values())

        # Save the data to a JSON file per category
        output_filename = f'players_data_{category}.json'
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(players_list, f, ensure_ascii=False, indent=4)
        print(f"Data for category '{category}' saved to {output_filename}")

# Run the main function
if __name__ == "__main__":
    main()
