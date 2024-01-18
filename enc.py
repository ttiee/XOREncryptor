"""
读取命令行参数，对二进制文件进行加密，解密
"""

import sys
import os


def enc_file(file_name, key):
    """
    加密文件
    :param file_name: 文件名
    :param key: 密钥
    :return:
    """
    with open(file_name, 'rb') as f:
        data = f.read()
    data = bytearray(data)
    for i in range(len(data)):
        data[i] ^= key
    with open(file_name, 'wb') as f:
        f.write(data)


def dec_file(file_name, key):
    """
    解密文件
    :param file_name: 文件名
    :param key: 密钥
    :return:
    """
    enc_file(file_name, key)


def enc_dir(dir_name, key):
    """
    加密目录下所有文件
    :param dir_name: 目录名
    :param key: 密钥
    :return:
    """
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            enc_file(os.path.join(root, file), key)


def dec_dir(dir_name, key):
    """
    解密目录下所有文件
    :param dir_name: 目录名
    :param key: 密钥
    :return:
    """
    enc_dir(dir_name, key)


def main():
    """
    主函数
    :return:
    """
    if len(sys.argv) != 5:
        print('Usage: enc.py [enc|dec] [file|dir] [name] [key]')
        return
    if sys.argv[1] == 'enc':
        if sys.argv[2] == 'file':
            enc_file(sys.argv[3], int(sys.argv[4]))
        elif sys.argv[2] == 'dir':
            enc_dir(sys.argv[3], int(sys.argv[4]))
        else:
            print('Usage: enc.py [enc|dec] [file|dir] [name] [key]')
    elif sys.argv[1] == 'dec':
        if sys.argv[2] == 'file':
            dec_file(sys.argv[3], int(sys.argv[4]))
        elif sys.argv[2] == 'dir':
            dec_dir(sys.argv[3], int(sys.argv[4]))
        else:
            print('Usage: enc.py [enc|dec] [file|dir] [name] [key]')
    else:
        print('Usage: enc.py [enc|dec] [file|dir] [name] [key]')
    return


if __name__ == '__main__':
    main()