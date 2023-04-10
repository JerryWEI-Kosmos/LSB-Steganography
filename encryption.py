from random import randint


# 密钥生成算法
def creat_key(carrier, cryptograph, flag):
    # 获取可隐写的最大范围
    max_h, max_w, max_c = carrier.shape
    # 获取密文的尺寸
    h, w, c = cryptograph.shape
    # 获取密文的隐写大小
    size = max_h * max_w
    # 判断是否超出隐写范围
    if size > max_w * max_h:
        print("超出最大隐写容量！请重新选择载体图像或更改密文大小")
        return -1
    # 获取隐写的起点范围
    max_x = max_w - w
    max_y = max_h - h
    # 格式化密钥
    keys = []
    if c == 1:
        if size > (h * w):
            keys.append(randint(0, max_x))
            keys.append(randint(0, max_y))
            keys.append(randint(0, c - 1))
            keys.append(int(h))
            keys.append(int(w))
        elif size == (h * w):
            keys.append(int(0))
            keys.append(int(0))
            keys.append(randint(0, c - 1))
            keys.append(int(max_h))
            keys.append(int(max_w))
    if c == 3:
        if size > (h * w):
            keys.append(randint(0, max_x))
            keys.append(randint(0, max_y))
            keys.append(int(-1))
            keys.append(int(h))
            keys.append(int(w))
        elif size == (h * w):
            keys.append(int(0))
            keys.append(int(0))
            keys.append(int(-1))
            keys.append(int(max_h))
            keys.append(int(max_w))
    keys.append(flag)
    return keys


# LSB隐写
def steganography(carrier, cryptograph, keys):
    if keys[2] == -1:
        x = keys[0]
        y = keys[1]
        for c in range(2):
            for i in range(keys[3]):
                for j in range(keys[4]):
                    # carrier[i + y][j + x][c] = (carrier[i + y][j + x][c] - (carrier[i + y][j + x][c] % 2)) + int(
                    #     cryptograph[i][j][c])
                    if carrier[i + y][j + x][c] % 2 == cryptograph[i][j][c]:
                        continue
                    else:
                        carrier[i + y][j + x][c] = (carrier[i + y][j + x][c] - (carrier[i + y][j + x][c] % 2)) + int(
                            cryptograph[i][j][c])
    else:
        x = keys[0]
        y = keys[1]
        c = keys[2]
        if keys[5] == 1 or keys[5] == 4:
            for i in range(keys[3]):
                for j in range(keys[4]):
                    result = (carrier[i + y][j + x][c] - (carrier[i + y][j + x][c] % 2)) + int(cryptograph[i][j])
                    carrier[i + y][j + x][c] = result
        elif keys[5] == 3:
            for i in range(keys[3]):
                for j in range(keys[4]):
                    if carrier[i + y][j + x][c] % 2 == cryptograph[i][j][c]:
                        continue
                    else:
                        carrier[i + y][j + x][c] = (carrier[i + y][j + x][c] - (carrier[i + y][j + x][c] % 2)) + int(
                            cryptograph[i][j][c])
    return carrier
