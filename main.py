import os
import sys
import time
import itertools

import argparse
import termcolor

from utils import isSubfileFolder


def generatePossibilities(combinations : str, length : int):
    for combination in itertools.product(combinations, repeat=length):
        yield ''.join(combination)



parser = argparse.ArgumentParser(
    description="Python script by AinTea#0519 that search subfolders and files by an URL given"
)

parser.add_argument(
    '-u',
    '--url',
    type=str,
    help='Website\'s URL'
)

parser.add_argument(
    '-w',
    '--wordlist',
    type=str,
    nargs='?',
    default='',
    help='File that will content all combinations'
)

parser.add_argument(
    '-o',
    '--output-file',
    type=str,
    nargs='?',
    default='./log.txt',
    help='File where the script logs will be written'
)

parser.add_argument(
    '--brute-force',
    action='store_true',
    help='Argument that tells (or not) to the script he can overwrite on an existing logfile (given by the user)'
)

args = parser.parse_args()


if not args.wordlist and not args.brute_force:
    errorText = termcolor.colored(f"[!] You need either to precise a wordlist or if you want to use the brute force\n", 'red')
    print(errorText)
    sys.exit()
elif not os.path.exists(args.wordlist) and not args.brute_force:
    errorText = termcolor.colored(f"[!] The wordlist file '{args.wordlist}' doesn't exists\n", 'red')
    print(errorText)
    sys.exit()


if os.path.exists(args.output_file):
    warningText = termcolor.colored(f"[/!\\] The file '{args.output_file}' already exists", 'yellow')
    print(warningText)
    sys.exit()

# Creating / Overwrite a file and put nothing in it
with open(args.output_file, 'w') as f:
    f.write("You can check all the status code meanings and infos on https://kinsta.com/blog/http-status-codes/\n\n")


combinationLength = 1
listedFilesNumber = 0

combinationList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789."


# I transform the URL so there is no '/' at the end
if args.url.endswith('/'):
    args.url = args.url[:-1]


try:
    if args.brute_force:
        while combinationLength <= len(combinationList):
            for folderfileName in generatePossibilities(combinationList, combinationLength):
                exists, statusCode, infoText = isSubfileFolder(args.url, name=folderfileName)

                if exists and not folderfileName in open(args.output_file, 'r').read():
                    with open(args.output_file, 'a') as f:
                        f.write(f"URL : {args.url}/{folderfileName}\nExists : {exists}\nStatus code : {statusCode}\nInfos : {infoText}\n\n-\n\n")

                    print(f"-> {args.url}/{folderfileName}")

                    listedFilesNumber += 1

            combinationLength += 1
    else:
        with open(args.wordlist, 'r') as f:
            wordList = f.read().split('\n')
        
        for combination in wordList:
            exists, statusCode, infoText = isSubfileFolder(args.url, name=combination)
            
            if exists:
                with open(args.output_file, 'a') as f:
                    f.write(f"URL : {args.url}/{combination}\nExists : {exists}\nStatus code : {statusCode}\nInfos : {infoText}\n\n-\n\n")
                    
                print(f"-> {args.url}/{combination}")
                
                listedFilesNumber += 1
except KeyboardInterrupt:
    text = termcolor.colored(f"\n\n[+] {listedFilesNumber} files/folder listed\n", 'green')
    print(text)
    time.sleep(0.5)
    sys.exit()
