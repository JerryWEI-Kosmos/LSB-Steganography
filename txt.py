import os
import re
import numpy as np


# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)


# 将文本密文转化为bit矩阵
def to_bit_array(ciphertext):
    string = ""
    for i in range(len(ciphertext)):
        string = string + "" + plus(bin(ord(ciphertext[i])).replace('0b', ''))
    word_list = re.findall(r'.{1}', string)
    list_len = len(word_list)
    width = list_len
    height = 1
    n = 0
    # 规定矩阵行列
    while width % 2 == 0:
        if width == height:
            break
        n = n + 1
        width = int(width / 2)
        height = int(2 ** n)
    # 初始化bit矩阵
    bit_array = np.zeros((height, width))
    n = 0
    # 将列表中的bit按位写入矩阵
    for i in range(height):
        for j in range(width):
            bit_array[i][j] = word_list[n]
            n = n + 1
    return bit_array


# 打开文本密文 输出一个nArray对象
def open_txt():
    # 打开相对路径下的密文文件夹
    path = "data/cryptograph/txt/"
    txt_list = os.listdir(path)
    print("密文文件下有如下内容：(打开为nArray)")
    n = 1
    # 将可选择的文件输出到控制台
    for txt in txt_list:
        print("{}.".format(n) + txt)
        n = n + 1
    print("选择需要打开的密文（退出输入0）")
    while 1 == 1:
        num = int(input("请输入密文编号:"))
        if num == 0:
            print("已退出选择")
            break
        # 判断输入是否合法
        elif num in range(1, len(txt_list) + 1):
            # 打开选中的txt文件
            txt = open(path + txt_list[num - 1])
            ciphertext = ""
            ciphertext_list = []
            for word in txt.read():
                word = word.strip("\n")
                ciphertext_list.append(word)
            ciphertext = "".join(word for word in ciphertext_list if word.isalnum())
            ciphertext = list(ciphertext)
            txt_array = to_bit_array(ciphertext)
            n, m = txt_array.shape
            txt_array = np.reshape(txt_array, (n, m, 1))
            print("选择文本为:{}".format(txt_list[num - 1]))
            return txt_array
        else:
            print("输入编号超出范围！")
