import cv2
import numpy as np
from scipy import ssim


def calculate_ssim(image1, image2):
    # 将图像转换为灰度图
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 计算 SSIM
    ssim_score = ssim(gray_image1, gray_image2)

    return ssim_score


def calculate_mse(image1, image2):
    # 计算 MSE
    mse = np.mean((image1 - image2) ** 2)

    return mse


if __name__ == "__main__":
    image_path1 = r"D:\Learn\TestFiles\225_A.jpg"  # 替换为第一张图像的文件路径
    image_path2 = r"D:\Learn\TestFiles\225_B.jpg"  # 替换为第二张图像的文件路径

    # 读取图像
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # 计算 SSIM 和 MSE
    ssim_score = calculate_ssim(image1, image2)
    mse = calculate_mse(image1, image2)

    print(f"SSIM Score: {ssim_score}")
    print(f"MSE: {mse}")
