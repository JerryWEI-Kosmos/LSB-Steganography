from PIL import Image
import numpy as np
import os
import sys
import matplotlib.pyplot as plt


def open_c_image():
    # 需要隐写分析的图像保存路径
    path = "data/steganalysis/steganographic_result/"
    images = os.listdir(path)
    i = 1
    for image in images:
        print("{}.{}".format(i, image))
        i = i + 1
    print("请选择要隐写分析的图片(退出请输入0)")
    while 1 == 1:
        number = int(input("图片编号："))
        if number == 0:
            print("程序退出...")
            exit()
        elif number > len(images):
            print("输入超出范围！请重新选择")
            continue
        else:
            image = Image.open(path + images[number - 1]).convert("RGB")
            return image


def open_o_image():
    # 原图保存路径
    o_path = "data/steganalysis/original_images/"
    o_images = os.listdir(o_path)
    i = 1
    for image in o_images:
        print("{}.{}".format(i, image))
        i = i + 1
    print("请选择隐写分析的原图(退出请输入0)")
    while 1 == 1:
        number = int(input("图片编号："))
        if number == 0:
            print("程序退出...")
            exit()
        elif number > len(o_images):
            print("输入超出范围！请重新选择")
            continue
        else:
            image = Image.open(o_path + o_images[number - 1]).convert("RGB")
            return image


# 位平面分解函数
def bit_plane_decomposition(image):
    b, g, r = image.split()
    b = b.convert("L")
    g = g.convert("L")
    r = r.convert("L")
    img_array_b = np.array(b)
    img_array_g = np.array(g)
    img_array_r = np.array(r)
    h, w = img_array_r.shape
    size = h * w
    # 定义三个矩阵进行位平面保存
    b_bit = np.zeros((h, w), dtype='bool')
    g_bit = np.zeros((h, w), dtype='bool')
    r_bit = np.zeros((h, w), dtype='bool')
    # 提取R、G、B三通道的最低位平面
    print("正在分解R通道位平面")
    m = 0
    for i in range(h):
        for j in range(w):
            # 提取R通道的最低位平面
            if img_array_r[i][j] % 2 == 0:
                r_bit[i][j] = False
            else:
                r_bit[i][j] = True
            m = m + 1
            sys.stdout.write(("\r当前完成 :{0}/" + str(size)).format(m))
            sys.stdout.flush()
    print("\n已完成R通道位平面分解\n")
    print("正在分解G通道位平面")
    m = 0
    for i in range(h):
        for j in range(w):
            # 提取G通道的最低位平面
            if img_array_g[i][j] % 2 == 0:
                g_bit[i][j] = False
            else:
                g_bit[i][j] = True
            m = m + 1
            sys.stdout.write(("\r当前完成 :{0}/" + str(size)).format(m))
            sys.stdout.flush()
    print("\n已完成G通道位平面分解\n")
    print("正在分解B通道位平面")
    m = 0
    for i in range(h):
        for j in range(w):
            # 提取B通道的最低位平面
            if img_array_b[i][j] % 2 == 0:
                b_bit[i][j] = False
            else:
                b_bit[i][j] = True
            m = m + 1
            sys.stdout.write(("\r当前完成 :{0}/" + str(size)).format(m))
            sys.stdout.flush()
    print("\n已完成B通道位平面分解")
    print("即将输出结果...")
    # 展示位平面分解结果
    r_bit_plane = Image.fromarray(r_bit)
    g_bit_plane = Image.fromarray(g_bit)
    b_bit_plane = Image.fromarray(b_bit)

    plt.rcParams['figure.figsize'] = (7.2, 12.8)
    plt.subplot(311)
    plt.imshow(b_bit_plane)
    plt.axis()
    plt.subplot(312)
    plt.imshow(g_bit_plane)
    plt.axis()
    plt.subplot(313)
    plt.imshow(r_bit_plane)
    plt.axis()
    plt.show()
    # r_bit_plane.show()
    # g_bit_plane.show()
    # b_bit_plane.show()


# 卡方隐写分析算法

# RS隐写分析算法
def rs_analysis(image):
    # 定义判断函数
    def is_odd(number):
        if number % 2 == 0:
            return False
        else:
            return True

    # 定义变量
    p = [0] * 256
    rs_number = 0
    a = np.zeros((8, 8))

    # 统计像素值出现次数
    for i in range(len(image)):
        for j in range(len(image[0])):
            p[image[i][j]] += 1

    # 计算RS值
    for i in range(len(image)):
        for j in range(len(image[0])):
            rs_number += p[image[i][j]]
            if is_odd(i + j):
                a[i % 8][j % 8] += 1

    # 计算嵌入强度
    alpha = rs_number / (len(image) * len(image[0]) * 256)

    # 计算RS分析结果
    result = (a[0][0] + a[0][1] + a[1][0] + a[1][1]) / (alpha * (len(image) * len(image[0]) / 64))

    return result


def rs(image):
    # 将灰度图像分成3个通道
    b, g, r = image.split()
    b = np.array(b)
    g = np.array(g)
    r = np.array(r)

    rs_b = rs_analysis(b)
    rs_g = rs_analysis(g)
    rs_r = rs_analysis(r)

    result = np.mean([rs_b, rs_g, rs_r])

    return result
    # 输出结果
    # print("B通道RS分析结果：", rs_b)
    # print("G通道RS分析结果：", rs_g)
    # print("R通道RS分析结果：", rs_r)


def kafang(image):
    b, g, r = image.split()
    b = np.array(b)
    g = np.array(g)
    r = np.array(r)

    # 计算直方图
    b_hist, _ = np.histogram(b, bins=256)
    g_hist, _ = np.histogram(g, bins=256)
    r_hist, _ = np.histogram(r, bins=256)

    # 计算卡方值
    def chi_square(observed, expected):
        return np.sum((observed - expected) ** 2 / expected)

    b_expected = np.sum(b_hist) / 256
    g_expected = np.sum(g_hist) / 256
    r_expected = np.sum(r_hist) / 256

    b_chi_square = chi_square(b_hist, b_expected)
    g_chi_square = chi_square(g_hist, g_expected)
    r_chi_square = chi_square(r_hist, r_expected)

    print("R通道卡方值：", r_chi_square)
    print("G通道卡方值：", g_chi_square)
    print("B通道卡方值：", b_chi_square)

    result = np.mean([b_chi_square, g_chi_square, r_chi_square])

    return result


if __name__ == '__main__':
    img = open_c_image()
    o_img = open_o_image()
    print("请选择隐写分析方法\n1.位平面分解\n2.卡方隐写分析\n3.RS隐写分析\n4.自动计算卡方值与RS\n0.退出程序")
    while 1 == 1:
        num = int(input("请选择："))
        if num == 0:
            print("程序退出...")
            exit()
        elif num > 4:
            print("选择超出范围！请重新选择...")
            continue
        elif num == 1:
            bit_plane_decomposition(img)
            break
        elif num == 2:
            o_kf = kafang(o_img)
            print("原图卡方值：{}".format(o_kf))
            kf = kafang(img)
            print("隐写图卡方值：{}".format(kf))
            print("差值：{}".format(o_kf - kf))
            break
        elif num == 3:
            o_rs = rs(o_img)
            print("原图RS分析结果：{}".format(o_rs))
            rs = rs(img)
            print("隐写图RS分析结果：{}".format(rs))
            print("差值：{}".format(o_rs - rs))
            break
        elif num == 4:
            o_kf = kafang(o_img)
            print("原图卡方值：{}".format(o_kf))
            kf = kafang(img)
            print("隐写图卡方值：{}".format(kf))
            print("差值：{}\n".format(o_kf - kf))
            o_rs = rs(o_img)
            print("原图RS分析结果：{}".format(o_rs))
            rs = rs(img)
            print("隐写图RS分析结果：{}".format(rs))
            print("差值：{}".format(o_rs - rs))
            break
