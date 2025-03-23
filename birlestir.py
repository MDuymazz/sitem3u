import requests
import re

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def extract_tvg_name(line):
    match = re.search(r'tvg-name="(.*?)"', line)
    return match.group(1)[:14] if match else ""

def sort_m3u(lines):
    entries = []
    buffer = []
    for line in lines:
        if line.startswith("#EXTINF"):
            if buffer:
                entries.append((extract_tvg_name(buffer[0]), buffer))
            buffer = [line]
        else:
            buffer.append(line)
    if buffer:
        entries.append((extract_tvg_name(buffer[0]), buffer))
    
    entries.sort(key=lambda x: ("" if x[0].startswith("CANLI") else x[0]))
    
    sorted_lines = []
    for _, entry in entries:
        sorted_lines.extend(entry)
    return sorted_lines

def merge_m3u(url1, url2, output_file="playlist.m3u"):
    gol_m3u = download_m3u(url1)
    vavoo_m3u = download_m3u(url2)
    
    merged_content = ["#EXTM3U"]
    merged_content.extend(sort_m3u(gol_m3u))
    merged_content.extend(vavoo_m3u)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))

merge_m3u(
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/gol.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/vavoo.m3u"
)
