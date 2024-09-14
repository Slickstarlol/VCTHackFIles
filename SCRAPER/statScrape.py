import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URLs for each category
urls = {
    "vct": [
        "https://www.vlr.gg/stats/?event_group_id=61&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=45&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=14&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=3&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all"
    ],
    "game_changer": [
        "https://www.vlr.gg/stats/?event_group_id=8&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=17&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=38&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=62&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all"
    ],
    "challengers": [
        "https://www.vlr.gg/stats/?event_group_id=31&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all",
        "https://www.vlr.gg/stats/?event_group_id=59&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all"
    ]
}

def scrape_links_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send a GET request to the webpage
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the stats table based on its class
        table = soup.find('table', class_='wf-table mod-stats mod-scroll')
        
        if table:
            # Initialize a set to store unique links
            links = set()
            
            # Find all rows within the table (inside <tr> tags)
            rows = table.find_all('tr')
            
            # Loop through the rows and extract data
            for row in rows:
                time.sleep(0.1)  # Add a delay to avoid overwhelming the server
                cells = row.find_all('td')
                
                # Only process rows that have data
                if len(cells) > 0:
                    # Attempt to find the <a> tag in the first cell
                    link_tag = cells[0].find('a')
                    
                    if link_tag and 'href' in link_tag.attrs:
                        relativeLink = link_tag['href']
                        links.add(relativeLink)
            
            return links
        else:
            print(f"Table not found on the page: {url}")
            return set()
    else:
        print(f"Failed to retrieve page: {url}. Status code: {response.status_code}")
        return set()

def main():
    for category, urls_list in urls.items():
        all_links = set()
        
        # Scrape each URL and collect links for the current category
        for url in urls_list:
            links = scrape_links_from_url(url)
            all_links.update(links)
        
        # Convert the set of links to a DataFrame
        df = pd.DataFrame(list(all_links), columns=["Link"])
        
        # Save the DataFrame to a CSV file
        filename = f'vlr_{category}_links.csv'
        df.to_csv(filename, index=False)
        print(f"Data for {category} saved to {filename}")

# Run the main function
main()
