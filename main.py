import os
import sys
import time
import itertools

import argparse
import termcolor

from utils import isSubfileFolder


parser = argparse.ArgumentParser(
    description="Python script by AinTea#0519 that search subfolders and files by an URL given"
)

parser.add_argument(
    'url',
    metavar='url',
    type=str,
    help='Website\'s URL'
)

parser.add_argument(
    'logFilename',
    metavar='logFilename',
    type=str,
    nargs='?',
    default='./log.txt',
    help='File where the script logs will be written'
)

parser.add_argument(
    'forceWrite',
    metavar='forceWrite',
    type=bool,
    nargs='?',
    default=False,
    help='Argument that tells (or not) to the script he can overwrite on an existing logfile (given by the user)'
)

args = parser.parse_args()


if args.forceWrite and os.path.exists(args.logFilename):
    warningText = termcolor.colored(f"[/!\\] The file '{args.logFilename}' already exists", 'yellow')
    print(warningText)
    sys.exit()

# Creating / Overwrite a file and put nothing in it
with open(args.logFilename, 'w') as f:
    f.write("You can check all the return codes meaning and infos on https://kinsta.com/blog/http-status-codes/\n\n")


nameLength = 3
fileListed = 0

#combinationList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789."
combinationList = "homebootr"

listedFilefolder = []

try:
    while nameLength <= len(combinationList):
        for folderfileName in itertools.product(combinationList, repeat=nameLength):
            folderfileName = "".join(folderfileName)
            exists, statusCode, infoText = isSubfileFolder(args.url, name=folderfileName)

            if exists and not folderfileName in listedFilefolder:
                with open(args.logFilename, 'a') as f:
                    f.write(f"URL : {args.url}/{folderfileName}\nExists : {exists}\nStatus code : {statusCode}\nInfos : {infoText}\n\n-\n\n")

                print(f"-> {args.url}/{folderfileName}")

                listedFilefolder.append(folderfileName)
                fileListed += 1

        nameLength += 1
except KeyboardInterrupt:
    text = termcolor.colored(f"\n\n[+] {fileListed} files/folder listed\n", 'green')
    print(text)
    time.sleep(0.5)
    sys.exit()
