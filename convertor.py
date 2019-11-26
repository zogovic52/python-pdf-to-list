#!/usr/bin/env python3

__author__ = 'Nikola'
__date__ = '26.11.2019'

import sys
import html2text
import re
import csv
import os
import shutil
from subprocess import call

FILENAME = "all.pdf"

def validStr(str):
    str = re.sub(r"[\**]", "", str)
    str = re.sub(r"\s*$", "", str)
    return str


def logicalStr(str):
    return re.sub(r"[\s|-]", "_", str)


def main():
    filename = FILENAME[:-4]

    # Remove old files.
    if os.path.exists(filename+"-html.html"):
        os.remove(filename+"-html.html")

    # Change pdf into html.
    call(["pdftohtml", filename+".pdf", "-q", "-s", "-i"])
    html = open(filename+"-html.html", encoding="utf8").read()
    text = html2text.html2text(html)

    resList = []

    # Parse file and return extracted data.

    row = []
    offsetStart = 0
    offsetEnd = 0
    physicalName = ""
    fieldLength = 0
    flag = 0
    cnt = 0

    for line in text.split("\n"):
        s = re.search(r"^(\d)+–(\d)+$", line)
        if(s is not None and flag == 0):
            flag = 1
            s = s.group()
            offsetStart = re.search(r"\d+", s).group()
            osLen = len(offsetStart)+1

            offsetEnd = re.search(r"\d+", s[osLen:]).group()
            osLen = osLen + len(offsetEnd) + 1
        elif(flag == 1 and re.search(r"[0-9]+", line) is not None):
            fieldLength = validStr(line)
            flag = 2
        elif(flag == 2 and re.search(r"[a-zA-Z]+", line) is not None):
            physicalName = validStr(line)

            row = [cnt, offsetStart, offsetEnd, physicalName,
                   logicalStr(physicalName), fieldLength]
            resList.append(row)
            cnt = cnt + 1
            flag = 0

    # Remove temp file.
    if os.path.exists(filename+"-html.html"):
        os.remove(filename+"-html.html")
    if os.path.exists(filename+"s.html"):
        os.remove(filename+"s.html")

    return resList

if __name__ == "__main__":
  res = main()
  sys.exit(res)