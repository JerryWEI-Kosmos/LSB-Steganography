import numpy as np


# 椒盐噪声
def add_salt_pepper(img, SNR):
    img_ = img.copy()
    c, h, w = img_.shape
    mask = np.random.choice((0, 1, 2), size=(1, h, w), p=[SNR, (1 - SNR) / 2., (1 - SNR) / 2.])
    mask = np.repeat(mask, c, axis=0)  # 按channel 复制到 与img具有相同的shape
    img_[mask == 1] = 255  # 盐噪声
    img_[mask == 2] = 0  # 椒噪声
    return img_


# 高斯噪声
def gasuss_noise(image, mu=0.0, sigma=0.1):
    """
     添加高斯噪声
    :param image: 输入的图像
    :param mu: 均值
    :param sigma: 标准差
    :return: 含有高斯噪声的图像
    """
    image = np.array(image,dtype="float")
    noise = np.random.normal(mu, sigma, image.shape)
    gauss_noise = image + noise
    if gauss_noise.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    gauss_noise = np.clip(gauss_noise, low_clip, 1.0)
    gauss_noise = np.uint8(gauss_noise * 255)
    return gauss_noise