# mac_verileri.txt ve m3u_link_alındı.txt dosyalarını okuma
with open("mac_verileri.txt", "r", encoding="utf-8") as mac_file:
    mac_verileri = mac_file.read().split("\n\n")  # Her bir maç bilgisi arasına boşluk eklenmiş

with open("final_url.txt", "r", encoding="utf-8") as link_file:
    m3u_links = link_file.readlines()

# Sonuçları son_m3u.txt dosyasına kaydetmek için açıyoruz
with open("son_m3u.txt", "w", encoding="utf-8") as output_file:
    # mac_verileri ve m3u_links'leri eşleştirip yazıyoruz
    for i, match in enumerate(mac_verileri):
        if i < len(m3u_links):
            output_file.write(match + "\n")
            output_file.write(m3u_links[i].strip() + "\n\n")  # Linki ekleyip bir satır boşluk bırakıyoruz

print("Veriler başarıyla son_m3u.txt dosyasına kaydedildi.")
