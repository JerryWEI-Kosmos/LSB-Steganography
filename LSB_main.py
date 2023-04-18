from BinaryImage import *
from encryption import *
from decryption import *
from GrayImage import *
from RGBImage import *
from attack import *
from PIL import Image
from txt import *
import numpy as np
import math
import os


# 打开载体图像
def open_carrier():
    path = "./data/carriers/"
    carrier_list = os.listdir(path)
    print("可选择的载体图像如下：(打开为nArray)")
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


# 性能计算
# 计算峰值信息量
def psnr(img_1, img_2):
    # 将要计算的图像打开成nArray矩阵
    img_1int = np.array(img_1)
    img_2int = np.array(img_2)
    # 计算差错平均值
    mse = np.mean((img_2int / 1.0 - img_1int / 1.0) ** 2)
    if mse < 1.0e-10:
        return 100
    # 返回峰值信噪比
    return 10 * math.log10(255.0 ** 2 / mse)


# 选择要隐写的内容
def open_cryptograph():
    print("可选择如下隐写内容：")
    print("1.二值图隐写\n2.RGB隐写\n3.灰度图隐写\n4.文本隐写\n0.退出隐写")
    num = int(input("请输入编号："))
    if num == 1:
        return open_binary_image(), 1
    elif num == 2:
        return open_image(), 2
    elif num == 3:
        return open_Grayimage(), 3
    elif num == 4:
        return open_txt(), 4
    elif num == 0:
        exit()


if __name__ == '__main__':
    # 选择测试模式
    print("选择测试模式")
    while 1 == 1:
        print("1.正常隐写与提取\n2.模拟攻击\n0.退出程序")
        num = int(input("选择测试模式："))
        if num > 2:
            print("选择超出范围！请重新选择")
        elif num == 0:
            print("退出程序...")
            exit()
        break
    # 打开载体图像
    carrier = open_carrier()
    # 打开密文图像
    cryptograph, flag = open_cryptograph()
    # 生成随机密钥
    keys = creat_key(carrier, cryptograph, flag)
    print("\n密钥为：{}".format(keys))
    # 进行LSB隐写
    cImg = steganography(carrier, cryptograph, keys)
    # 将隐写前后的图像从矩阵还原并输出载体图像和隐写后的载体图像
    cImg = Image.fromarray(cImg)
    cImg.show()
    carrier = Image.fromarray(carrier)
    carrier.show()
    # 计算隐写性能
    PSNR = psnr(cImg, carrier)
    print("峰值信噪比 PSNR=%.1f dB" % PSNR)
    if num == 1:
        # 从载体图像中提取密文
        newcryptograph = decryption(cImg, keys)
        # 识别隐写类型并输出提取后的密文
        if keys[5] == 4:
            print(newcryptograph)
        else:
            newcryptograph.show()
    elif num == 2:
        print("可选择的攻击模式：\n1.椒盐噪声攻击\n2.旋转攻击\n0.退出程序")
        while 1 == 1:
            number = int(input("请选择攻击模式："))
            if number > 2:
                print("选择超出范围！请重新选择...")
            elif number == 0:
                print("程序退出...")
                exit()
        if number == 1:
            # 添加椒盐噪声
            print("1. 添加椒盐噪声，可选比例如下:\n0.9 0.7 0.5 0.3")
            while 1 == 1:
                snr = float(input(("请选择椒盐噪声的比例：")))
                if snr > 0.9 or snr < 0.3:
                    print("输入非法！请重新输入")
                else:
                    break
            attack_img = add_salt_pepper(np.array(cImg), snr)
            attack_img = Image.fromarray(attack_img)
            attack_img.show()
        elif number == 2:
            # 旋转攻击
            print("将图像矩阵转置后提取密文")
            attack_img = cImg.transpose(Image.ROTATE_180)
            attack_img.show()

        # 被攻击的载体解密
        newcryptograph = decryption(attack_img, keys)
        # 识别隐写类型并输出提取后的密文
        if keys[5] == 4:
            print(newcryptograph)
        else:
            newcryptograph.show()
