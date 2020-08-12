from keras.datasets import mnist
from keras import models, layers
from keras.utils import to_categorical

# 加载数据
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# train_images.shape -> (60000, 28, 28)
# train_labels.shape -> (60000,)

# 建立深度学习模型框架
network = models.Sequential()
# 训练层
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
# 分类层
network.add(layers.Dense(10, activation='softmax'))
# 选择网络的优化器和损失函数,并且指定监视的指标:metrics=accuracy即正确率
network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# 处理原始图像数据，方便计算
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# 训练
network.fit(train_images, train_labels, epochs=5, batch_size=128)
# 验证
test_loss, test_acc = network.evaluate(test_images, test_labels)