from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import warnings

# Tarayıcı seçeneklerini ayarlıyoruz
options = Options()
options.add_argument("--headless")  # Tarayıcıyı başsız çalıştır
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Doğru ChromeDriver sürümünü otomatik indiriyoruz
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

# Hata mesajlarını bastırıyoruz
warnings.filterwarnings("ignore", category=UserWarning, message=".*undetected_chromedriver.*")

# m3u_link.txt dosyasındaki ilk URL'yi okuma
with open("m3u_link.txt", "r", encoding="utf-8") as file:
    url = file.readline().strip()

video_url = "https://LİNK BULUNAMADI.m3u8"
if url:
    try:
        print(f"🔍 {url} sayfası açılıyor...")
        driver.get(url)

        time.sleep(5)

        # Ağ isteklerini takip ederek video URL'lerini alma
        logs = driver.execute_script("return performance.getEntriesByType('resource');")
        video_urls = [log['name'] for log in logs if log['name'].endswith(('.m3u8', '.mp4'))]

        if video_urls:
            video_url = max(video_urls, key=len)
            print(f"🎥 En uzun video URL'si bulundu: {video_url}")
        else:
            print("⚠️ Bu sayfada video URL'si bulunamadı.")
    except Exception as e:
        print(f"❌ {url} sayfasında hata oluştu: {e}")

# Video URL'sini kaydetme
with open("m3u_link_alındı.txt", "w", encoding="utf-8") as file:
    file.write(f"{video_url}\n")

print("🎉 Video URL'si m3u_link_alındı.txt dosyasına kaydedildi.")

# Tarayıcıyı kapatma
try:
    driver.quit()
    print("Tarayıcı başarıyla kapatıldı.")
except Exception as e:
    print(f"Tarayıcıyı kapatma hatası (görmezden gelindi): {e}")
