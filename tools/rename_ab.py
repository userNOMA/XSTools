import os
import re


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
    zxs_print.print('\n'.join(files))


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


# 判断文件路径是不是我要的路径
def need_file(path):
    return False if re.search(r'\\[0-9]+(_A|_B| \(1\)| \(2\))\.', path) is None else True


# 获取文件编号
def get_num(path):
    return re.search(r'\\[0-9]+[ _]', path).group()[1:-1]


# 判断文件类型A/B
def is_ab(path):
    if re.search(r' \(1\)\.', path) is not None:
        return '_A.'
    elif re.search(r' \(2\)\.', path) is not None:
        return '_B.'
    else:
        return ''


# 仅负责更名从(1)到A
def rename(path):
    path_new = re.sub(r' \([12]\)\.', is_ab(path), path)
    os.rename(path, path_new)
    print(path, '  >>>>>  ', path_new)
    return path_new


# 仅负责更名从12 (1)到num_A
def rename_c(path, num, tail):
    path_new = re.sub(r'\\[0-9]+.*\.', r'\\' + num + tail, path)
    os.rename(path, path_new)
    print(path, '  >>>>>  ', path_new)
    return path_new


# 仅负责更名从12_A到num_A
def rename_d(path, ab, num):
    path_new = re.sub(r'\\[0-9]+_[AB].', r'\\' + str(num) + ab, path)
    os.rename(path, path_new)
    print(path, '  >>>>>  ', path_new)


# 遍历重命名文件：
# xxx (1).xx->xxx_A.xx
# xxx (2).xx->xxx_B.xx
# 从以下几个方面改进：
# 1.处理修改后文件名冲突的情况
# 2.处理修改后中间少一项编号的情况（进行重新编号）
def rename_ab1(path):
    # 获取所有当前路径下的文件
    all_files, need_files, dont_need = [], [], []
    recursive_files_scandir(path, all_files)
    zxs_print.print(all_files)
    # 第一次遍历，得到需要的文件路径
    for file in all_files:
        if need_file(file):
            need_files.append(file)
        else:
            dont_need.append(file)
    zxs_print.print(f'''1.1符合要求的文件共计 {len(need_files)} 条,''', pri=1)
    zxs_print.print('\n'.join(need_files), pri=0)
    zxs_print.print(f'''   不符合要求的文件共计 {len(dont_need)} 条，
   具体路径为：''', pri=1)
    zxs_print.print('\n'.join(dont_need), pri=1)
    inp = input("是否确认继续：Y/y确认\n")
    if inp != 'Y' and inp != 'y':
        return
    # 第二次遍历，更名，得到重复的文件路径
    zxs_print.print('2.重命名：', pri=1)
    exit_num, rep_files, deal = {}, [], {int: list}
    for file in need_files:
        num = int(get_num(file))
        exit_num[num] = exit_num.setdefault(num, 0) + 1
        if exit_num[num] > 2:
            rep_files.append(file)
        else:
            try:
                file_new = rename(file)
                if exit_num[num] == 1:
                    deal[num] = ['', '']
                    deal[num][0] = file_new
                else:
                    deal[num][1] = file_new
            except FileExistsError:
                rep_files.append(file)
    zxs_print.print(rep_files)
    zxs_print.print('3.处理重复的文件路径：', pri=1)
    # 第三次循环，处理重复的文件路径,全部添加到末尾
    max_num = max(exit_num.keys())
    for file in rep_files:
        exit_num.setdefault(max_num + 1, 0)
        exit_num[max_num+1] += 1
        if exit_num[max_num+1] == 1:
            num = max(exit_num.keys())
            file_new = rename_c(file, str(num), '_A.')
            deal[num] = [file_new, '']
            file_new = rename_c(file, str(num), '_B.')
            deal[num][1] = file_new
            max_num += 1
    zxs_print.print('4.插空补缺：', pri=1)
    # 第四次循环，将末尾的填补到中间空缺的
    num_ord = sorted(set(exit_num.keys()))
    num_c = min(num_ord)
    real_len = max(num_ord) - min(num_ord) + 1
    zxs_print.print(num_ord)
    zxs_print.print(deal)
    zxs_print.print(exit_num)
    while 0 < len(num_ord) < real_len:
        num = min(num_ord)
        num_ord.remove(num)
        rename_d(deal[num][0], '_A.', num_c)
        rename_d(deal[num][1], '_B.', num_c)
        num_c += 1
    print('全部重命名成功！')


zxs_print.lev = 1
inf = f'''将批量更改该文件夹下的文件名：
{os.getcwd()}
效果如下：
33 (1).txt  >>>>>  33_A.txt
33 (2).txt  >>>>>  33_B.txt'''
zxs_print.print(inf, pri=9)
inp = input("请输入：Y/y确认\n")
if inp == 'Y' or inp == 'y':
    rename_ab1(r'D:\Learn\TestFiles\相似图片224组')
    # rename_ab1(os.getcwd())
else:
    zxs_print.print(f'未确认，退出运行！', pri=9)
