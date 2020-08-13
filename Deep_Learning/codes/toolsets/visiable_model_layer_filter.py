import numpy as np
import tensorflow as tf
from keras.applications import VGG16
from keras import backend as K
model = VGG16(weights="imagenet", include_top=False, input_shape=(150, 150, 3))
# ===============test====================
    # layer_name = "block3_conv1"
    # filter_index = 0
    # layer_output = model.get_layer(layer_name).output
    # loss = K.mean(layer_output[:, :, :, filter_index])
    # # 为了实现梯度下降，我们需要得到损失相对于模型输入的梯度，为此使用keras.backend的内置函数gradients
    # # 返回的grads是个以元素为张量的列表。
    # grads = K.gradients(loss, model.input)[0]
    # # 为了让梯度下降过程顺利进行，一个非显而易见的技巧是将梯度张量除以其L2范数（张量中所有值的平方的平均值的平方根）来标准化。这就确保了输入图像的更新大小始终位于相同的范围
    # grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5) # 加上1e-5 以防不小心除0

    # # 计算给定输入图像的损失张量和梯度张量的值
    # iterate = K.function([model.input], [loss, grads])
    # import numpy as np
    # loss_value, grads_value = iterate([np.zeros((1, 150, 150, 3))])

    # # 进行随机梯度下降
    # # 从一张带有噪声的灰度图像开始
    # imput_img_data = np.random.random((1, 150, 150, 3)) * 20 + 128.
    # step = 1. # 每次梯度更新的步长
    # for i range(40):
    #     loss_value, grads_value = iterate([input_img_data])
    #     input_img_data += grads_value * step
# ============================================
# 得到的图像张量是形状为(1, 150, 150, 3)的浮点数张量，其取值可能不是[0-255]区间内的整数，因此还需要后期处理，将其转换为可显示的图像，定义一个处理函数
def deprocess_image(x):
    x -= x.mean() 			# 对张量做标准化，使其均值为0
    x /= (x.std() + 1e-5)	# 标准差为0.1
    x *= 0.1
    
    x += 0.5
    x = np.clip(x, 0, 1) 	# 将x剪裁到[0,1]区间
    
    x *= 255				# 将x转换为RGB数组
    x = np.clip(x, 0, 255).astype("uint8")
    return x
# ============将上诉内容抽象成一个函数===============
# 生成过滤器可视化函数
def generate_pattern(layer_name, filter_index, size=150):
    layer_output = model.get_layer(layer_name).output
    loss = K.mean(layer_output[:, :, :, filter_index])
    grads = K.gradients(loss, model.input)[0]
    grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)
    iterate = K.function([model.input], [loss, grads])
    input_img_data = np.ramdom.random((1, size, size, 3) * 20 + 128.)
    step = 1.
    for i in range(40):
        loss_value, grads_value = iterate([input_img_data])
        input_img_data += grads_value * step
    img = input_img_data[0]
    return deprocess_image(x)

# 调用函数测试
# plt.imshow(generate_pattern('block3_conv1', 0))
# plt.show()

# 生成某一层中所有过滤器相应模式组成的网格
layer_name = "block1_conv1"
size = 64 # 取前64个过滤器
margin = 5
results = np.zeros((8 * size + 7 * margin, 8 * size + 7 * margin, 3))
for i in range(8):
    for j in range(8):
        filter_img = generate_pattern(layer_name, i + (j * 8), size=size)
        horizontal_start = i * size + i * margin
        horizontal_end = horizontal_start + size
        vertical_start = j * size + j * margin
        vertical_end = vertical_start + size
        results[horizontal_start : horizontal_end,
               	vertical_start : vertical_end, :] = filter_img
plt.figure(figsize=(20, 20))
plt.imshow(results)
plt.show()