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

def sort_by_time(m3u_list):
    # #EXTINF satırındaki zaman dilimlerine göre sıralama
    m3u_with_time = []
    for i, line in enumerate(m3u_list):
        if line.startswith("#EXTINF"):
            time = extract_time_from_extinf(line)
            if time:
                m3u_with_time.append((time, i, line))
    
    # Saat bilgisine göre sıralama (en küçük saat önce gelsin)
    m3u_with_time.sort(key=lambda x: x[0])
    
    # Sıralanmış öğeleri m3u_list'ten alarak yeni liste oluşturma
    sorted_m3u = []
    for time, i, line in m3u_with_time:
        sorted_m3u.append(m3u_list[i])
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

    # Diziler.m3u ve Belgesel.m3u'yu zaman dilimlerine göre sırala
    diziler_m3u = sort_by_time(diziler_m3u)
    belgesel_m3u = sort_by_time(belgesel_m3u)

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
