"""
读取命令行参数，对二进制文件进行加密，解密
使用异或运算，加密解密使用同一函数

usage: python XOREncryptor.py [-h] [-k KEY] [-d] [-o OUTPUT] path

author: ttiee
time: 2024/1/18

update: 2021/1/19
"""

import argparse
import os
import sys
import warnings

from rich import print
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm

# ignore tqdm experimental warning
warnings.filterwarnings('ignore', category=TqdmExperimentalWarning)


def encrypt_file(file_name, key, output_file):
    """
    加密文件
    :param file_name: 文件名
    :param key: 密钥
    :param output_file: 输出文件名
    :return:
    """
    with open(file_name, 'rb') as f:
        data = f.read()
    data = bytearray(data)

    pbar = tqdm(range(len(data)), desc="[green]Encrypting[/green]", unit="B", unit_scale=True, unit_divisor=1024)
    for i in pbar:
        data[i] ^= key
    with open(output_file, 'wb') as f:
        f.write(data)
    print(f'[green]Encrypting finished![/green] [cyan]Output file: [/cyan][yellow]{os.path.abspath(output_file)}[/yellow]')
    

def decrypt_file(file_name, key, output_file):
    """
    解密文件
    :param file_name: 文件名
    :param key: 密钥
    :param output_file: 输出文件名
    :return:
    """
    encrypt_file(file_name, key, output_file)


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
    parser.add_argument('path', type=str, help='file or directory path')
    parser.add_argument('-k', '--key', type=int, default=0, help='key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt')
    parser.add_argument('-o', '--output', default=None, help='output file or directory')
    args = parser.parse_args()

    if args.output is None:
        args.output = args.path

    if os.path.isfile(args.path):
        if args.decrypt:
            decrypt_file(args.path, args.key, args.output)
        else:
            encrypt_file(args.path, args.key, args.output)
    elif os.path.isdir(args.path):
        if args.decrypt:
            decrypt_dir(args.path, args.key)
        else:
            encrypt_dir(args.path, args.key)
    else:
        print('[red]Error: [/red][yellow]Path not exists![/yellow]')
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[red]KeyboardInterrupt[/red]')
        # print('[red]Program terminated![/red]')
        print('Exit code: [red]1[/red]')
        print('[green]Bye![/green]')
        sys.exit(1)
