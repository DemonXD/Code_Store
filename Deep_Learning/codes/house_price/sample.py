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