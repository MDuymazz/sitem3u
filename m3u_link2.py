import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
import warnings

# Tarayıcı seçeneklerini ayarlıyoruz
options = Options()
options.add_argument("--headless")  # Tarayıcıyı başsız çalıştır
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Tarayıcıyı başlatıyoruz
driver = uc.Chrome(options=options)

# Hata mesajlarını bastırıyoruz
warnings.filterwarnings("ignore", category=UserWarning, message=".*undetected_chromedriver.*")

# m3u_link.txt dosyasındaki ilk URL'yi okuma
with open("m3u_link.txt", "r", encoding="utf-8") as file:
    url = file.readline().strip()  # İlk satırı okuyoruz

# URL kontrolü
video_url = "https://LİNK BULUNAMADI.m3u8"
if url:
    try:
        print(f"🔍 {url} sayfası açılıyor...")
        driver.get(url)  # URL'yi açıyoruz

        # Sayfanın yüklenmesi için bekleme süresi
        time.sleep(5)

        # Ağ isteklerini takip ederek video URL'lerini alma
        logs = driver.execute_script("return performance.getEntriesByType('resource');")
        video_urls = [log['name'] for log in logs if log['name'].endswith(('.m3u8', '.mp4'))]

        # Eğer video URL'leri varsa en uzun olanı seçiyoruz
        if video_urls:
            video_url = max(video_urls, key=len)
            print(f"🎥 En uzun video URL'si bulundu: {video_url}")
        else:
            print("⚠️ Bu sayfada video URL'si bulunamadı.")
    except Exception as e:
        print(f"❌ {url} sayfasında hata oluştu: {e}")

# Video URL'sini kaydetme
with open("m3u_link_alındı2.txt", "w", encoding="utf-8") as file:
    file.write(f"{video_url}\n")

print("🎉 Video URL'si m3u_link_alındı2.txt dosyasına kaydedildi.")

# Tarayıcıyı kapatma
try:
    driver.quit()
    print("Tarayıcı başarıyla kapatıldı.")
except Exception as e:
    print(f"Tarayıcıyı kapatma hatası (görmezden gelindi): {e}")
