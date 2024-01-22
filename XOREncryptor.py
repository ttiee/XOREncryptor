# -*- coding: utf-8 -*-

"""
读取命令行参数，对二进制文件进行加密，解密
使用异或运算，加密解密使用同一函数

usage: python XOREncryptor.py [-h] [-k KEY] [-d] [-o OUTPUT] [-f] path

description:
    Encrypt or decrypt files or directories

options:
    -h, --help            show this help message and exit
    -k KEY, --key KEY     key
    -d, --decrypt         decrypt
    -o OUTPUT, --output OUTPUT
                          output file or directory
    -f, --force           force overwrite output file

example:
    python XOREncryptor.py -k 123456 -o encrypted_file -f file

note:
    1. The key must be an integer
    2. The key must be the same when encrypting and decrypting
    3. The output file or directory must not exist, unless you use -f

author: ttiee
github: http://github/ttiee

time: 2024/1/18

update: 2021/1/22
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
unfinished_file = None


def encrypt_file(args):
    """
    加密文件
    :param args: 命令行参数
    :return:
    """
    global unfinished_file

    file_name = args.path
    key = args.key
    output_file = args.output
    force = args.force

    if os.path.exists(output_file) and not force:
        """如果输出文件已存在，且没有指定强制覆盖，则退出"""
        print(f'[cyan]Output file already exists: [/cyan][yellow]{os.path.abspath(output_file)}[/yellow] [cyan]Use -f to force overwrite[/cyan]')
        return None
    
    # 如果输入文件和输出文件相同，则先重命名输入文件作为临时文件
    File_name_Equal_Output_file = os.path.abspath(file_name) == os.path.abspath(output_file)
    if File_name_Equal_Output_file:
        os.rename(file_name, file_name + '.tmp')
        file_name += '.tmp'

    with open(file_name, 'rb') as f, open(output_file, 'wb') as f2:
        unfinished_file = output_file
        pbar = tqdm(range(os.path.getsize(file_name)), desc="[green]Encrypting[/green]", unit="B", unit_scale=True, unit_divisor=1024)
        while True:
            data = f.read(1024)
            if not data:
                # 读取完毕
                break
            data = bytearray(data)
            for i in range(len(data)):
                data[i] ^= key
            f2.write(data)
            pbar.update(len(data))
        pbar.close()
    unfinished_file = None  # 读取完毕，将未完成文件置空

    if File_name_Equal_Output_file:
        # 删除临时文件
        os.remove(file_name)
    
    print(f'[green]Encrypting finished![/green] [cyan]Output file: [/cyan][yellow]{os.path.abspath(output_file)}[/yellow]')
    

def decrypt_file(args):
    """
    解密文件
    :param args: 命令行参数
    :return:
    """
    encrypt_file(args)


def encrypt_dir(args):
    """
    加密目录下所有文件
    :param args: 命令行参数
    :return:
    """
    dir_name = args.path
    output_dir = args.output

    if output_dir is None:
        """如果没有指定输出目录，则默认输出到encrypted_目录"""
        output_dir = os.path.join(os.path.dirname(dir_name), 'encrypted_' + os.path.basename(dir_name))
    if not os.path.exists(output_dir):
        """如果输出目录不存在，则创建"""
        os.mkdir(output_dir)
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)   # 文件或目录的绝对路径
        output_file = os.path.join(output_dir, file_name)   # 输出文件或目录的绝对路径
        if os.path.isfile(file_path):
            args.path = file_path
            args.output = output_file
            encrypt_file(args)
        elif os.path.isdir(file_path):
            args.path = file_path
            args.output = output_file
            encrypt_dir(args)


def decrypt_dir(args):
    """
    解密目录下所有文件
    :param args: 命令行参数
    :return:
    """
    encrypt_dir(args)


def get_args():
    """
    设置命令行参数
    :return:
    """
    parser = argparse.ArgumentParser(description='encrypt or decrypt files')
    parser.add_argument('path', type=str, help='file or directory path')
    parser.add_argument('-k', '--key', type=int, default=0, help='key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt')
    parser.add_argument('-o', '--output', default=None, help='output file or directory')
    parser.add_argument('-f', '--force', action='store_true', help='force overwrite output file')
    args = parser.parse_args()
    return args


def analysis_args(args):
    """
    分析命令行参数
    :param args: 命令行参数
    :return:
    """
    args.path = os.path.abspath(args.path)

    if args.output is None:
        """如果没有指定输出文件或目录，则默认输出到encrypted_文件或目录"""
        args.output = os.path.join(os.path.dirname(args.path), 'encrypted_' + os.path.basename(args.path))

    if os.path.isfile(args.path):
        print(f'[cyan]Input file: [/cyan][yellow]{args.path}[/yellow]')
        # 切换到输入文件所在目录
        os.chdir(os.path.dirname(args.path))    
        if args.decrypt:
            decrypt_file(args)
        else:
            encrypt_file(args)
    elif os.path.isdir(args.path):
        print(f'[cyan]Input directory: [/cyan][yellow]{args.path}[/yellow]')
        # 切换到输入目录所在目录
        os.chdir(os.path.dirname(args.path))
        if args.decrypt:
            decrypt_dir(args)
        else:
            encrypt_dir(args)
    else:
        # 输入路径不存在
        print('[red]Error: [/red][yellow]Path not exists![/yellow]')
        sys.exit(1)


def main():
    """
    主函数
    :return:
    """
    args = get_args()
    analysis_args(args)
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C 退出
        if unfinished_file is not None:
            # 如果有未完成的文件，则删除
            os.remove(unfinished_file)
        print('[red]KeyboardInterrupt[/red]')
        print('Exit code: [red]1[/red]')
        print('[green]Bye![/green]')
        sys.exit(1)
