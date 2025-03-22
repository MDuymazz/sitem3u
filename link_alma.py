import requests
from bs4 import BeautifulSoup

# 'ana_link.txt' dosyasından URL'yi oku
with open('ana_link.txt', 'r') as file:
    url = file.readline().strip()

# URL'ye istek gönder
response = requests.get(url)

# Eğer istek başarılıysa
if response.status_code == 200:
    # HTML'i BeautifulSoup ile analiz et
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 'data-seolink' özelliğine sahip ilk öğeyi bul
    data_seolink = soup.find(attrs={"data-seolink": True})

    # Eğer 'data-seolink' bulunmuşsa
    if data_seolink:
        # Bulduğumuz değeri al
        seolink_value = data_seolink['data-seolink']
        
        # 'm3u_link.txt' dosyasına 'ana_link.txt' içeriğini ve 'data-seolink' değerini yaz
        with open('m3u_link.txt', 'w') as file:
            file.write(f"{url}{seolink_value}")

        print(f"Bulunan data-seolink değeri: {seolink_value}")
    else:
        print("data-seolink değeri bulunamadı.")
else:
    print(f"URL'ye istek başarısız. Durum Kodu: {response.status_code}")
