import re

def update_m3u_links(m3u_file, updated_link_file, output_file):
    # Yeni linki dosyadan oku
    with open(updated_link_file, 'r', encoding='utf-8') as f:
        new_link = f.readline().strip()
    
    # 4 haneli numarayı içeren regex
    pattern = re.compile(r'(https://playerpro\.live/proxy\.php\?url=https://a\.strmrdr-cf-worker-[^/]+/[^/]+/[^/]+/)(\d{4})(/[^\s]+)')
    
    # M3U dosyasını oku ve güncelle
    with open(m3u_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replace_link(match):
        number = match.group(2)  # 4 haneli sayı
        old_segment = re.search(r"/\d{4}/", new_link)
        if old_segment:
            old_segment = old_segment.group(0)
            updated_link = new_link.replace(old_segment, f"/{number}/")
            return f'https://playerpro.live/proxy.php?url={updated_link}&referer=https://golvar2014.sbs/&origin=https://golvar2014.sbs/'
        return match.group(0)  # Eşleşme olmazsa değiştirme
    
    updated_content = pattern.sub(replace_link, content)
    
    # Güncellenmiş içeriği yeni dosyaya yaz
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

# Kullanım
update_m3u_links('gol.m3u', 'm3u_link_alındı2.txt', 'gol_guncel.m3u')
