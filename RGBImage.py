import os
import re

import numpy as np
from PIL import Image

# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)

# 将RGB图像转换为01矩阵
def ImageToBit(img):
    height,width,channel = img.shape
    string = ""
    for c in range(channel-1):
        for i in range(height):
            for j in range(width):
                string = string + "" + plus(bin(img[i][j][c]).replace('0b',''))
    list = re.findall(r'.{1}',string)
    listLen = len(list)
    width = width*8
    # 初始化bit矩阵
    bitArray = np.zeros((height, width,channel))
    n = 0
    # 将列表中的bit按位写入矩阵
    for c in range(channel-1):
        for i in range(height):
            for j in range(width):
                bitArray[i][j][c] = int(list[n])
                n = n + 1
    return bitArray

# 选择密文图像
def OpenImage():
    # 打开相对路径下的密文文件夹
    Path = ".\data\cryptographs\images\\"
    ImageList = os.listdir(Path)
    print("密文文件下有如下内容：(打开为nArray)")
    n = 1
    for ImagePath in ImageList:
        Img = Image.open(".\data\cryptographs\images\\"+ImagePath)
        # 将密文转换为Tensor
        ImgTensor = np.array(Img)
        # 获取密文图像的通道数、高度、宽度
        H , W , C= ImgTensor.shape
        print("{}.文件名：{} 高：{} 宽：{} 通道：{}".format(n,ImagePath,H,W,C))
        n = n + 1
    print("选择需要打开的密文（退出选择输入0）")
    while 1==1:
        num = int(input("请输入密文编号:"))
        if num == 0:
            print("已退出选择")
            break
        # 判断输入是否合法
        elif num in range(1,len(ImageList)+1):
            CryptographsImage = Image.open(Path+ImageList[num-1])
            CryptographsImage = CryptographsImage.convert("RGB")
            CryptographsArray = ImageToBit(np.array(CryptographsImage))
            print("选择图像为:{}".format(ImageList[num-1]))
            return CryptographsArray
        else:
            print("输入编号超出范围！")
