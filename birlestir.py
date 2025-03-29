import requests
import re
from datetime import datetime

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def extract_time_from_extinf(line):
    # #EXTINF satırındaki zaman dilimini almak için regex
    match = re.search(r'(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})', line)
    if match:
        start_time = match.group(1)
        return datetime.strptime(start_time, "%H:%M")  # Saat bilgisini datetime formatında döndür
    return None

def sort_m3u_blocks(m3u_list):
    # #EXTINF satırları ve ilgili video/stream URL'leri birlikte sıralanacak
    blocks = []
    current_block = []
    
    for line in m3u_list:
        if line.startswith("#EXTINF"):
            if current_block:
                blocks.append(current_block)  # Önceki blok ekleniyor
            current_block = [line]  # Yeni bir blok başlıyor
        else:
            current_block.append(line)  # Satır, mevcut bloğa ekleniyor

    if current_block:
        blocks.append(current_block)  # Son bloğu da ekleyelim

    # Blokları sıralama: her bloktaki #EXTINF satırının zaman dilimine göre sıralama
    sorted_blocks = []
    for block in blocks:
        extinf_line = block[0]
        time = extract_time_from_extinf(extinf_line)
        if time:
            sorted_blocks.append((time, block))
    
    sorted_blocks.sort(key=lambda x: x[0])  # Saat bilgisine göre sıralama

    # Sıralanmış blokları geri al
    sorted_m3u = []
    for _, block in sorted_blocks:
        sorted_m3u.extend(block)

    return sorted_m3u

def merge_m3u(url1, url2, url3, url4, url5, output_file="playlist.m3u"):
    new_m3u = download_m3u(url3)  # En üste eklenecek dosya
    gol_m3u = download_m3u(url1)  # İkinci sırada olacak
    diziler_m3u = download_m3u(url4)
    belgesel_m3u = download_m3u(url5)  # Üçüncü sırada olacak
    vavoo_m3u = download_m3u(url2)  # En altta olacak
    
    merged_content = ["#EXTM3U"]

    # Eğer indirdiğimiz dosyaların ilk satırı #EXTM3U ise, onu kaldırıyoruz.
    for m3u_list in [new_m3u, gol_m3u, diziler_m3u, vavoo_m3u, belgesel_m3u]:
        if m3u_list and m3u_list[0] == "#EXTM3U":
            m3u_list.pop(0)  # İlk satırı sil

    # Dosyaları bloklar halinde sıralayıp birleştir
    gol_m3u = sort_m3u_blocks(gol_m3u)
    diziler_m3u = sort_m3u_blocks(diziler_m3u)
    belgesel_m3u = sort_m3u_blocks(belgesel_m3u)
    vavoo_m3u = sort_m3u_blocks(vavoo_m3u)

    # Dosyaları sırayla ekle
    merged_content.extend(new_m3u)   # new_m3u en üstte
    merged_content.extend(gol_m3u)   # gol_m3u ikinci sırada
    merged_content.extend(diziler_m3u)  # diziler_m3u üçüncü sırada
    merged_content.extend(belgesel_m3u)  # belgesel.m3u dördüncü sırada
    merged_content.extend(vavoo_m3u)  # vavoo.m3u en altta

    # Dosyaya yaz
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))

merge_m3u(
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/gol.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/vavoo.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/new_m3u.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/diziler.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/belgesel.m3u"
)
