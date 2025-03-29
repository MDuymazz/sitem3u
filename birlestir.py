import requests

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def merge_m3u(url1, url2, url3, url4, output_file="playlist.m3u"):
    new_m3u = download_m3u(url3)  # En üste eklenecek dosya
    gol_m3u = download_m3u(url1)  # İkinci sırada olacak
    programlar_m3u = download_m3u(url4)
    vavoo_m3u = download_m3u(url2)  # En altta olacak
    
    merged_content = ["#EXTM3U"]

    # Eğer indirdiğimiz dosyaların ilk satırı #EXTM3U ise, onu kaldırıyoruz.
    for m3u_list in [new_m3u, gol_m3u, programlar_m3u, vavoo_m3u]:
        if m3u_list and m3u_list[0] == "#EXTM3U":
            m3u_list.pop(0)  # İlk satırı sil

    # Dosyaları sırayla ekle
    merged_content.extend(new_m3u)   # new_m3u en üstte
    merged_content.extend(gol_m3u)   # gol_m3u ikinci sırada
    merged_content.extend(programlar_m3u)  # diziler_m3u üçüncü sırada
    merged_content.extend(vavoo_m3u)  # vavoo_m3u en altta

    # Dosyaya yaz
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))

merge_m3u(
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/gol.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/vavoo.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/new_m3u.m3u",
    "https://raw.githubusercontent.com/MDuymazz/efendikaptan/refs/heads/main/programlar.m3u"
)
