import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Modeli yükleyin
model = load_model('vitrinai.h5')

# Etiketler
class_labels = ["Şarnel", "Burma", "Tel"]

# Resmi yükleme ve ön işleme
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (224, 224))
    image_normalized = image_resized / 255.0
    return image, np.expand_dims(image_normalized, axis=0)

# Tahmin ve görselleştirme fonksiyonu
def predict_and_visualize(image_path):
    # Resmi işle
    original_image, preprocessed_image = preprocess_image(image_path)
    
    # Model ile tahmin yap
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions)
    confidence = predictions[0][predicted_class]
    
    # Sonuçları ekrana yazdır
    label_text = f"{class_labels[predicted_class]} {confidence:.2f}"
    
    # Kırmızı çerçeve ve maskeleme
    height, width, _ = original_image.shape
    x, y, w, h = 50, 50, width - 100, height - 100  # Çerçeve pozisyonu
    cv2.rectangle(original_image, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Kırmızı çerçeve
    mask = np.zeros_like(original_image, dtype=np.uint8)
    mask[y:y+h, x:x+w] = (0, 0, 255)  # Kırmızı maske
    original_image = cv2.addWeighted(original_image, 0.7, mask, 0.3, 0)  # Maske uygulama
    
    # Sol üst köşeye metin
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_color = (255, 255, 255)  # Beyaz yazı
    bg_color = (0, 0, 255)  # Kırmızı arka plan
    text_size = cv2.getTextSize(label_text, font, font_scale, 1)[0]
    text_x, text_y = x, y - 10
    cv2.rectangle(original_image, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), bg_color, -1)
    cv2.putText(original_image, label_text, (text_x, text_y - 2), font, font_scale, font_color, 1)
    
    # Görüntüyü göster
    cv2.imshow("Bilezik Tespiti", original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Resmi test etmek için
image_path = "/mnt/data/test.jpg"
predict_and_visualize(image_path)