# Dosya adlarını tanımlıyoruz
input_file = "son_m3u.txt"
output_file = "gol.m3u"
link_file = "ana_link.txt"

try:
    # ana_link.txt dosyasındaki ana URL'yi alıyoruz
    with open(link_file, "r", encoding="utf-8") as file:
        referrer_url = file.read().strip()
        if not referrer_url.startswith("http"):
            raise ValueError("Ana link dosyasında geçerli bir URL bulunamadı.")
except FileNotFoundError:
    print("❌ Hata: 'ana_link.txt' dosyası bulunamadı!")
    exit()
except ValueError as e:
    print(f"❌ Hata: {e}")
    exit()

try:
    # son_m3u.txt dosyasındaki verileri okuyoruz
    with open(input_file, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]  # Boş satırları temizle
except FileNotFoundError:
    print("❌ Hata: 'son_m3u.txt' dosyası bulunamadı!")
    exit()

# Eğer veri yoksa işlemi durdur
if not lines:
    print("❌ Hata: 'son_m3u.txt' dosyası boş!")
    exit()

formatted_data = ["#EXTM3U\n"]  # M3U başlığı ekle

i = 0
while i < len(lines):
    try:
        if lines[i].startswith("MatchType:") and i + 2 < len(lines):
            match_type = lines[i].replace('MatchType: ', '').replace('"', '')
            text = lines[i + 1].replace('Text: ', '').replace('"', '')
            url = lines[i + 2]

            if not url.startswith("http"):
                print(f"⚠️ Geçersiz URL atlandı: {url}")
                i += 3
                continue

            formatted_entry = f"""
#EXTINF:-1 tvg-name=\"{text.upper()}\" tvg-language=\"Turkish\" tvg-country=\"TR\" group-title=\"{match_type.upper()}\",{text.upper()}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
#EXTVLCOPT:http-referrer={referrer_url}
{url}
"""
            formatted_data.append(formatted_entry)
            i += 3
        else:
            print(f"⚠️ Eksik veya hatalı veri atlandı: {lines[i]}")
            i += 1
    except IndexError:
        print("⚠️ Beklenmeyen veri formatı, işleme devam ediliyor...")
        break

# Dosyaya yazma işlemi
try:
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(formatted_data)
    print(f"✅ M3U dosyası başarıyla oluşturuldu: {output_file}")
except Exception as e:
    print(f"❌ Hata: M3U dosyası oluşturulurken bir hata oluştu: {e}")
