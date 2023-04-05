from random import *

from BinaryImage import *
from encryption import *
from RGBImage import *
from txt import *
import math
import numpy as np
import os
import sys
from PIL import Image


# 打开载体图像
def open_carrier():
    path = "./data/carriers/"
    carrier_list = os.listdir(path)
    print("载体文件如下：(打开为nArray)")
    for i in range(0, len(carrier_list)):
        width = Image.open(path + carrier_list[i]).width
        height = Image.open(path + carrier_list[i]).height
        print(str(i + 1) + "." + carrier_list[i] + " " + str(width) + "*" + str(height))
    while 1 == 1:
        num = int(input("请选择密文载体图像(输入序号)："))
        if num == 0:
            print("未选择载体信息！退出隐写")
            exit()
        # 判断输入是否合法
        elif num in range(1, len(carrier_list) + 1):
            # 打开选中的图像
            carrier = Image.open(path + carrier_list[num - 1])
            # 将图像转换为三通道RGB图像
            carrier_array = np.array(carrier.convert("RGB"))
            # 获取当前图像的高宽信息
            h, w, c = carrier_array.shape
            print("选择图像为:{} {}*{} {}通道\n".format(carrier_list[num - 1], h, w, c))
            return carrier_array
        else:
            print("输入编号超出范围！")
    return False


# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)


# 提取密文
def get_cryptograph(carrier, keys):
    # 裁剪出隐写区域
    carrier = carrier.crop((keys[0], keys[1], keys[0] + keys[4], keys[0] + keys[3]))
    # 将裁剪出的隐写区域转换为nArray
    carrier_array = np.array(carrier)
    if keys[5] == 2:
        cryptograph = decode_image(carrier_array)

    elif keys[5] == 3:
        index = keys[2]
        cryptograph = decode_txt(carrier_array,index)
    elif keys[5] == 1:
        index = keys[2]
        cryptograph = decode_binary_image(carrier_array)

    return cryptograph


# 性能计算
# 计算峰值信息量
def psnr(img_1, img_2):
    img_1int = np.array(img_1)
    img_2int = np.array(img_2)
    mse = np.mean((img_1int / 1.0 - img_2int / 1.0) ** 2)
    if mse < 1.0e-10:
        return 100
    return 10 * math.log10(255.0 ** 2 / mse)


# 选择要隐写的内容
def open_cryptograph():
    print("可选择如下隐写内容：")
    print("1.二值图隐写\n2.RGB隐写\n3.文本隐写\n0.退出隐写")
    num = int(input("请输入编号："))
    if num == 1:
        return open_binary_image(),1
    elif num == 2:
        return open_image(),2
    elif num == 3:
        return open_txt(),3
    elif num == 0:
        exit()


if __name__ == '__main__':
    carrier = open_carrier()
    cryptograph, flag = open_cryptograph()
    keys = creat_key(carrier, cryptograph, flag)
    print("密钥为：{}".format(keys))
    cImg = steganography(carrier, cryptograph, keys)
    cImg = Image.fromarray(cImg)
    carrier = Image.fromarray(carrier)
    cImg.show()

    PSNR = psnr(cImg, carrier)
    print("峰值信噪比 PSNR=%.1f dB" % PSNR)

    newcryptograph = get_cryptograph(cImg, keys)
    print(newcryptograph)
