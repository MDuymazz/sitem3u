import re

def update_m3u_links(m3u_file, updated_link_file, output_file, base_url_file):
    # Yeni linki dosyadan oku
    with open(updated_link_file, 'r', encoding='utf-8') as f:
        new_link = f.readline().strip()
    
    # Ana linki (referer ve origin için) base_url_file dosyasından oku
    with open(base_url_file, 'r', encoding='utf-8') as f:
        base_url = f.readline().strip()  # https://golvar4137.sbs gibi bir URL alıyoruz
    
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
            # Güncellenmiş referer ve origin değerlerini ekle
            updated_url = f'https://playerpro.live/proxy.php?url={updated_link}&referer={base_url}&origin={base_url}'
            return updated_url
        return match.group(0)  # Eşleşme olmazsa değiştirme

    # `#EXTVLCOPT:http-referrer` kısmını da güncelle
    def update_referrer(match):
        return f'#EXTVLCOPT:http-referrer={base_url}/'

    # Referer ve linki güncelle
    updated_content = pattern.sub(replace_link, content)
    
    # `#EXTVLCOPT:http-referrer`'ı güncelle
    updated_content = re.sub(r'#EXTVLCOPT:http-referrer=[^\s]+', update_referrer, updated_content)
    
    # Güncellenmiş içeriği yeni dosyaya yaz
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

# Kullanım
update_m3u_links('gol.m3u', 'm3u_link_alındı2.txt', 'gol_guncel.m3u', 'ana_link.txt')
