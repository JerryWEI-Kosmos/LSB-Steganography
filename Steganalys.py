from PIL import Image
import numpy as np
import os
import sys

def openimage():
    # 需要隐写分析的图像保存路径
    path = "./data/saveImage/"
    imgs = os.listdir(path)
    for img in imgs:
        print("1.{}".format(img))
    print("请选择要隐写分析的图片(退出请输入0)")
    while 1==1:
        num = int(input("图片编号："))
        if num == 0:
            print("程序退出...")
            exit()
        elif num >len(imgs):
            print("输入超出范围！请重新选择")
            continue
        else:
            img = Image.open(path+imgs[num-1]).convert("RGB")
            imgArray = np.array(img)
            return imgArray


# 位平面分解函数
def bit_plane_decomposition(img):
    r,g,b = img.split()
    img_array_r = np.array(r,dtype="uint8")
    img_array_g = np.array(g,dtype="uint8")
    img_array_b = np.array(b,dtype="uint8")
    h,w = img_array_r.shape
    size = h*w
    # 定义三个矩阵进行位平面保存
    r_bit = np.zeros((h,w),dtype="uint8")
    g_bit = np.zeros((h,w),dtype="uint8")
    b_bit = np.zeros((h,w),dtype="uint8")
    # 提取R、G、B三通道的最低位平面
    print("正在分解R通道位平面")
    m = 0
    for i in range(h):
        for j in range(w):
            # 提取R通道的最低位平面
            if img_array_r[i][j]%2 == 0:
                r_bit[i][j] = 0
            else:
                r_bit[i][j] = 255
            m = m + 1
            sys.stdout.write(("\r当前完成 :{0}/" + str(size)).format(m))
            sys.stdout.flush()
    print("\n已完成R通道位平面分解\n")
    print("正在分解G通道位平面")
    m = 0
    for i in range(h):
        for j in range(w):
            # 提取G通道的最低位平面
            if img_array_g[i][j]%2 == 0:
                r_bit[i][j] = 0
            else:
                r_bit[i][j] = 255
            m = m + 1
            sys.stdout.write(("\r当前完成 :{0}/" + str(size)).format(m))
            sys.stdout.flush()
    print("\n已完成G通道位平面分解\n")
    print("正在分解B通道位平面")
    m = 0
    for i in range(h):
        for j in range(w):
            # 提取B通道的最低位平面
            if img_array_b[i][j]%2 == 0:
                r_bit[i][j] = 0
            else:
                r_bit[i][j] = 255
            m = m + 1
            sys.stdout.write(("\r当前完成 :{0}/" + str(size)).format(m))
            sys.stdout.flush()
    print("已完成B通道位平面分解\n")
    print("即将输出结果...")
    # 展示位平面分解结果
    r_bit_plane = Image.fromarray(r_bit)
    g_bit_plane = Image.fromarray(g_bit)
    b_bit_plane = Image.fromarray(b_bit)
    r_bit_plane.show()
    g_bit_plane.show()
    b_bit_plane.show()
# 卡方隐写分析算法

# RS隐写分析算法

if __name__ == '__main__':
    img = openimage()
    print("请选择隐写分析方法\n1.位平面分解\n2.卡方隐写分析\n3.RS隐写分析\n0.退出程序")
    while 1 == 1:
        num = int(input("请选择："))
        if num == 0:
            print("程序退出...")
            exit()
        elif num > 3:
            print("选择超出范围！请重新选择...")
            continue
        elif num == 1:
            bit_plane_decomposition(img)
            break
        elif num == 2:
            break
        elif num == 3:
            break
