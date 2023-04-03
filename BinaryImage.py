import os
import numpy as np
from PIL import Image

# 选择密文图像 返回一个nArray对象
def OpenBinaryImage():
    # 打开相对路径下的密文文件夹
    Path = ".\data\cryptographs\images\\"
    ImageList = os.listdir(Path)
    print("密文文件下有如下内容：(打开为二值nArray)")
    n = 1
    # 将可选择的文件输出到控制台
    for ImagePath in ImageList:
        Img = Image.open(".\data\cryptographs\images\\"+ImagePath)
        ImgArray = np.array(Img)
        # 获取密文图像的通道数、高度、宽度
        H , W ,C= ImgArray.shape
        print("{}.文件名：{} 高：{} 宽：{}".format(n,ImagePath,H,W))
        n = n + 1
    print("选择需要打开的密文（退出选择输入0）")
    while 1==1:
        num = int(input("请输入密文编号:"))
        if num == 0:
            print("已退出选择")
            break
        # 判断输入是否合法
        elif num in range(1,len(ImageList)+1):
            # 打开选中的图像
            CryptographsImage = Image.open(Path+ImageList[num-1])
            # 将图像转换为二值矩阵
            CryptographsArray = np.array(CryptographsImage.convert("1"))
            # 获取当前图像的高宽信息
            H,W = CryptographsArray.shape
            # 将nArray格式化为高、宽、通道格式
            CryptographsArray = np.reshape(CryptographsArray,(H,W,1))
            print("选择图像为:{}".format(ImageList[num-1]))
            return CryptographsArray
        else:
            print("输入编号超出范围！")

def DecodeImage(CryptographsArray):
    H , W = CryptographsArray.shape
    for j in range(H):
        for i in range(W):
            if CryptographsArray[i][j] == 0:
                continue
            else:
                CryptographsArray[i][j] = 255
    CryptographsImage = Image.fromarray(CryptographsArray)
    return CryptographsImage
