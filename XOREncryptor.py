"""
读取命令行参数，对二进制文件进行加密，解密
使用异或运算，加密解密使用同一函数

usage: python XOREncryptor.py [-h] [-k KEY] [-d] [-o OUTPUT] [-f] path

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


def encrypt_file(args):
    """
    加密文件
    :param args: 命令行参数
    :return:
    """
    file_name = args.path
    key = args.key
    output_file = args.output
    force = args.force

    if os.path.exists(output_file) and not force:
        print(f'[cyan]Output file already exists: [/cyan][yellow]{os.path.abspath(output_file)}[/yellow] [cyan]Use -f to force overwrite[/cyan]')
        return None
    
    File_name_Equal_Output_file = os.path.abspath(file_name) == os.path.abspath(output_file)
    if File_name_Equal_Output_file:
        os.rename(file_name, file_name + '.tmp')
        file_name += '.tmp'

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

    if File_name_Equal_Output_file:
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
    key = args.key
    output_dir = args.output
    force = args.force

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(dir_name), 'encrypted_' + os.path.basename(dir_name))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)
        output_file = os.path.join(output_dir, file_name)
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

    if os.path.isfile(args.path):
        print(f'[cyan]Input file: [/cyan][yellow]{args.path}[/yellow]')
        os.chdir(os.path.dirname(args.path))
        if args.decrypt:
            decrypt_file(args)
        else:
            encrypt_file(args)
    elif os.path.isdir(args.path):
        print(f'[cyan]Input directory: [/cyan][yellow]{args.path}[/yellow]')
        os.chdir(os.path.dirname(args.path))
        if args.decrypt:
            decrypt_dir(args)
        else:
            encrypt_dir(args)
    else:
        print('[red]Error: [/red][yellow]Path not exists![/yellow]')
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[red]KeyboardInterrupt[/red]')
        # print('[red]Program terminated![/red]')
        print('Exit code: [red]1[/red]')
        print('[green]Bye![/green]')
        sys.exit(1)
