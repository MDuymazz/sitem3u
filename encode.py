import urllib.parse
import re

# ana_link.txt dosyasından referer ve origin verilerini okuma
try:
    with open("ana_link.txt", "r") as file:
        lines = file.readlines()
        if len(lines) >= 1:
            referer = lines[0].strip()  
            origin = referer
        else:
            raise ValueError("ana_link.txt dosyasındaki satır sayısı yetersiz. En az bir satır olmalıdır.")
except FileNotFoundError:
    print("ana_link.txt dosyası bulunamadı.")
    exit(1)

# new_links.txt dosyasından URL'leri alma
try:
    with open("new_links.txt", "r") as file:
        content = file.read().strip()  # Dosyayı okuyup boşlukları temizle

    if not content:
        raise ValueError("new_links.txt dosyası boş.")

    # Çift tırnak olmadan URL'leri yakalayan regex
    urls = re.findall(r'https?://\S+', content)

    if not urls:
        raise ValueError("new_links.txt dosyasında geçerli URL bulunamadı.")
except FileNotFoundError:
    print("new_links.txt dosyası bulunamadı.")
    exit(1)

# Base URL
base_url = "https://playerpro.live/proxy.php?url="

# final_url'leri depolamak için bir liste
final_urls = []

# URL'leri işleme
for original_url in urls:
    # Eğer URL, https://playerpro.live ile başlıyorsa, direkt ekle
    if original_url.startswith("https://playerpro.live"):
        final_urls.append(f"{original_url}")
    else:
        # URL encode işlemi
        encoded_referer = urllib.parse.quote(referer, safe=":/?&=")  # referer için encode
        encoded_origin = urllib.parse.quote(origin, safe=":/?&=")    # origin için encode

        # original_url'yi encode etmeden kullanıyoruz çünkü zaten encode edilmiş
        final_url = f"{base_url}{urllib.parse.quote(original_url, safe=':/?&=')}&referer={encoded_referer}&origin={encoded_origin}"
        
        # final_url'yi listeye ekle
        final_urls.append(f"{final_url}")

# final_url'leri final_url.txt dosyasına kaydetme
try:
    with open("final_url.txt", "w") as output_file:
        for url in final_urls:
            output_file.write(url + "\n")
    print("final_url başarıyla final_url.txt dosyasına kaydedildi.")
except Exception as e:
    print(f"final_url.txt dosyasına yazarken bir hata oluştu: {e}")
