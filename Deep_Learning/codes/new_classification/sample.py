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

one_hot_train_labels = one_hot_labels(train_labels)
one_hot_test_labels = one_hot_labels(test_labels)

# 也可以直接使用keras内置方法进行操作
# from keras.utils import to_categorical
# one_hot_train_labels = to_categorical(train_labels)
# one_hot_test_labels = to_categorical(test_labels)

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
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 切割一部分验证数据
x_val = x_train[:1000]
partial_x_train = x_train[1000:]

y_val = one_hot_train_labels[:1000]
partial_y_train = one_hot_train_labels[1000:]

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