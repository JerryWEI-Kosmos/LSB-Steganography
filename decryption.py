import re
from scramble import *
from PIL import Image
import numpy as np


# 将提取出的密文转换为可读密文信息
def decode_txt(carrier_array,index):
    h, w, c = carrier_array.shape
    cryptograph_string = ""
    for i in range(h):
        for j in range(w):
            cryptograph_string = cryptograph_string + "" + str(carrier_array[i][j][index] % 2)
    cryptograph = ""
    ciphertext_list = re.findall(r'.{8}', cryptograph_string)
    for i in range(len(ciphertext_list)):
        cryptograph = cryptograph + "" + str(chr(int(ciphertext_list[i], 2)))
    return cryptograph


# 将01矩阵转换会RGB图像
def decode_image(carrier_array):
    h, w, c = carrier_array.shape
    new_w = int(w/8)
    # decode_cryptograph = np.zeros((h, int(w / 8), 3),dtype='uint8')
    # 将加密信息从截取的隐写区域中读出成字符串
    dearray_r = np.zeros((h,new_w),dtype='uint8')
    dearray_g = np.zeros((h,new_w),dtype='uint8')
    dearray_b = np.zeros((h,new_w),dtype='uint8')
    cryptograph_string = ""
    for index in range(c):
        for i in range(h):
            for j in range(w):
                cryptograph_string = cryptograph_string + "" + str(carrier_array[i][j][index] % 2)
    ciphertext_list = re.findall(r'.{8}', cryptograph_string)
    # 将字符串还原成矩阵
    lenth = len(ciphertext_list)
    n = 0
    m = n + int(lenth/3)
    k = n + 2*int(lenth/3)
    for j in range(h):
        for i in range(new_w):
            dearray_r[i][j] = int(ciphertext_list[n], 2)
            dearray_g[i][j] = int(ciphertext_list[m], 2)
            dearray_b[i][j] = int(ciphertext_list[k], 2)
            n = n + 1
            m = m + 1
            k = k + 1
    # 将各通道矩阵进行转置获得原图矩阵
    array_r = np.transpose(dearray_r)
    array_g = np.transpose(dearray_g)
    array_b = np.transpose(dearray_b)
    # 将转置后的各通道图像矩阵转换回正常的图像
    deimage_r = Image.fromarray(array_r)
    deimage_g = Image.fromarray(array_g)
    deimage_b = Image.fromarray(array_b)
    # 将各通道图片恢复成RGB图像
    cryptograph_image = Image.merge("RGB",(deimage_r,deimage_g,deimage_b))
    # 返回经过logistic_img解密的图片
    return logistic_img(cryptograph_image)
    # return cryptograph_image


# 将密文图像灰度图转换为正常可视灰度图
def decode_gray_image(carrier_array,index):
    h, w, c = carrier_array.shape
    new_w = int(w / 8)
    # 将加密信息从截取的隐写区域中读出成字符串
    decode_array = np.zeros((h, new_w), dtype='uint8')
    cryptograph_string = ""
    for index in range(c):
        for i in range(h):
            for j in range(w):
                cryptograph_string = cryptograph_string + "" + str(carrier_array[i][j][index] % 2)
    ciphertext_list = re.findall(r'.{8}', cryptograph_string)
    # 将字符串还原成矩阵
    n = 0
    for j in range(h):
        for i in range(new_w):
            decode_array[i][j] = int(ciphertext_list[n], 2)
            n = n + 1
    # 将各通道矩阵进行转置获得原图矩阵
    array_t = np.transpose(decode_array)
    # 将转置后的各通道图像矩阵转换回正常的图像
    cryptograph_image = Image.fromarray(array_t)
    # 返回经过logistic_img解密的图片
    return logistic_Gray_img(cryptograph_image)
    # return cryptograph_image


# 将密文二值图转换成正常可读的二值图
def decode_binary_image(cryptograph_array,index):
    h, w, c = cryptograph_array.shape
    decode_cryptograph = np.zeros((h,w),dtype='bool')
    for j in range(h):
        for i in range(w):
            if cryptograph_array[i][j][index] % 2 == 0:
                decode_cryptograph[i][j] = False
            else:
                decode_cryptograph[i][j] = True
    cryptograph_image = Image.fromarray(decode_cryptograph)
    # 返回logistic_img解密的图片
    return cryptograph_image
    # return logistic_binary_img(cryptograph_image)


# 提取密文
def decryption(carrier, keys):
    # 判断要解密的图像是否与原始图像的大小一致
    try:
        # 裁剪出隐写区域
        carrier = carrier.crop((keys[0], keys[1], keys[0] + keys[4], keys[1] + keys[3]))
    except TypeError:
        print("当前图像受到了裁剪攻击或压缩攻击，密文完整性受到破坏，暂时无法解密！")
    # 将裁剪出的隐写区域转换为nArray
    carrier_array = np.array(carrier)
    # 对二值图进行解密
    if keys[5] == 1:
        index = keys[2]
        cryptograph = decode_binary_image(carrier_array, index)
    # 对RGB图像进行解密
    elif keys[5] == 2:
        cryptograph = decode_image(carrier_array)
    # 对灰度图进行解密
    elif keys[5] == 3:
        index = keys[2]
        cryptograph = decode_gray_image(carrier_array,index)
    # 对文本进行解密
    elif keys[5] == 4:
        index = keys[2]
        cryptograph = decode_txt(carrier_array,index)

    return cryptograph