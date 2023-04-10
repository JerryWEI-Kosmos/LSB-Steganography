import numpy as np
from PIL import Image


# 将密文图片基于混沌Logistic映射加密算法加密
# 0<x<1 , 3.5699<u<4 , times为迭代次数
def logistic(img, x, u, times):
    M = img.size[0]
    N = img.size[1]
    for i in range(1, times):
        x = u * x * (1 - x)
    array = np.zeros(M * N)
    array[1] = x
    for i in range(1, M * N - 1):
        array[i + 1] = u * array[i] * (1 - array[i])
    array = np.array(array * 255, dtype='uint8')
    code = np.reshape(array, (M, N))
    xor = img ^ code
    v = xor
    return v


# RGB密文图像加密
def logistic_img(img):
    # 定义logistic运算参数
    x = 0.1
    u = 4
    times = 500
    # 将图片分割成三个颜色通道
    r, g, b = img.split()
    # 将三通道色分开进行置乱
    R = logistic(r, x, u, times)
    G = logistic(g, x, u, times)
    B = logistic(b, x, u, times)
    # 将置乱后的信息从矩阵转会单通道图像
    R = Image.fromarray(R)
    G = Image.fromarray(G)
    B = Image.fromarray(B)
    # 恢复RGB图像
    cimg = Image.merge("RGB", (R, G, B))
    return cimg


# 灰度图密文加密
def logistic_Gray_img(img):
    # 定义logistic运算参数
    x = 0.1
    u = 4
    times = 500
    # 将三通道色分开进行置乱
    c = logistic(img, x, u, times)
    # 将置乱后的信息从矩阵转会单通道图像
    cimg = Image.fromarray(c)
    return cimg

# 二值密文图像加密
def logistic_binary_img(img):
    # 定义logistic运算参数
    x = 0.1
    u = 4
    times = 500
    carray = logistic(img, x, u, times)
    cimg = Image.fromarray(carray)
    return cimg
