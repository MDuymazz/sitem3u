import requests

# Başlangıç yılı
year = 2013
base_url = "https://golvar{}.sbs/"
output_file = "ana_link.txt"

# Dosyayı açalım
with open(output_file, "w") as file:
    while True:
        url = base_url.format(year)
        try:
            # Bağlantıyı deniyoruz
            response = requests.get(url, timeout=10)  # 10 saniye zaman aşımı
            if response.status_code == 200:
                # Eğer bağlantı başarılıysa, URL'yi kaydediyoruz
                print(f"{url} başarılı, kaydedildi.")
                file.write(url + "\n")
                break  # İlk başarılı bağlantı sonrası döngüden çık
        except requests.exceptions.RequestException as e:
            # Eğer bağlantı hatası alırsak, yılı bir artırıyoruz
            print(f"{url} bağlantısı hatalı, {year} yılı başarısız. Bir sonraki yıla geçiliyor.")
            year += 1  # Yılı bir artırıyoruz (2015, 2016, 2017, ...)
