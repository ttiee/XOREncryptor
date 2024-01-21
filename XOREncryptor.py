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


def encrypt_file(file_name, key, output_file, force=False):
    """
    加密文件
    :param file_name: 文件名
    :param key: 密钥
    :param output_file: 输出文件名
    :return:
    """
    if os.path.exists(output_file) and not force:
        print(f'[red]Error: [/red][yellow]Output file already exists: [/yellow][cyan]{output_file}[/cyan]')
        return None
    with open(file_name, 'rb') as f, open(output_file, 'wb') as f2:
        pbar = tqdm(range(os.path.getsize(file_name)), desc="[green]Encrypting[/green]", unit="B", unit_scale=True, unit_divisor=1024)
        while True:
            data = f.read(1024)
            if not data:
                break
            data = bytearray(data)
            for i in range(len(data)):
                data[i] ^= key
            f2.write(data)
            pbar.update(len(data))
        pbar.close()
    
    print(f'[green]Encrypting finished![/green] [cyan]Output file: [/cyan][yellow]{os.path.abspath(output_file)}[/yellow]')
    

def decrypt_file(file_name, key, output_file, force=False):
    """
    解密文件
    :param file_name: 文件名
    :param key: 密钥
    :param output_file: 输出文件名
    :return:
    """
    encrypt_file(file_name, key, output_file, force)


def encrypt_dir(dir_name, key, output_dir=None, force=False):
    """
    加密目录下所有文件
    :param dir_name: 目录名
    :param key: 密钥
    :param output_dir: 输出目录
    :return:
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(dir_name), 'encrypted_' + os.path.basename(dir_name))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)
        output_file = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key, output_file, force)
        elif os.path.isdir(file_path):
            encrypt_dir(file_path, key, output_file, force)


def decrypt_dir(dir_name, key, output_dir=None, force=False):
    """
    解密目录下所有文件
    :param dir_name: 目录名
    :param key: 密钥
    :param output_dir: 输出目录
    :return:
    """
    encrypt_dir(dir_name, key, output_dir, force)


def main():
    parser = argparse.ArgumentParser(description='encrypt or decrypt files')
    parser.add_argument('path', type=str, help='file or directory path')
    parser.add_argument('-k', '--key', type=int, default=0, help='key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt')
    parser.add_argument('-o', '--output', default=None, help='output file or directory')
    parser.add_argument('-f', '--force', action='store_true', help='force overwrite output file')
    args = parser.parse_args()

    args.path = os.path.abspath(args.path)

    if args.output is None:
        args.output = os.path.join(os.path.dirname(args.path), 'encrypted_' + os.path.basename(args.path))

    if args.output == args.path:
        print('[red]Error: [/red][yellow]Output file is the same as input file![/yellow]')
        sys.exit(1)
    
    if os.path.isfile(args.path):
        print(f'[cyan]Input file: [/cyan][yellow]{args.path}[/yellow]')
        if args.decrypt:
            decrypt_file(args.path, args.key, args.output, args.force)
        else:
            encrypt_file(args.path, args.key, args.output, args.force)
    elif os.path.isdir(args.path):
        print(f'[cyan]Input directory: [/cyan][yellow]{args.path}[/yellow]')
        if args.decrypt:
            decrypt_dir(args.path, args.key, args.output, args.force)
        else:
            encrypt_dir(args.path, args.key, args.output, args.force)
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
