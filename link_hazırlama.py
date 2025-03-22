# m3u_link_alındı.txt dosyasındaki şablon linkini oku
with open("m3u_link_alındı.txt", "r", encoding="utf-8") as template_file:
    template_link = template_file.readline().strip()

# tüm_link.txt dosyasındaki numaraları oku
# Farklı encoding formatlarını deneyebiliriz, örneğin 'cp1254'
try:
    with open("tüm_link.txt", "r", encoding="utf-8") as numbers_file:
        numbers = numbers_file.readlines()
except UnicodeDecodeError:
    # Eğer utf-8 ile okumada hata alırsak, cp1254 encoding ile tekrar deneyelim
    with open("tüm_link.txt", "r", encoding="cp1254") as numbers_file:
        numbers = numbers_file.readlines()

# Yeni linkleri oluştur
new_links = []
for number in numbers:
    number = number.strip()  # Satırdaki boşlukları temizle
    new_link = template_link.replace("5062", number)  # "5062"yi numara ile değiştir
    new_links.append(new_link)

# Yeni linkleri bir dosyaya yaz
with open("new_links.txt", "w", encoding="utf-8") as output_file:
    for link in new_links:
        output_file.write(link + "\n")
