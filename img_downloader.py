
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

# İndirilecek resimlerin kaydedileceği klasör
output_dir = 'downloaded_images'
os.makedirs(output_dir, exist_ok=True)

# İlk sayfayı yükle ve toplam sayfa sayısını bul
base_url = "https://www.bilezikci.com/kategori/ajda-bilezik"
first_page_response = requests.get(base_url + "?tp=1")

if first_page_response.status_code == 200:
    # HTML'yi parse et
    soup = BeautifulSoup(first_page_response.text, 'html.parser')

    # Toplam sayfa sayısını bul
    last_page_link = soup.select_one('div.paginate-content a:last-child')
    if last_page_link:
        total_pages = int(last_page_link.text.strip())
        print(f"Toplam Sayfa Sayısı: {total_pages}")
        
        # Sayfaları döngü ile gez
        for page in range(1, total_pages + 1):
            print(f"Sayfa {page} yükleniyor...")
            response = requests.get(f"{base_url}?tp={page}")

            if response.status_code == 200:
                # HTML'yi parse et
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # showcase-image-container class'ına sahip resimleri seç
                images = soup.select('div.showcase-container div.row div.col-6.col-lg-4 div.showcase div.showcase-image-container div.showcase-image a img')
                
                # Tüm resimlerin kaynaklarını al
                clean_image_urls = []
                for img in images:
                    img_url = img.get('src')  # 'src' özniteliğini al
                    if img_url:  # Eğer img_url None değilse
                        # Eğer URL'de ?revision=... kısmı varsa kaldır
                        if '?' in img_url:
                            img_url = img_url.split('?')[0]

                        # Eğer URL başında // varsa, https:// ile değiştir
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif not img_url.startswith('http'):  # URL'de http veya https yoksa, düzelt
                            img_url = 'https://' + img_url

                        clean_image_urls.append(img_url)

                # Resimleri indir, boyutlandır ve kaydet
                for i, img_url in enumerate(clean_image_urls, 1):
                    try:
                        # Resmi indir
                        img_response = requests.get(img_url)
                        img_response.raise_for_status()  # Hata kontrolü

                        # Resmi BytesIO ile yükle
                        img = Image.open(BytesIO(img_response.content))

                        # Resmi 224x224 boyutuna ölçeklendir
                        img = img.resize((224, 224))

                        # Resim uzantısını kontrol et ve gerekli dönüşümü yap
                        if img.format == 'WEBP':
                            img = img.convert('RGBA')  # Dönüşüm için RGBA formatına al
                            img_name = os.path.join(output_dir, f'image_page{page}_{i}.png')
                            img.save(img_name, 'PNG')  # PNG formatında kaydet
                            print(f"Sayfa {page}, Resim {i} indirildi ve 224x224 boyutunda PNG olarak kaydedildi: {img_name}")
                        else:
                            img_name = os.path.join(output_dir, f'image_page{page}_{i}.{img.format.lower()}')
                            img.save(img_name)  # Orijinal formatta kaydet
                            print(f"Sayfa {page}, Resim {i} indirildi ve 224x224 boyutunda kaydedildi: {img_name}")
                    except Exception as e:
                        print(f"Sayfa {page}, Resim {i} için hata: {e}")
            else:
                print(f"Sayfa {page} yüklenemedi. HTTP Status Code: {response.status_code}")
    else:
        print("Toplam sayfa sayısı bulunamadı.")
else:
    print(f"Sayfa yüklenemedi. HTTP Status Code: {first_page_response.status_code}")
