input_file = "son_m3u.txt"
output_file = "gol.m3u"
link_file = "ana_link.txt"
logo_file = "logo.txt"

# Referrer al
try:
    with open(link_file, "r", encoding="utf-8") as f:
        referrer_url = f.read().strip()
        if not referrer_url.startswith("http"):
            raise ValueError("Geçerli bir URL değil.")
except Exception as e:
    print(f"HATA: {e}")
    exit()

# Veri oku
try:
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("HATA: son_m3u.txt dosyası yok!")
    exit()

# Logo verileri
logo_dict = {}
baska_logo = ""
try:
    with open(logo_file, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                k = k.strip()
                v = v.strip().replace('"', '')
                if k == "BASKA":
                    baska_logo = v
                else:
                    logo_dict[k] = v
except FileNotFoundError:
    print("UYARI: logo.txt yok, logosuz devam.")

formatted_data = ["#EXTM3U\n"]

i = 0
while i + 2 < len(lines):
    match_type_raw = lines[i]
    text_raw = lines[i + 1]
    url = lines[i + 2].strip()

    # Veriyi çek
    match_type = match_type_raw.split(":", 1)[1].replace('"', '').strip().upper()
    text = text_raw.split(":", 1)[1].replace('"', '').strip()

    # Logo
    logo = logo_dict.get(text, baska_logo)
    logo_part = f' tvg-logo="{logo}"' if logo else ""

    # TV8,5 düzelt
    if text == "TV8,5":
        text = "TV 8-5"

    # Grup başlığı
    if match_type == "CANLI":
        group_title = "SPOR YAYINLARI (MAC SAATİ)"
    else:
        group_title = "GÜNLÜK SPOR AKIŞI 2"

    entry = f"""#EXTINF:-1 tvg-name="{text}"{logo_part} tvg-language="Turkish" tvg-country="TR" group-title="{group_title}",{text}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
#EXTVLCOPT:http-referrer={referrer_url}
{url}
"""
    formatted_data.append(entry)
    i += 3

# Dosyaya yaz
try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(formatted_data)
    print(f"✅ Tamamlandı: {output_file}")
except Exception as e:
    print(f"Yazma hatası: {e}")
