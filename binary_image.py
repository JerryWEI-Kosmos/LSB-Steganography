import os
from scramble import *


# 选择密文图像 返回一个nArray对象
def open_binary_image():
    # 打开相对路径下的密文文件夹
    path = "data/cryptograph/images/"
    image_list = os.listdir(path)
    print("密文文件下有如下内容：(打开为二值nArray)")
    n = 1
    # 将可选择的文件输出到控制台
    for image_path in image_list:
        img = Image.open(path + image_path)
        img_array = np.array(img)
        # 获取密文图像的通道数、高度、宽度
        h, w, c = img_array.shape
        print("{}.文件名：{} 高：{} 宽：{}".format(n, image_path, h, w))
        n = n + 1
    print("选择需要打开的密文（退出输入0）")
    while 1 == 1:
        num = int(input("请输入密文编号:"))
        if num == 0:
            print("已退出选择")
            break
        # 判断输入是否合法
        elif num in range(1, len(image_list) + 1):
            # 打开选中的图像
            cryptograph_image = Image.open(path + image_list[num - 1])
            # 将图像转换为二值矩阵
            cryptograph_image = cryptograph_image.convert("1")
            # # 将图片进行logistic置乱
            # cryptograph_image = logistic_binary_img(cryptograph_image)
            cryptograph_array = np.array(cryptograph_image)
            # 获取当前图像的高宽信息
            h, w = cryptograph_array.shape
            # 将nArray格式化为高、宽、通道格式
            cryptograph_array = np.reshape(cryptograph_array, (h, w, 1))
            print("选择图像为:{}".format(image_list[num - 1]))
            # 返回经过logistic变换的图
            return cryptograph_array
        else:
            print("输入编号超出范围！")


# 无选择打开二值图
def open_binary_images(path):
    # 打开选中的图像
    cryptograph_image = Image.open(path).resize((32, 256))
    # 将图像转换为二值矩阵
    cryptograph_image = cryptograph_image.convert("1")
    # # 将图片进行logistic置乱
    # cryptograph_image = logistic_binary_img(cryptograph_image)
    cryptograph_array = np.array(cryptograph_image)
    # 获取当前图像的高宽信息
    h, w = cryptograph_array.shape
    # 将nArray格式化为高、宽、通道格式
    cryptograph_array = np.reshape(cryptograph_array, (h, w, 1))
    return cryptograph_array
