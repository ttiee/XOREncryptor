"""
读取命令行参数，对二进制文件进行加密，解密
"""

import sys
import os
import argparse


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
    parser = argparse.ArgumentParser(description='encrypt or decrypt files')
    parser.add_argument('path', help='file or directory path')
    parser.add_argument('-k', '--key', type=int, default=0, help='key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt')
    args = parser.parse_args()
    if os.path.isfile(args.path):
        if args.decrypt:
            dec_file(args.path, args.key)
        else:
            enc_file(args.path, args.key)
    elif os.path.isdir(args.path):
        if args.decrypt:
            dec_dir(args.path, args.key)
        else:
            enc_dir(args.path, args.key)
    else:
        print('path not exists')


if __name__ == '__main__':
    main()