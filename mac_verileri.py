from bs4 import BeautifulSoup
import requests

# Read the URL from ana_link.txt
with open("ana_link.txt", "r", encoding="utf-8") as file:
    url = file.read().strip()  # Strip to remove any extra spaces or newline characters

# Send a GET request to fetch the HTML content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the div with the class "list-area"
list_area_div = soup.find("div", class_="list-area")
# Find the div with the class "channel-area"
channel_area_div = soup.find("div", class_="channel-area")

# Open mac_verileri.txt to write the extracted data
with open("mac_verileri.txt", "w", encoding="utf-8") as output_file:
    if list_area_div:
        # Find all elements with the required attributes (data-matchtype) and get the text
        matches = list_area_div.find_all(attrs={"data-matchtype": True})

        for match in matches:
            # Extract the required data attributes
            matchtype = match.get("data-matchtype")
            txt = match.get_text(" ", strip=True).replace(",", "")  # Remove commas
            
            # Replace "-" with "vs"
            txt = txt.replace("-", "vs")

            # Write match data
            output_file.write(f'MatchType: "{matchtype}"\n')
            output_file.write(f'Text: "{txt}"\n')
            output_file.write("\n")  # Add a space between matches
    
    if channel_area_div:
        # Find all elements with data-name attribute inside channel-area
        channels = channel_area_div.find_all(attrs={"data-name": True})

        for channel in channels:
            data_name = channel.get("data-name")
            output_file.write(f'MatchType: "CANLI"\n')
            output_file.write(f'Text: "{data_name}"\n')
            output_file.write("\n")  # Add a space between channels

print("Data has been extracted and saved to mac_verileri.txt")
