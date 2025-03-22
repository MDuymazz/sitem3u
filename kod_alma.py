import requests
from bs4 import BeautifulSoup

# Read the URL from ana_link.txt
with open('ana_link.txt', 'r', encoding='utf-8') as file:
    url = file.readline().strip()  # Assuming the URL is on the first line

# Send request to the website
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Open the file once in write mode to ensure it doesn't overwrite the previous data
with open('tüm_link.txt', 'w', encoding='utf-8') as file:

    # Find all elements with 'data-stream' attribute inside <div class="container-grid player-grid">
    player_grid_elements = soup.find('div', class_='container-grid player-grid')
    if player_grid_elements:
        data_stream_elements = player_grid_elements.find_all(attrs={'data-stream': True})
        # Write the last 4 characters of 'data-stream' values to the file
        for element in data_stream_elements:
            file.write(element['data-stream'][-4:] + '\n')  # Write last 4 characters

    # Find all elements with 'data-stream' attribute inside <div class="channel-area">
    channel_area_elements = soup.find('div', class_='channel-area')
    if channel_area_elements:
        data_stream_elements = channel_area_elements.find_all(attrs={'data-stream': True})
        # Write the last 4 characters of 'data-stream' values to the file
        for element in data_stream_elements:
            file.write(element['data-stream'][-4:] + '\n')  # Write last 4 characters
