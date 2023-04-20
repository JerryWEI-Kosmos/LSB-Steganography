import cv2
from binary_image import *
from encryption import *
from decryption import *
from gray_image import *
from RGB_image import *
from attack import *
from PIL import Image
from txt import *
import numpy as np
import math
import os
import matplotlib.pyplot as plt


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
        image_number = int(input("请选择密文载体图像(输入序号)："))
        if image_number == 0:
            print("未选择载体信息！退出隐写")
            exit()
        # 判断输入是否合法
        elif image_number in range(1, len(carrier_list) + 1):
            # 打开选中的图像
            carrier_open = Image.open(path + carrier_list[image_number - 1])
            # 将图像转换为三通道RGB图像
            carrier_array = np.array(carrier_open.convert("RGB"))
            # 获取当前图像的高宽信息
            h, w, c = carrier_array.shape
            print("选择图像为:{} {}*{} {}通道\n".format(carrier_list[image_number - 1], h, w, c))
            return carrier_array
        else:
            print("输入编号超出范围！")


# 性能计算
# 计算峰值信息量
def psnr(img_1, img_2):
    # 将要计算的图像打开成nArray矩阵
    img_1_b, img_1_g, img_1_r = img_1.split()
    img_1_b = np.array(img_1_b.convert("L"))
    img_1_g = np.array(img_1_g.convert("L"))
    img_1_r = np.array(img_1_r.convert("L"))

    img_2_b, img_2_g, img_2_r = img_2.split()
    img_2_b = np.array(img_2_b.convert("L"))
    img_2_g = np.array(img_2_g.convert("L"))
    img_2_r = np.array(img_2_r.convert("L"))
    # 计算差错平均值
    mse_1 = np.mean((img_1_b / 1.0 - img_2_b / 1.0) ** 2)
    mse_2 = np.mean((img_1_g / 1.0 - img_2_g / 1.0) ** 2)
    mse_3 = np.mean((img_1_r / 1.0 - img_2_r / 1.0) ** 2)

    mse = np.mean([mse_3, mse_2, mse_1])
    if mse < 1.0e-10:
        return 100
    # 返回峰值信噪比
    return 10 * math.log10(255.0 ** 2 / mse)


# SSIM
def ssim_2(img1, img2):
    """Calculate SSIM (structural similarity) for one channel images.
    It is called by func:`calculate_ssim`.
    Args:
        img1 (ndarray): Images with range [0, 255] with order 'HWC'.
        img2 (ndarray): Images with range [0, 255] with order 'HWC'.
    Returns:
        float: ssim result.
    """
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2
    # 公式二计算
    ssim_map = ((2 * mu1_mu2 + c1) *
                (2 * sigma12 + c2)) / ((mu1_sq + mu2_sq + c1) *
                                       (sigma1_sq + sigma2_sq + c2))
    return ssim_map.mean()


# 选择要隐写的内容
def open_cryptograph():
    print("可选择如下隐写内容：")
    print("1.二值图隐写\n2.RGB隐写\n3.灰度图隐写\n4.文本隐写\n0.退出隐写")
    cryptograph_number = int(input("请输入编号："))
    if cryptograph_number == 1:
        return open_binary_image(), 1
    elif cryptograph_number == 2:
        return open_image(), 2
    elif cryptograph_number == 3:
        return open_gray_image(), 3
    elif cryptograph_number == 4:
        return open_txt(), 4
    elif cryptograph_number == 0:
        exit()


# 选择是否保存照片
def save(img):
    path = "data/steganalysis/steganographic_result/"
    images = os.listdir(path)
    index = len(images)
    while 1 == 1:
        save_flag = input("是否需要保存当前隐写图像？(yes/no):")
        if save_flag in ["yes", "y", "Y", "YES"]:
            img.save(path + "saveImages{}.jpg".format(index + 1))
            break
        elif save_flag in ["no", 'n', "No", "NO"]:
            print("图像未保存")
            break


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
    # 计算隐写性能
    SSIM = ssim_2(cImg, carrier)
    print("结构相似性 SSIM=%.1f" % SSIM)
    # 将隐写前后的图像从矩阵还原并输出载体图像和隐写后的载体图像
    carrier = Image.fromarray(carrier)
    cImg = Image.fromarray(cImg)
    # 计算峰值信噪比
    PSNR = psnr(cImg, carrier)
    print("峰值信噪比 PSNR=%.1f dB" % PSNR)
    # 选择是否保存图片
    save(cImg)
    if num == 1:
        # 从载体图像中提取密文
        new_cryptograph = decryption(cImg, keys)
        # 识别隐写类型并输出提取后的密文
        if keys[5] == 4:
            print(new_cryptograph)
        else:
            # 使用matplotlib输出图像
            plt.rcParams['figure.figsize'] = (12.8, 7.2)
            plt.subplot(111)
            plt.imshow(new_cryptograph)
            plt.axis()
            plt.show()
            # new_cryptograph.show()
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
                    snr = float(input("请选择椒盐噪声的比例："))
                    if snr > 0.9 or snr < 0.3:
                        print("输入非法！请重新输入")
                    else:
                        break
                attack_img = add_salt_pepper(np.array(cImg), snr)
                attack_img = Image.fromarray(attack_img)
                attack_img.show()
                break
            elif number == 2:
                # 旋转攻击
                print("将图像矩阵转置后提取密文")
                attack_img = cImg.transpose(Image.ROTATE_180)
                attack_img.show()
                break

        # 被攻击的载体解密
        new_cryptograph = decryption(attack_img, keys)
        # 识别隐写类型并输出提取后的密文
        if keys[5] == 4:
            print(new_cryptograph)
        else:
            new_cryptograph.show()
