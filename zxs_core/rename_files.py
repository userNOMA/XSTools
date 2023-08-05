import os
import re
from tool_class import ZXSPrint

# 递归遍历所有子文件，暴力
# os.listdir(path)仅仅返回子文件夹和文件，所以需要遍历
def recursive_files_listdir(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            print(file)
        elif os.path.isdir(file_path):
            recursive_files_listdir(file_path)


# 双循环遍历所有子文件
# os.walk(top, topdown=True, onerror=None, followlinks=False)
def recursive_files_walk(path):
    paths = os.walk(path)
    for path_all, dir_lst, file_lst in paths:
        for file_name in file_lst:
            print(os.path.join(path_all, file_name))


# 递归遍历所有子文件
# os.walk(top, topdown=True, onerror=None, followlinks=False)
def recursive_files_scandir(paths, files=None):
    if files is None:
        files = []
    dirs = []
    for item in os.scandir(paths):
        if item.is_dir():
            dirs.append(item.path)
            recursive_files_scandir(dirs[-1], files)
        elif item.is_file():
            files.append(item.path)
    # print('\n'.join(files))


# 遍历重命名文件：
# xxx (1).xx->xxx_A.xx
# xxx (2).xx->xxx_B.xx
def rename_ab(path):
    all_files = []
    recursive_files_scandir(path, all_files)
    for file in all_files:
        file_a = re.sub(r' \(1\)\.', r'_A.', file)
        file_b = re.sub(r' \(2\)\.', r'_B.', file)
        if file_a != file:
            os.rename(file, file_a)
            print(file, '  >>>>>  ', file_a)
        elif file_b != file:
            os.rename(file, file_b)
            print(file, '  >>>>>  ', file_b)
    print('全部重命名成功！')


# rename_ab(os.getcwd())
print('aaa')
zxs_print = ZXSPrint()
zxs_print.lev = 1
zxs_print.print('aaaa0')
zxs_print.print('aaaa2', pri=2)
zxs_print.print('aaaa3', pri=3)

