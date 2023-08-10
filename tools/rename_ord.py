import os
import re
import sys


class ZXSPrint:
    lev = int

    def __init__(self, lev=0):
        self.lev = lev

    # pri：本次打印优先级，该数字大于整体打印优先级的时候才会打印
    def print(self, *objects, sep=' ', end='\n', file=None, flush=False, pri=0):
        if self.lev <= pri:
            print(*objects, sep=' ', end='\n', file=None, flush=False)
        else:
            pass


zxs_print = ZXSPrint()


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
    zxs_print.print('\n'.join(files), pri=-1)


# 判断文件路径是不是我要的路径
# 判断依据是：文件名中包含数字
def need_file(path):
    file = re.split(r'\\', path)[-1]
    return False if re.search(r'[0-9]+', file) is None else True


# 从文件路径中获取文件名中包含的数字
def path_file_num(path):
    return int(re.search(r'[0-9]+', re.split(r'\\', path)[-1]).group())


# 将名字中的数字递减
def rename_num(path, num_old, num_new):
    file = re.split(r'\\', path)[-1]
    path_pre = '\\'.join(re.split(r'\\', path)[0:-1])
    file_new = file.replace(str(num_old), str(num_new))
    path_new = path_pre + '\\' + file_new
    os.rename(path, path_new)
    zxs_print.print(file, file_new)
    zxs_print.print(path, path_new, num_old, num_new)
    print(path, '  >>>>>  ', path_new)


# 将所有按照序号命名的内容整体前移或者后移一个顺序：
# 12.xx->2.xx
# 13.xx->3.xx
def rename_ord(path, sta_num):
    # 获取所有当前路径下的文件
    all_files, need_files, ord_files = [], [], {}
    recursive_files_scandir(path, all_files)
    zxs_print.print(all_files)
    # 第一次遍历，得到需要的文件路径，并存储路径与序号的对应关系
    for file in all_files:
        if need_file(file):
            need_files.append(file)
            ord_files[file] = path_file_num(file)
    zxs_print.print('1.已找到符合要求的文件路径并排序', pri=1)
    zxs_print.print(need_files)
    min_num, max_num = min(ord_files.values()), max(ord_files.values())
    zxs_print.print(ord_files)
    zxs_print.print(sta_num, min_num)
    # 第二次遍历，按照排序后的顺序，把所有的文件名从小到大依次更改
    if sta_num < min_num:
        ord_files = sorted(ord_files.items(), key=lambda x: x[1])
        for file, num in ord_files:
            rename_num(file, num, num - min_num + sta_num)
    elif min_num < sta_num < max_num:
        rename_ord(path, 2*sta_num - min_num + 1)
        rename_ord(path, sta_num)
    else:
        ord_files = sorted(ord_files.items(), key=lambda x: x[1], reverse=True)
        for file, num in ord_files:
            rename_num(file, num, num + sta_num - min_num)
    print('全部重命名成功！')

if __name__ == '__main__':
    zxs_print.lev = 1
    inf = f'''将批量更改该文件夹下的文件名：
{sys.argv[1]}
把文件名中的数字整体偏移，效果如下：
33 (1)副本.txt  >>>>>  6 (1)副本.txt
33 (2).txt  >>>>>  6 (2).txt
35_A.txt  >>>>>  8_A.txt'''
    zxs_print.print(inf, pri=9)
    inp = input("请输入最小编号偏移后的对应值：\n")
    if inp.isdigit():
        rename_ord(sys.argv[1], int(inp))
    else:
        zxs_print.print(f'输入值不正确，退出运行！', pri=9)
