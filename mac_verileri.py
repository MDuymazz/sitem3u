import requests
from bs4 import BeautifulSoup

# Read the URL from ana_link.txt
with open('ana_link.txt', 'r', encoding='utf-8') as file:
    url = file.readline().strip()  # Assuming the URL is on the first line

# Send request to the website
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Open the file to write the data
with open('mac_verileri.txt', 'w', encoding='utf-8') as file:

    # Find all elements with 'data-matchtype' and 'data-name' inside <div class="container-grid player-grid">
    player_grid_elements = soup.find('div', class_='container-grid player-grid')
    if player_grid_elements:
        data_matchtype_elements = player_grid_elements.find_all(attrs={'data-matchtype': True})
        data_name_elements = player_grid_elements.find_all(attrs={'data-name': True})
        # Write the data in the requested format
        for matchtype, name in zip(data_matchtype_elements, data_name_elements):
            file.write(f'MatchType: "{matchtype["data-matchtype"]}"\n')
            file.write(f'Text: "{name["data-name"]}"\n')
            file.write('\n')  # Separate entries with a blank line

    # Find all elements with 'data-matchtype' and 'data-name' inside <div class="channel-area">
    channel_area_elements = soup.find('div', class_='channel-area')
    if channel_area_elements:
        data_matchtype_elements = channel_area_elements.find_all(attrs={'data-matchtype': True})
        data_name_elements = channel_area_elements.find_all(attrs={'data-name': True})
        # Write the data in the requested format
        for matchtype, name in zip(data_matchtype_elements, data_name_elements):
            file.write(f'MatchType: "{matchtype["data-matchtype"]}"\n')
            file.write(f'Text: "{name["data-name"]}"\n')
            file.write('\n')  # Separate entries with a blank line

    # Now find the <div class="channel-area"> again and write only 'data-name' with "CANLI" as MatchType
    channel_area_elements = soup.find_all('div', class_='channel-area')
    for area in channel_area_elements:
        data_name_elements = area.find_all(attrs={'data-name': True})
        for name in data_name_elements:
            file.write(f'MatchType: "CANLI"\n')
            file.write(f'Text: "{name["data-name"]}"\n')
            file.write('\n')  # Separate entries with a blank line
