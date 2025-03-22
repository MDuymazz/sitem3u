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

    # First part: Process <a> elements with 'data-matchtype' and 'data-name'
    match_elements = soup.find_all('a', attrs={'data-matchtype': True, 'data-name': True})
    
    for element in match_elements:
        matchtype = element['data-matchtype']  # Get the match type
        text = element.get_text(separator=' ').strip()  # Get the text, replacing <br> with a space

        # Replace hyphen with en dash and remove the comma
        text = text.replace('-', '–')  # Replace hyphen with en dash
        text = text.replace(',', '')  # Remove the comma

        # Make the text uppercase
        text = text.upper()

        # Write the formatted data to the file
        file.write(f'MatchType: "{matchtype}"\n')
        file.write(f'Text: "{text}"\n')
        file.write('\n')  # Separate entries with a blank line

    # Second part: Process <div class="channel-area"> elements

    # Process <div class="channel-area"> for 'data-matchtype' and 'data-name'
    channel_area_elements = soup.find_all('div', class_='channel-area')
    for area in channel_area_elements:
        data_matchtype_elements = area.find_all(attrs={'data-matchtype': True})
        data_name_elements = area.find_all(attrs={'data-name': True})

        # Write the data in the requested format
        for matchtype, name in zip(data_matchtype_elements, data_name_elements):
            file.write(f'MatchType: "{matchtype["data-matchtype"]}"\n')
            file.write(f'Text: "{name["data-name"]}"\n')
            file.write('\n')  # Separate entries with a blank line

    # Process <div class="channel-area"> again and write only 'data-name' with "CANLI" as MatchType
    for area in channel_area_elements:
        data_name_elements = area.find_all(attrs={'data-name': True})
        for name in data_name_elements:
            file.write(f'MatchType: "CANLI"\n')
            file.write(f'Text: "{name["data-name"].upper()}"\n')
            file.write('\n')  # Separate entries with a blank line
