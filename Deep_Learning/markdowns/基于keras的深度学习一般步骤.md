---
tags: [Deep Learning]
title: keras运行MNIST
created: '2020-08-11 09:50:00'
modified: '2020-08-11 09:50:00'
---



- 数据采集
  - 规范化数据统一性，比如图片要保证图像位置，尺寸统一
  - 保证数据和标签的统一
- 定义训练数据：输入张量和目标张量
- 数据预处理
  - 数据格式的转换
  - 数据转换，以方便计算，one-hot等方法
- 定义层 组成的网络（或模型），将输入映射到目标
- 配置学习过程：选择损失函数、优化器和需要监控的目标
- 调用模型的fit方法在训练数据上进行迭代
- 验证

```python
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
```

- 损失函数的选择：
  - 二分类问题： 一般选用二元交叉熵，binary-corssentropy
  - 多分类问题： 一般选用分类交叉熵，categorical-corssentropy
  - 回归问题： 一般选用均方误差(MSE)，mean-squared error
    - 回归问题评估指标一般是MAE，平均绝对误差
  - 序列学习问题： 一般选用联结主义时序分类，CTC connectionist temporal classification

- 激活函数：

  - Dense层如果没有激活函数的参与，就只会进行点积和加法的运算，就只会进行线性变换，

    而激活函数则可以扩展假设空间，因为有了非线性的运算。

- 网络架构的确定：
  - 网络的层数
  - 每层的隐藏单元数量

### 二分类（电影评论的正面负面）

```Python
import time
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import imdb
from keras import models, layers
from keras import optimizers, losses, metrics

def vectorize_sequence(sequences, dimention=10000):
    results = np.zeros((len(sequences), dimention))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

x_train = vectorize_sequence(train_data)
x_test = vectorize_sequence(test_data)

y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

network = models.Sequential()
network.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
network.add(layers.Dense(16, activation='relu'))
network.add(layers.Dense(1, activation='sigmoid'))

network.compile(
    optimizer=optimizers.RMSprop(learning_rate=0.001),
    loss=losses.binary_crossentropy,
    metrics=["acc"])

x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

history = network.fit(
    partial_x_train,
    partial_y_train,
    epochs=4,
    batch_size=512,
    validation_data=(x_val, y_val)
)

# history_dict = history.history
# loss_values = history_dict['loss']
# val_loss_values = history_dict['val_loss']
# epochs = range(1, len(loss_values) + 1)
# plt.plot(epochs, loss_values, "bo", label="Training loss")
# plt.plot(epochs, val_loss_values, 'b', label="Validation loss")
# plt.title("Training and Validation loss")
# plt.xlabel("Epochs")
# plt.ylabel("Loss")
# plt.legend()
# plt.show()

# time.sleep(10)

# plt.clf()
# acc = history_dict['acc']
# val_acc = history_dict['val_acc']
# plt.plot(epochs, acc, "bo", label="Training acc")
# plt.plot(epochs, val_acc, 'b', label="Validation acc")
# plt.title("Training and Validation accuracy")
# plt.xlabel("Epochs")
# plt.ylabel("Accuracy")
# plt.legend()
# plt.show()

# 使用测试集验算该模型的精度
results = network.evaluate(x_test, y_test)
print(results)

# 使用模型对测试集进行预测
network.predict(x_test)
```

### 多分类（新闻类型分类）

```Python
import numpy as np
from keras.datasets import reuters
from keras import models, layers

(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)

# 向量化数据
def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

def one_hot_labels(labels, dimension=46):
    """
    向量化标签，标签总类有46中，每类标签由一种向量表示，例如：
    政治类: [0, 0, ..., 0, 1] -> 长度46，最后一位为1
    体育类: [0, 0, ..., 1, 0] -> 长度46, 倒数第二位为1
    """
    results = np.zeros((len(labels), dimension))
    for i, label in enumerate(labels):
        results[i, label] = 1.
    return results

ont_hot_train_labels = one_hot_labels(train_labels)
ont_hot_test_labels = one_hot_labels(test_labels)

# 也可以直接使用keras内置方法进行操作
# from keras.utils import to_categorical
# ont_hot_train_labels = to_categorical(train_labels)
# ont_hot_test_labels = to_categorical(test_labels)

# build netword
network = models.Sequential()
network.add(layers.Dense(64, activation='relu', input_shape=(10000, )))
network.add(layers.Dense(64, activation='relu'))
network.add(layers.Dense(46, activation='softmax')) # 最后一步输出46种分类的概率


# 因为此处的分类标签使用的是one_hot编码，所以使用categorical损失函数，
# 如果使用整数张量np.array(train_labels), 则需要使用sparse_categorical_crossentropy，
# 两种损失函数数学上完全相同，只是接口不同，对应不同编码的标签
network.compile(
    optimizer='rmsprop',
    loss='categorical_corssentropy',
    metrics=['accuracy']
)

# 切割一部分验证数据
x_val = x_train[:1000]
partial_x_train = x_train[1000:]

y_val = ont_hot_train_labels[:1000]
partial_y_train = ont_hot_train_labels[1000:]

history = network.fit(
    partial_x_train,
    partial_y_train,
    epochs=9,
    batch_size=512,
    validation_data=(x_val, y_val)
)

results = network.evaluate(x_test, one_hot_test_labels)
print(results)

predictions = network.predict(x_test)
```

### 房价预测，回归问题，多特征

```Python
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import boston_housing
from keras import models, layers


(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()

# 数据预处理
# 数据标准化，为了减少每个特征大范围的差异
# 所以把数据减去特征平均值再除以标准差
# 这样得到的特征平均值为0， 标准差为1

mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std

def build_model():
    """
    loss(mse): 均方误差，预测值与目标值之差的平方
    metrics(mae): 平均绝对误差，目标值与预测值之差的绝对值
    """
    network = models.Sequential()
    network.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
    network.add(layers.Dense(64, activation='relu'))
    network.add(layers.Dense(1))
    network.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    return network

# 在对于实际训练和验证的数据集数量较少的情况下，可以使用K折验证
# 将数据划为为K个分区(K通常取4、5)， 实例化K个相同的模型
# 将每个模型在K-1个分区上训练，并在剩下的一个分区上进行评估
# 模型的验证分数等于K个验证分数的平均值

# K = 4
# num_val_samples = len(train_data) // K
# num_epochs = 100
# all_mae_histories = []

# for i in range(K):
#     print("processing fold #", i)
#     val_data = train_data[i * num_val_samples: (i+1) * num_val_samples]
#     val_targets = train_targets[i * num_val_samples: (i+1) * num_val_samples]

#     partial_train_data = np.concatenate(
#         [train_data[:i * num_val_samples],
#          train_data[(i+1) * num_val_samples:]],
#         axis=0
#     )
#     partial_train_targets = np.concatenate(
#         [train_targets[:i * num_val_samples],
#          train_targets[(i+1) * num_val_samples:]],
#         axis=0
#     )
#     model = build_model()
#     history = model.fit(partial_train_data, partial_train_targets,
#                validation_data=(val_data, val_targets),
#                epochs=num_epochs, batch_size=1, verbose=0)
#     all_mae_histories.append(history.history['val_mae'])

# avg_mae_history = [
#     np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)
# ]

# # 查看验证分数
# plt.plot(range(1, len(avg_mae_history) + 1), avg_mae_history)
# plt.xlabel("Epochs")
# plt.ylabel("Validation MAE")
# plt.show()

# 通过验证分数，可以进行epochs和隐藏层大小的调节
# 最后可以得到合适的epochs和隐藏层

model = build_model()
# verbose=0 为静默训练，不显示过程数据
model.fit(train_data, train_targets,
          epochs=80, batch_size=16, verbose=0)
test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)
print(test_mae_score)
```

