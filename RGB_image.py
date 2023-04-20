import os
import re
from scramble import *


# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)


# 将RGB图像转换为01矩阵
def image_to_bit(img):
    height, width, channel = img.shape
    string = ""
    for c in range(channel):
        for i in range(height):
            for j in range(width):
                string = string + "" + plus(bin(img[i][j][c]).replace('0b', ''))
    zero_one_list = re.findall(r'.{1}', string)
    width = width * 8
    # 初始化bit矩阵
    bit_array = np.zeros((height, width, channel))
    n = 0
    # 将列表中的bit按位写入矩阵
    for c in range(channel):
        for i in range(height):
            for j in range(width):
                bit_array[i][j][c] = int(zero_one_list[n])
                n = n + 1
    return bit_array


# 选择密文图像
def open_image():
    # 打开相对路径下的密文文件夹
    path = "./data/cryptograph/images/"
    image_list = os.listdir(path)
    print("密文文件下有如下内容：(打开为nArray)")
    n = 1
    for image_path in image_list:
        img = Image.open(path + image_path)
        # 将密文转换为nArray
        img_array = np.array(img)
        # 获取密文图像的通道数、高度、宽度
        h, w, c = img_array.shape
        print("{}.文件名：{} 高：{} 宽：{} 通道：{}".format(n, image_path, h, w, c))
        n = n + 1
    print("选择需要打开的密文（退出输入0）")
    while 1 == 1:
        num = int(input("请输入密文编号:"))
        if num == 0:
            print("已退出选择")
            break
        # 判断输入是否合法
        elif num in range(1, len(image_list) + 1):
            cryptograph_image = Image.open(path + image_list[num - 1])
            cryptograph_image = cryptograph_image.convert("RGB")
            # 将RGB图片进行logistic加密
            cryptograph_image = logistic_img(cryptograph_image)
            # cryptograph_image.show()
            cryptograph_array = image_to_bit(np.array(cryptograph_image))
            print("选择图像为:{}".format(image_list[num - 1]))
            return cryptograph_array
        else:
            print("输入编号超出范围！")
