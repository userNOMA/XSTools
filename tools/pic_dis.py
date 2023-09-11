import random
import sys

import cv2
import os
import numpy as np


# 遍历文件夹内的文件
def recursive_files_walk(path):
    paths = os.walk(path)
    for path_all, dir_lst, file_lst in paths:
        return path_all, file_lst


def dis_pic(path, s_num=1):
    print(path)
    f_path, file_name = recursive_files_walk(path)
    for file in file_name:
        path = f_path + '\\' + file
        path_a = f_path + '\\' + str(s_num) + '_A.png'
        path_b = f_path + '\\' + str(s_num) + '_B.png'
        inf = f'''删除：{file}
调整分辨率后：{str(s_num) + '_A.png'}    {str(s_num) + '_B.png'}'''
        print(inf)
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
        f1 = random.uniform(0.5, 1.5)
        ime_a = cv2.resize(img, None, fx=f1, fy=f1)
        f2 = random.uniform(0.5, 1.5)
        ime_b = cv2.resize(img, None, fx=f2, fy=f2)
        cv2.imencode('.png', ime_a)[1].tofile(path_a)
        cv2.imencode('.png', ime_b)[1].tofile(path_b)
        s_num += 1
        os.remove(path)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        pass
    else:
        sys.argv.append(r'D:\Formal\20230810相似图片200组\调分辨率')
        # sys.argv.append(os.getcwd())
    inf = f'''执行的路径为：
{sys.argv[1]}
是否执行？'''
    print(inf)
    inp = input("请输入：Y/y确认\n")
    if inp == 'Y' or inp == 'y':
        dis_pic(sys.argv[1])
    else:
        print(f'未确认，退出运行！')