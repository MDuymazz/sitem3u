# Dosya adlarını tanımlıyoruz
input_file = "son_m3u.txt"
output_file = "gol.m3u"
link_file = "ana_link.txt"
logo_file = "logo.txt"  # Logo verisinin olduğu dosya

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

# Logo verilerini içeren sözlük oluştur
logo_dict = {}
baska_logo = ""  # Varsayılan logo için boş değişken

try:
    with open(logo_file, "r", encoding="utf-8") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                key = key.strip()
                value = value.strip().replace('"', '')  # Gereksiz tırnakları kaldır

                if key == "BASKA":
                    baska_logo = value  # Varsayılan logo olarak kaydet
                else:
                    logo_dict[key] = value  # Normal logoları kaydet
except FileNotFoundError:
    print("⚠️ Uyarı: 'logo.txt' dosyası bulunamadı! Logolar eklenmeyecek.")

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

            # tvg-name'e göre logo belirle, eşleşme yoksa BASKA kullan
            logo_url = logo_dict.get(text, baska_logo)

            # Logo URL varsa M3U satırına ekle
            logo_part = f' tvg-logo="{logo_url}"' if logo_url else ""

            # TV8,5 ismini 8-5 olarak değiştirme
            if text == "TV8,5":
                text = "TV 8-5"

            formatted_entry = f"""
#EXTINF:-1 tvg-name="{text}"{logo_part} tvg-language="Turkish" tvg-country="TR" group-title="GÜNLÜK SPOR AKIŞI 2",{text}
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

# tvg-name'e göre sıralama ve CANLI olanları en üste taşıma
def custom_sort(entry):
    if 'CANLI' in entry:
        return (0, entry)
    elif 'BUGÜN' in entry:
        return (1, entry)
    elif 'YARIN' in entry:
        return (2, entry)
    return (3, entry.split('tvg-name="')[1][:14])

formatted_data_sorted = sorted(formatted_data[1:], key=custom_sort)

# Sıralı verileri başlık ile birleştiriyoruz
final_data = formatted_data[:1] + formatted_data_sorted

# Dosyaya yazma işlemi
try:
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(final_data)
    print(f"✅ M3U dosyası başarıyla oluşturuldu: {output_file}")
except Exception as e:
    print(f"❌ Hata: M3U dosyası oluşturulurken bir hata oluştu: {e}")
