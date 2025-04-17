import requests
import re

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def parse_m3u(m3u_lines, force_group_title=None, exclude_group_title="Diğerleri"):
    """
    M3U dosyasını parçalar ve group-title değerine göre liste oluşturur.
    Eğer force_group_title değeri verilirse, tüm girişlerin group-title'ı buna ayarlanır.
    exclude_group_title eşleşirse, o grup atlanır.
    """
    parsed_entries = []
    entry = []
    group_title = ""
    
    for line in m3u_lines:
        if line.startswith("#EXTINF"):
            if force_group_title:
                line = re.sub(r'group-title="[^"]+"', f'group-title="{force_group_title}"', line)
                if 'group-title' not in line:
                    line = line.replace("#EXTINF", f'#EXTINF group-title="{force_group_title}"', 1)
            match = re.search(r'group-title="([^"]+)"', line)
            group_title = match.group(1) if match else "ZZZ"
            if group_title == exclude_group_title:
                entry = []  # Bu giriş atlanacak
                continue
            entry = [line]  # Yeni giriş başlıyor
        elif line.startswith("#EXTVLCOPT") or line.startswith("http"):
            if entry:
                entry.append(line)
                if line.startswith("http"):
                    parsed_entries.append((group_title, entry))
                    entry.append("")  # Girişler arasına boşluk ekle
                    entry = []  # Bir giriş tamamlandı
    
    return parsed_entries

def merge_m3u(url1, url2, url3, url4, url5, output_file="playlist.m3u"):
    new_m3u = download_m3u(url3)  # En üste eklenecek dosya
    gol_m3u = download_m3u(url1)  # İkinci sırada olacak
    programlar_m3u = download_m3u(url4)  # Üçüncü sırada olacak
    vavoo_m3u = download_m3u(url2)  # En altta olacak
    neon_m3u = download_m3u(url5)  # Bu dosyanın tüm kanalları "SPOR YAYINLARI 2" olacak
    
    merged_content = ["#EXTM3U"]
    
    all_entries = []
    for m3u_list, force_group in [
        (new_m3u, None),
        (gol_m3u, None),
        (programlar_m3u, None),
        (vavoo_m3u, None),
        (neon_m3u, "SPOR YAYINLARI 2 (MAC SAATİ)")  # NeonSpor.m3u8 içeriği bu grup başlığına atanacak
    ]:
        if m3u_list and m3u_list[0] == "#EXTM3U\n\n":
            m3u_list.pop(0)  # İlk satırı sil
        all_entries.extend(parse_m3u(m3u_list, force_group))
    
    # Öncelikli sıralama düzeni
    group_priority = {
        "GÜNLÜK SPOR AKIŞI": 1,
        "GÜNLÜK SPOR AKIŞI 2": 2,
        "SPOR YAYINLARI": 3,
        "SPOR YAYINLARI (MAC SAATİ)": 4,
        "SPOR YAYINLARI 2 (MAC SAATİ)": 5,  # Yeni eklenen kategori
        "HAFTANIN FUTBOL FİKSTÜRÜ": 6,
        "HAFTANIN BASKETBOL FİKSTÜRÜ": 7,
    }
    
    all_entries.sort(key=lambda x: group_priority.get(x[0], 99))
    
    for _, entry in all_entries:
        merged_content.extend(entry)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))

merge_m3u(
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/gol.m3u",
    "https://raw.githubusercontent.com/MDuymazz/veriler/refs/heads/main/vavoo.m3u",
    "https://raw.githubusercontent.com/MDuymazz/veriler/refs/heads/main/new_m3u.m3u",
    "https://raw.githubusercontent.com/MDuymazz/veriler/refs/heads/main/programlar.m3u",
    "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/refs/heads/master/NeonSpor/NeonSpor.m3u8"
)
