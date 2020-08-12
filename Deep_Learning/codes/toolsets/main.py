import numpy as np
from keras import layers, models
from keras.utils import to_categorical
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation="sigmoid"))

model.compile(
    optimizer=optimizers.RMSprop(lr=0.0001),
    loss="binary_crossentropy",
    metrics=["acc"]
)

# 数据预处理
train_dir = r"D:\Practice_Code\Python\DEEP_LEARNING\toolsets\small_pictures\train"
validation_dir = r"D:\Practice_Code\Python\DEEP_LEARNING\toolsets\small_pictures\validation"
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,           # 图像随机旋转的角度范围(0~180)
    width_shift_range=0.2,       # 图像在水平方向上平移的范围（比例）
    height_shift_range=0.2,      # 图像在垂直方向上平移的范围（比例）
    shear_range=0.2,             # 随机错切变换的角度
    zoom_range=0.2,              # 图像随机缩放的范围
    horizontal_flip=True,        # 随机将一半图像水平翻转
    fill_mode="nearest"          # 填充新创建像素的方法
)

#不能增强验证数据
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')
validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')

history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=100,
    validation_data=validation_generator,
    validation_steps=50
)

# 保存模型
model.save('cats_dogs_small_1.h5')

# 绘制训练过程中的损失曲线和精度曲线
import matplotlib.pyplot as plt
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc)+1)
plt.plot(epochs, acc, 'bo', label="Training Acc")
plt.plot(epochs, val_acc, 'b', label="Validation Acc")
plt.title("Trainging and validation Accuracy")
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'bo', label="Training Loss")
plt.plot(epochs, val_loss, 'b', label="Validation Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.figure()

plt.show()