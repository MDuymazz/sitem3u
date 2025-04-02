import requests
import re

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def parse_m3u(m3u_lines):
    """
    M3U dosyasını parçalar ve group-title değerine göre liste oluşturur.
    """
    parsed_entries = []
    entry = []
    group_title = ""
    
    for line in m3u_lines:
        if line.startswith("#EXTINF"):
            entry = [line]  # Yeni giriş başlıyor
            match = re.search(r'group-title="([^"]+)"', line)
            if match:
                group_title = match.group(1)
            else:
                group_title = "ZZZ"  # Varsayılan olarak en sona eklemek için
        elif line.startswith("#EXTVLCOPT") or line.startswith("http"):
            entry.append(line)
            if line.startswith("http"):
                parsed_entries.append((group_title, entry))
                entry.append("")  # Girişler arasına boşluk ekle
                entry = []  # Bir giriş tamamlandı
    
    return parsed_entries

def merge_m3u(url1, url2, url3, url4, output_file="playlist.m3u"):
    new_m3u = download_m3u(url3)  # En üste eklenecek dosya
    gol_m3u = download_m3u(url1)  # İkinci sırada olacak
    programlar_m3u = download_m3u(url4)  # Üçüncü sırada olacak
    vavoo_m3u = download_m3u(url2)  # En altta olacak
    
    merged_content = ["#EXTM3U"]
    
    all_entries = []
    for m3u_list in [new_m3u, gol_m3u, programlar_m3u, vavoo_m3u]:
        if m3u_list and m3u_list[0] == "#EXTM3U\n\n":
            m3u_list.pop(0)  # İlk satırı sil
        all_entries.extend(parse_m3u(m3u_list))
    
    # Öncelikli sıralama düzeni
    group_priority = {
        "GÜNLÜK SPOR AKIŞI": 1,
        "GÜNLÜK SPOR AKIŞI 2": 2,
        "SPOR YAYINLARI": 3
    }
    
    all_entries.sort(key=lambda x: group_priority.get(x[0], 99))
    
    for _, entry in all_entries:
        merged_content.extend(entry)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))

merge_m3u(
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/gol.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/vavoo.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/new_m3u.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/programlar.m3u"
)
