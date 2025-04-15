import requests

input_file = "ana_link.txt"

# Dosyadan linki oku
with open(input_file, "r") as file:
    original_url = file.readline().strip()

try:
    # İsteği yap (redirectleri takip eder)
    response = requests.get(original_url, timeout=10)
    
    # Son URL'yi al (redirect sonucu oluşan gerçek URL)
    final_url = response.url
    
    # Eğer yönlendirilmişse ve farklıysa, dosyayı güncelle
    if final_url != original_url:
        with open(input_file, "w") as file:
            file.write(final_url + "\n")
        print(f"Yönlendirme tespit edildi. Yeni URL dosyaya yazıldı: {final_url}")
    else:
        print("Yönlendirme yok. URL aynı kaldı.")
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")
