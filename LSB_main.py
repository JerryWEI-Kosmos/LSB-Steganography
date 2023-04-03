from random import *

from BinaryImage import *
from RGBImage import *
from Txt import *
import math
import numpy as np
import os
import sys
from PIL import Image


# 打开载体图像
def OpenCarrier():
    Path = ".\data\carriers\\"
    CarrierList = os.listdir(".\data\carriers")
    print("载体文件如下：(打开为nArray)")
    for i in range(0, len(CarrierList)):
        width = Image.open(".\data\carriers\\" + CarrierList[i]).width
        height = Image.open(".\data\carriers\\" + CarrierList[i]).height
        print(str(i+1) + "." + CarrierList[i] + " " + str(width) + "*" + str(height))
    while 1==1:
        num = int(input("请选择密文载体图像(输入序号)："))
        if num == 0:
            print("未选择载体信息！退出隐写")
            exit()
        # 判断输入是否合法
        elif num in range(1,len(CarrierList)+1):
            # 打开选中的图像
            carrier = Image.open(Path+CarrierList[num-1])
            # 将图像转换为三通道RGB图像
            carrierArray = np.array(carrier.convert("RGB"))
            # 获取当前图像的高宽信息
            H,W,C = carrierArray.shape
            print("选择图像为:{}\n".format(CarrierList[num-1]))
            return carrierArray
        else:
            print("输入编号超出范围！")
    return False

# 密钥生成算法
def CreatKey(carrier,cryptograph):
    maxH,maxW,maxC = carrier.shape
    H,W,C = cryptograph.shape
    size = maxH*maxW
    maxX = maxW-W
    maxY = maxH-H
    keys = []
    if C ==1:
        if size > (H * W):
            keys.append(randint(0, maxX))
            keys.append(randint(0, maxY))
            keys.append(randint(0,C-1))
            keys.append(int(H))
            keys.append(int(W))
        elif size == (H * W):
            keys.append(int(0))
            keys.append(int(0))
            keys.append(randint(0, C - 1))
            keys.append(int(maxH))
            keys.append(int(maxW))
    if C == 3:
        if size > (H * W):
            keys.append(randint(0, maxX))
            keys.append(randint(0, maxY))
            keys.append(int(-1))
            keys.append(int(H))
            keys.append(int(W))
        elif size == (H * W):
            keys.append(int(0))
            keys.append(int(0))
            keys.append(int(-1))
            keys.append(int(maxH))
            keys.append(int(maxW))
    return keys
# LSB隐写
def Steganographt(carrier,cryptograph,keys):
    if keys[2]==-1:
        x = keys[0]
        y = keys[1]
        for c in range(2):
            for i in range(keys[3]):
                for j in range(keys[4]):
                    carrier[i + y][j + x][c] = (carrier[i + y][j + x][c] - (carrier[i + y][j + x][c] % 2)) + int(
                        cryptograph[i][j][c])
    else:
        x = keys[0]
        y = keys[1]
        c = keys[2]
        for i in range(keys[3]):
            for j in range(keys[4]):
                result = (carrier[i+y][j+x][c]-(carrier[i+y][j+x][c]%2))+int(cryptograph[i][j])
                carrier[i+y][j+x][c] = result
    return carrier

def plus(string):
    return string.zfill(8)

# 提取密文
def GetCryptograph(carrier,keys):
    carrier = carrier.crop(keys[0],keys[1],keys[0]+keys[4],keys[0]+keys[3])
    if keys[2]==-1:
        exit()
    else:
        cryptographString = ""
        for i in range(keys[3]):
            for j in range(keys[4]):
                cryptographString =cryptographString+ ""+str(carrier[i][j]%2)
        cryptograph = toBit()
        cryptographImage = Image.fromarray(cryptograph)

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
def OpenCryptograph():
    print("可选择如下隐写内容：")
    print("1.二值图隐写\n2.RGB隐写\n3.文本隐写\n0.退出隐写")
    num = int(input("请输入编号："))
    if num == 1:
        return OpenBinaryImage()
    elif num == 2:
        return OpenImage()
    elif num == 3:
        return OpenTxt()
    elif num == 0:
        exit()

if __name__ == '__main__':
    carrier = OpenCarrier()
    cryptograph = OpenCryptograph()
    keys = CreatKey(carrier,cryptograph)
    print("密钥为：{}".format(keys))
    cImg = Steganographt(carrier,cryptograph,keys)
    cImg = Image.fromarray(cImg)
    carrier = Image.fromarray(carrier)
    cImg.show()

    PSNR = psnr(cImg,carrier)
    print("峰值信噪比 PSNR=%.1f dB" % (PSNR))