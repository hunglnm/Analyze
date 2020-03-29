import re
import os


def func_find():
    s_path = input('Nhap duong dan :')
    s_pattern = input('Nhap regex can tim:')
    f_log = open(s_path + '/result_search.log', 'w')

    for path, subdirs, files in os.walk(s_path):
        for name in files:
            print(name)
            if 'result_search.log' not in name:
                path_file = os.path.join(path, name)
                f_log.write(path_file + '\n')
                f = open(path_file, 'r')
                temp_cfg = f.read()
                f.close()
                i = 0
                for every_part in re.findall(s_pattern, temp_cfg, flags=re.MULTILINE):
                    f_log.write('------part------\n')
                    f_log.write(every_part)
                    #print every_part
                    i += 1
                f_log.write('Result - Total lines: %s\n' % i)
    f_log.close()


def process_text():
    s_path = input('Nhap duong dan :')
    s_file_name = input('Ten file can xu ly :')
    s_path_name = s_path + s_file_name
    f = open(s_path_name, 'r')
    temp_txt = f.readlines()
    f.close()
    s_file_name_new = s_file_name[:s_file_name.find('.')] + '_new.log'
    f_new = open(s_path + s_file_name_new, 'w')
    for line in temp_txt:
        f_new.write(line[line.find(' $') + 2:])
    f_new.close()

def main():
    print('1.Tim kiem regex')
    print('2.Xu ly text')
    sel_index = input('Chon :')
    if sel_index == '1':
        func_find()
    elif sel_index == '2':
        process_text()

if __name__ == '__main__':
    main()
