# Dosya adları
input_file = "son_m3u.txt"
output_file = "gol.m3u"
link_file = "ana_link.txt"
logo_file = "logo.txt"

# Referrer URL'yi al
try:
    with open(link_file, "r", encoding="utf-8") as file:
        referrer_url = file.read().strip()
        if not referrer_url.startswith("http"):
            raise ValueError("Ana link dosyasında geçerli bir URL yok.")
except Exception as e:
    print(f"❌ Hata: {e}")
    exit()

# Giriş verisini oku
try:
    with open(input_file, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print("❌ Hata: 'son_m3u.txt' dosyası yok!")
    exit()

if not lines:
    print("❌ Hata: 'son_m3u.txt' dosyası boş!")
    exit()

# Logo verisi
logo_dict = {}
baska_logo = ""
try:
    with open(logo_file, "r", encoding="utf-8") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                key = key.strip()
                value = value.strip().replace('"', '')
                if key == "BASKA":
                    baska_logo = value
                else:
                    logo_dict[key] = value
except FileNotFoundError:
    print("⚠️ Uyarı: 'logo.txt' dosyası bulunamadı! Logosuz devam.")

# Başlık
formatted_data = ["#EXTM3U\n"]

i = 0
while i + 2 < len(lines):
    match_type = lines[i].split(":", 1)[1].replace('"', '').strip().lower()
    text = lines[i + 1].split(":", 1)[1].replace('"', '').strip()
    url = lines[i + 2].strip()

    if not url.startswith("http"):
        print(f"⚠️ Geçersiz URL atlandı: {url}")
        i += 3
        continue

    logo_url = logo_dict.get(text, baska_logo)
    logo_part = f' tvg-logo="{logo_url}"' if logo_url else ""

    if text == "TV8,5":
        text = "TV 8-5"

    group_title = "SPOR YAYINLARI 2 (MAC SAATİ)" if match_type == "CANLI" else "GÜNLÜK SPOR AKIŞI 2"

    formatted_entry = f"""#EXTINF:-1 tvg-name="{text}"{logo_part} tvg-language="Turkish" tvg-country="TR" group-title="{group_title}",{text}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
#EXTVLCOPT:http-referrer={referrer_url}
{url}
"""
    formatted_data.append(formatted_entry)
    i += 3

# CANLI olanları yukarı al
def custom_sort(entry):
    if 'CANLI' in entry:
        return (0, entry)
    elif 'BUGÜN' in entry:
        return (1, entry)
    elif 'YARIN' in entry:
        return (2, entry)
    return (3, entry)

sorted_data = sorted(formatted_data[1:], key=custom_sort)
final_data = formatted_data[:1] + sorted_data

# Yaz
try:
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(final_data)
    print(f"✅ M3U dosyası başarıyla yazıldı: {output_file}")
except Exception as e:
    print(f"❌ Yazma hatası: {e}")
