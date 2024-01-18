"""
读取命令行参数，对二进制文件进行加密，解密
"""

import sys
import os
import argparse
from tqdm.rich import tqdm
from rich import print

import warnings
from tqdm import TqdmExperimentalWarning

# 忽略tqdm的实验性警告
warnings.filterwarnings('ignore', category=TqdmExperimentalWarning)


def encrypt_file(file_name, key):
    """
    加密文件
    :param file_name: 文件名
    :param key: 密钥
    :return:
    """
    with open(file_name, 'rb') as f:
        data = f.read()
    data = bytearray(data)

    pbar = tqdm(range(len(data)), desc="Encrypting", unit="B", unit_scale=True, unit_divisor=1024)
    for i in pbar:
        data[i] ^= key
    with open(file_name, 'wb') as f:
        f.write(data)
    print(f"[green]Encryption of {file_name} completed![/green]")


def decrypt_file(file_name, key):
    """
    解密文件
    :param file_name: 文件名
    :param key: 密钥
    :return:
    """
    encrypt_file(file_name, key)


def encrypt_dir(dir_name, key):
    """
    加密目录下所有文件
    :param dir_name: 目录名
    :param key: 密钥
    :return:
    """
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            encrypt_file(os.path.join(root, file), key)


def decrypt_dir(dir_name, key):
    """
    解密目录下所有文件
    :param dir_name: 目录名
    :param key: 密钥
    :return:
    """
    encrypt_dir(dir_name, key)


def main():
    parser = argparse.ArgumentParser(description='encrypt or decrypt files')
    parser.add_argument('path', help='file or directory path')
    parser.add_argument('-k', '--key', type=int, default=0, help='key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt')
    args = parser.parse_args()
    if os.path.isfile(args.path):
        if args.decrypt:
            decrypt_file(args.path, args.key)
        else:
            encrypt_file(args.path, args.key)
    elif os.path.isdir(args.path):
        if args.decrypt:
            decrypt_dir(args.path, args.key)
        else:
            encrypt_dir(args.path, args.key)
    else:
        print('[red]Error: Invalid path![/red]')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[red]KeyboardInterrupt[/red]')
        sys.exit(1)