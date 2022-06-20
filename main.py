#!/usr/bin/python3

import os
import sys
import time
import argparse
import requests
import itertools

import termcolor

from utils import subname_exists, Color

VERSION = "0.1"
ASCII_ART = f"""{Color.BOLD}
 _______               ______               __              
|_     _|.-----.---.-.|   __ \.--.--.-----.|  |_.-----.----.
  |   |  |  -__|  _  ||   __ <|  |  |__ --||   _|  -__|   _|
  |___|  |_____|___._||______/|_____|_____||____|_____|__|  
{Color.END}"""



def generate_possibilities(combinations : str, length : int):
    for combination in itertools.product(combinations, repeat=length):
        yield ''.join(combination)


parser = argparse.ArgumentParser(
    description="Python script by AinTea#0519 that search subfolders and files by an URL given"
)

parser.add_argument(
    "-u",
    "--url",
    type=str,
    help="Website\'s URL"
)

parser.add_argument(
    "-w",
    "--wordlist",
    type=str,
    nargs='?',
    default='',
    help="File that will content all combinations"
)

parser.add_argument(
    "-o",
    "--output-file",
    type=str,
    nargs='?',
    default="./log.txt",
    help="File where the script logs will be written"
)

parser.add_argument(
    "--brute-force",
    action="store_true",
    help="Argument that tells (or not) to the script he can overwrite on an existing logfile (given by the user)"
)

args = parser.parse_args()

if not args.url:
    error_text = termcolor.colored("[!] You must specify an URL\n", "red")
    parser.print_help()
    sys.exit(1)


try:
    requests.get(args.url)
except requests.exceptions.InvalidURL:
    error_text = termcolor.colored("[!] URL is invalid\n", "red")
    print(error_text)
    sys.exit(1)
except requests.exceptions.ConnectionError:
    error_text = termcolor.colored("[!] URL is inaccessible\n", "red")
    print(error_text)
    sys.exit(1)
except requests.exceptions.MissingSchema:
    error_text = f"{Color.RED}[!] URL format is invalid, did you meant \
'{Color.END}{Color.GREEN}{Color.BOLD}http://{Color.END}{Color.RED}{args.url}' or \
'{Color.GREEN}{Color.BOLD}https://{Color.END}{Color.RED}{args.url}' ?{Color.END}\n"
    
    print(error_text)
    sys.exit(1)



if (not args.wordlist and not args.brute_force) or (args.wordlist and args.brute_force):
    error_text = termcolor.colored(f"[!] You need either to precise a wordlist or if you want to use the brute force\n", 'red')
    print(error_text)
    sys.exit()
elif not os.path.exists(args.wordlist) and not args.brute_force:
    error_text = termcolor.colored(f"[!] The wordlist file '{args.wordlist}' doesn't exists\n", 'red')
    print(error_text)
    sys.exit()


if os.path.exists(args.output_file):
    warning_text = termcolor.colored(f"[/!\\] The file '{args.output_file}' already exists", 'yellow')
    print(warning_text)
    sys.exit()

# Creating / Overwrite a file and put nothing in it
with open(args.output_file, 'w') as f:
    f.write("You can check all the status code meanings and infos on https://kinsta.com/blog/http-status-codes/\n\n")


combination_length = 1
listed_files_number = 0

combination_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789. "


# I transform the URL so there is no '/' at the end
if args.url.endswith('/'):
    args.url = args.url[:-1]



print(f"""
{Color.BOLD}{Color.RED}{ASCII_ART}{Color.END}

TeaBuster v{VERSION}
by AinTea (AinTea#0519) https://github.com/AinTEAsports/website-sublister

=======================[ {Color.BOLD}{Color.RED}TeaBuster{Color.END} ]=======================

[~] Target   : {args.url}
[~] Method   : GET
[~] Wordlist : {args.wordlist if args.wordlist else "brute force mode selected"}
[~] Version  : TeaBuster v{VERSION}

===========================================================
""")



try:
    if args.brute_force:
        while combination_length <= len(combination_list):
            for folder_file_name in generate_possibilities(combination_list, combination_length):
                exists, status_code, info_text = subname_exists(args.url, name=folder_file_name)

                if exists and not folder_file_name in open(args.output_file, 'r').read():
                    with open(args.output_file, 'a') as f:
                        f.write(f"URL : {args.url}/{folder_file_name}\nExists : {exists}\nStatus code : {status_code}\nInfos : {info_text}\n\n-\n\n")

                    print(f"-> {args.url}/{folder_file_name}")

                    listed_files_number += 1

            combination_length += 1
    else:
        with open(args.wordlist, 'r') as f:
            wordlist = f.read().split('\n')

        for combination in wordlist:
            exists, status_code, info_text = subname_exists(args.url, name=combination)

            if exists:
                with open(args.output_file, 'a') as f:
                    f.write(f"URL : {args.url}/{combination}\nExists : {exists}\nStatus code : {status_code}\nInfos : {info_text}\n\n-\n\n")


                if str(status_code).startswith('2'):
                    colored_stat_code = f"{Color.BOLD}{Color.GREEN}{status_code}{Color.END}"
                else:
                    colored_stat_code = f"{Color.BOLD}{Color.RED}{status_code}{Color.END}"

                print("-> {:<50} [{:<}]".format(f"{args.url}/{combination}", colored_stat_code))

                listed_files_number += 1
except KeyboardInterrupt:
    if listed_files_number:
        colored_number = f"{Color.BOLD}{Color.GREEN}{listed_files_number}{Color.END}"
    else:
        colored_number = f"{Color.BOLD}{Color.RED}{listed_files_number}{Color.END}"

    print(f"\n\n[{Color.BOLD}{Color.GREEN}+{Color.END}] {colored_number} files/folder listed\n")
    time.sleep(0.5)
    sys.exit()
