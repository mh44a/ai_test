import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Dataset yolları
base_dir = 'dataset/train'  # Dataset dizininin yolunu ayarlayın

# Resim veri ön işleme
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

# Eğitim ve doğrulama veri kümeleri
train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=(224, 224),  # Resim boyutu
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    base_dir,
    target_size=(224, 224),  # Resim boyutu
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Modeli oluştur
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    tf.keras.layers.Flatten(),  # Flatten katmanı burada ekleniyor
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(train_generator.class_indices), activation='softmax')  # Çıkış katmanı
])

# Modeli derle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Modeli eğit
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=10
)
