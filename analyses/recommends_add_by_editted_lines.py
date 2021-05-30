#! /usr/bin/env python3

import glob
import subprocess
import csv
import sys
import os

recommend_message1 = f''

home = os.environ['KANI_HOME']
threshold = 3

class EdittedLine:
    def __init__(self, addedLines, deletedLines, fileName):
        self.addedLines = int(addedLines)
        self.deletedLines = int(deletedLines)
        self.fileName = fileName

    def total_lines(self):
        return self.addedLines + self.deletedLines

    def should_commit(self, threshold):
        return self.total_lines() > threshold

def recommend_commit_ja(list):
    total_lines = 0
    for item in list:
        total_lines = total_lines + item.total_lines()
    if len(list) == 1:
        print(f'{list[0].fileName} の編集行数が{threshold}行を超えたので，"git add" を実行しましょう（合計編集行数: {total_lines}）．')
    else:
        print(f'{list[0].fileName} ほか{len(list)-1}ファイルの編集行数が{threshold}行を超えたので，"git add" を実行しましょう（合計編集行数: {total_lines}）．')

def recommend_commit(list):
    total_lines = 0
    for item in list:
        total_lines = total_lines + item.total_lines()
    if len(list) == 1:
        print(f'Recommend "git add" since editted lines of {list[0].fileName} was bigger than {threshold} lines. (total: {total_lines})')
    elif len(list) == 2:
        print(f'Recommend "git add" since editted lines of {list[0].fileName} and another file were bigger than {threshold} lines. (total: {total_lines})')
    else:
        print(f'Recommend "git add" since editted lines of {list[0].fileName} and other {len(list)-1} files were bigger than {threshold} lines. (total: {total_lines})')

def build_lines():
    result = subprocess.run("git diff --numstat | awk -v OFS=, '{print $1,$2,$3}'", shell=True, text=True, stdout=subprocess.PIPE)
    list = []
    for line in csv.reader(result.stdout.strip().splitlines()):
        el = EdittedLine(line[0], line[1], line[2])
        if el.should_commit(threshold):
            list.append(el)
    return list

list = build_lines()
if len(list) > 0:
    recommend_commit_ja(list)
    sys.exit(1)
