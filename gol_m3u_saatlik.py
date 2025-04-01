import re

# Yeni güncellenen linki al
with open('m3u_link_alındı2.txt', 'r', encoding='utf-8') as file:
    new_url = file.read().strip()

# Gol.m3u dosyasını aç ve oku
with open('gol.m3u', 'r', encoding='utf-8') as file:
    m3u_data = file.read()

# Yeni URL'yi almak için dinamik bir yaklaşım kullanarak güncelleme fonksiyonu
def update_m3u_links(m3u_data, new_url):
    # URL'nin genel yapısını tanımlamak için dinamik bir regex
    pattern = r"(https://a\.strmrdr-cf-worker-[\w-]+\.workers\.dev)/([\w-]+)/([\w-]+)/(\d+)/a\.strmrdr-cf-worker-[\w-]+\.workers\.dev/chunklist_hd\.m3u8"
    
    # Yeni URL'den dinamik kısımları ayıklıyoruz
    match = re.search(pattern, new_url)
    if match:
        base_url = match.group(1)  # "https://a.strmrdr-cf-worker-..."
        dynamic_part1 = match.group(2)  # İlk dinamik kısmı
        dynamic_part2 = match.group(3)  # İkinci dinamik kısmı
        static_part = match.group(4)  # Sabit olan sayı (örneğin 5067)

        # Eski URL'yi güncellemek için re.sub kullanıyoruz
        updated_m3u = re.sub(r"(https://a\.strmrdr-cf-worker-[\w-]+\.workers\.dev)/([\w-]+)/([\w-]+)/(\d+)/a\.strmrdr-cf-worker-[\w-]+\.workers\.dev/chunklist_hd\.m3u8", 
                             lambda x: f"{base_url}/{dynamic_part1}/{dynamic_part2}/{static_part}/a.strmrdr-cf-worker-{dynamic_part1}.workers.dev/chunklist_hd.m3u8", 
                             m3u_data)
    return updated_m3u

# Güncellenmiş m3u verisini al
updated_m3u = update_m3u_links(m3u_data, new_url)

# Güncellenmiş veriyi bir dosyaya yaz
with open('updated_gol.m3u', 'w') as file:
    file.write(updated_m3u)

print("M3u dosyası güncellendi.")
