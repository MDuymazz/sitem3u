import requests
import re
from datetime import datetime

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def extract_start_time_from_m3u(line):
    """M3U satırındaki saat aralığından başlangıç saatini çıkarır."""
    match = re.search(r"(\d{2}:\d{2}) - \d{2}:\d{2}", line)
    if match:
        return datetime.strptime(match.group(1), "%H:%M")
    return None

def sort_m3u_by_time(m3u_list):
    """M3U dosyasını başlangıç saatine göre sıralar."""
    m3u_with_times = []
    current_entry = []
    
    for line in m3u_list:
        if line.startswith("#EXTINF:"):
            start_time = extract_start_time_from_m3u(line)
            # Saat bilgisi mevcutsa, grubu ekliyoruz
            if start_time:
                if current_entry:
                    m3u_with_times.append((current_entry, start_time))
                current_entry = [line]
            else:
                current_entry.append(line)
        else:
            current_entry.append(line)

    # Sonuncu grubu da ekliyoruz
    if current_entry:
        m3u_with_times.append((current_entry, extract_start_time_from_m3u(current_entry[0])))

    # Saat bilgisine göre sıralama yapıyoruz
    m3u_with_times.sort(key=lambda x: x[1] if x[1] is not None else datetime.max)
    
    # Sıralanmış içerikleri birleştiriyoruz
    sorted_m3u = []
    for entry, _ in m3u_with_times:
        sorted_m3u.extend(entry)
    
    return sorted_m3u

def merge_m3u(url1, url2, url3, url4, url5, output_file="playlist.m3u"):
    new_m3u = download_m3u(url3)  # En üste eklenecek dosya
    gol_m3u = download_m3u(url1)  # İkinci sırada olacak
    diziler_m3u = download_m3u(url4)
    belgesel_m3u = download_m3u(url5)  # Üçüncü sırada olacak
    vavoo_m3u = download_m3u(url2)  # En altta olacak
    
    # Eğer indirdiğimiz dosyaların ilk satırı #EXTM3U ise, onu kaldırıyoruz.
    for m3u_list in [new_m3u, gol_m3u, diziler_m3u, vavoo_m3u, belgesel_m3u]:
        if m3u_list and m3u_list[0] == "#EXTM3U":
            m3u_list.pop(0)  # İlk satırı sil
    
    # Belgesel ve diziler dosyalarını saat bilgilerine göre sıralıyoruz
    sorted_belgesel_m3u = sort_m3u_by_time(belgesel_m3u)
    sorted_diziler_m3u = sort_m3u_by_time(diziler_m3u)
    
    # Şimdi, her iki listeyi birleştirip sıralıyoruz
    combined_m3u = []
    i, j = 0, 0
    
    while i < len(sorted_belgesel_m3u) and j < len(sorted_diziler_m3u):
        belgesel_time = extract_start_time_from_m3u(sorted_belgesel_m3u[i])
        diziler_time = extract_start_time_from_m3u(sorted_diziler_m3u[j])
        
        if belgesel_time <= diziler_time:
            combined_m3u.append(sorted_belgesel_m3u[i])
            i += 1
        else:
            combined_m3u.append(sorted_diziler_m3u[j])
            j += 1
    
    # Kalan elemanları ekliyoruz
    while i < len(sorted_belgesel_m3u):
        combined_m3u.append(sorted_belgesel_m3u[i])
        i += 1
    while j < len(sorted_diziler_m3u):
        combined_m3u.append(sorted_diziler_m3u[j])
        j += 1
    
    # Diğer dosyaları da sırayla ekliyoruz
    merged_content = ["#EXTM3U"]
    merged_content.extend(new_m3u)   # new_m3u en üstte
    merged_content.extend(gol_m3u)   # gol_m3u ikinci sırada
    merged_content.extend(combined_m3u)  # diziler ve belgesel sıralı
    merged_content.extend(vavoo_m3u)  # vavoo_m3u en altta

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
