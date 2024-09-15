import sys
import requests
from bs4 import BeautifulSoup
import json
import time

# Ensure that stdout is using UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Function to scrape team URLs from a single regional ranking page
def scrape_team_urls(region_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send a GET request to the regional ranking page
    response = requests.get(region_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all team items based on the class
        team_divs = soup.find_all('a', class_='rank-item-team fc-flex')
        
        if not team_divs:
            print(f"No teams found on page: {region_url}")
        
        for div in team_divs:
            # Extract the href attribute from the <a> tag
            team_url = div['href']
            yield team_url
    else:
        print(f"Failed to retrieve page: {region_url}. Status code: {response.status_code}")

# Function to scrape details from a team's page
def scrape_team_details(team_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    full_url = f"https://www.vlr.gg{team_url}"
    response = requests.get(full_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract team name
        team_name_div = soup.find('h1', class_='wf-title')  # Adjust the class if needed
        team_name = team_name_div.text.strip() if team_name_div else "Unknown"
        
        # Extract team abbreviation
        team_abbreviation_span = soup.find('h2', class_='wf-title team-header-tag')
        team_abbreviation = team_abbreviation_span.text.strip() if team_abbreviation_span else team_name
        
        # Extract team country
        country_div = soup.find('div', class_='team-header-country')
        if country_div:
            country = country_div.get_text(strip=True).replace('\n', ' ').split(' ', 1)[-1]
        else:
            country = "Unknown"
        
        return team_name, team_abbreviation, country
    else:
        print(f"Failed to retrieve team page: {full_url}. Status code: {response.status_code}")
        return "Unknown", "Unknown", "Unknown"

# Define URLs for each regional ranking page and their respective file names
region_urls = {
    "Latin America North": "https://www.vlr.gg/rankings/la-n",
    "China": "https://www.vlr.gg/rankings/china",
    "North America": "https://www.vlr.gg/rankings/north-america",
    "Europe": "https://www.vlr.gg/rankings/europe",
    "Brazil": "https://www.vlr.gg/rankings/brazil",
    "Asia-Pacific": "https://www.vlr.gg/rankings/asia-pacific",
    "Korea": "https://www.vlr.gg/rankings/korea",
    "Japan": "https://www.vlr.gg/rankings/japan",
    "Latin America South": "https://www.vlr.gg/rankings/la-s",
    "Oceania": "https://www.vlr.gg/rankings/oceania",
    "Middle East North Africa": "https://www.vlr.gg/rankings/mena",
    "Group Challengers": "https://www.vlr.gg/rankings/gc"
}

# Collect all teams' details for each region
for region, url in region_urls.items():
    output_file = f'team_data_{region.replace(" ", "_").lower()}.json'
    
    all_teams = []
    print(f"Processing region: {region} from URL: {url}")
    
    for team_url in scrape_team_urls(url):
        try:
            name, abbreviation, country = scrape_team_details(team_url)
            
            # Skip teams where the country is 'International'
            if country == "International":
                print(f'Skipped team: {name}, Abbreviation: {abbreviation}, Country: {country}')
                continue
            
            # Append to list
            all_teams.append({
                'Team Name': name,
                'Abbreviation': abbreviation,
                'Country': country
            })
            
            print(f'Added data for team: {name}, Abbreviation: {abbreviation}, Country: {country}')
            
            
        except requests.RequestException as e:
            print(f'Error fetching team details for URL {team_url}: {e}')
    
    # Write to JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(all_teams, file, ensure_ascii=False, indent=4)
        print(f"Data for {region} saved to {output_file}")
    except IOError as e:
        print(f'Error writing JSON file for {region}: {e}')
