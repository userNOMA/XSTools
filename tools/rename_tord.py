import os
import re
import sys


# 遍历文件夹内的文件
def recursive_files_walk(path):
    paths = os.walk(path)
    for path_all, dir_lst, file_lst in paths:
        return path_all, file_lst


# 重命名
def join_path_rename(f_path, name_old, name_new):
    os.rename(f_path + '\\' + name_old, f_path + '\\' + name_new)


# 把按严格升序命名的文件重命名为两个一组
def rename_t(path, s_name=1):
    f_path, file_name = recursive_files_walk(path)
    for x in range(0, len(file_name), 2):
        file_name_bf = re.split(r'\.', file_name[x])[-1]
        file_name_en = re.split(r'\.', file_name[x + 1])[-1]
        file_name_a = str(int(s_name+x/2)) + r'_A.' + file_name_bf
        file_name_b = str(int(s_name+x/2)) + r'_B.' + file_name_en
        print(file_name[x] + '   --->   ' + file_name_a)
        print(file_name[x + 1] + '   --->   ' + file_name_b)
        join_path_rename(f_path, file_name[x], file_name_a)
        join_path_rename(f_path, file_name[x + 1], file_name_b)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        pass
    else:
        sys.argv.append(os.getcwd())
    inf = f'''执行的路径为：
{sys.argv[1]}
是否执行？'''
    print(inf)
    inp = input("请输入：Y/y确认\n")
    if inp == 'Y' or inp == 'y':
        rename_t(sys.argv[1])
    else:
        print(f'未确认，退出运行！')


