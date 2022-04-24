from asyncio.proactor_events import _ProactorWritePipeTransport
from dataclasses import dataclass
from fileinput import filename
import os
from importlib_metadata import files
import pandas as pd
from tabulate import tabulate

def getAllFiles():
    '''
        获取当前文件夹下所有的markdown文件
        忽略文件夹: [_book, node_modules]
    '''
    results = []
    for root,dirs,files in os.walk("./"):
            for file in files:
                if(file.split(".")[-1] == "md"):
                    if(root.split("/")[1] == '_book' or root.split("/")[1] == "node_modules"):
                        continue
                    results.append(root +"/"+ file)
    return results

def readHeaders(filename):
    '''
        读取markdown文件的header信息
        ---
        title = xxx
        date = xxx
        tags = xxx
        ---
    '''
    results = {}
    f = open(filename, "r+")
    contents = f.readlines()
    if(len(contents) == 0):
        # 内容为空，返回空结果
        return results
    if(contents == "" or contents[0] != '---\n'):
        # 不以 --- 开始，返回空结果
        return results
    curLine = 1
    # 写的辣眼睛
    while(True):
        # 一直读取文件知道出现下一个 ---
        content = contents[curLine]
        if(content == "---\n"):
            break
        key = ""
        for i in range(len(content)):
            if(content[i] == ":"):
                results[key] = content[i+1:-1]
                break
            key += content[i]
        curLine += 1
    return results

def listString2list(listStr):
    '''
        将一个列表字符串转为字符串列表
        "[1,2,3]" -> ["1","2","3"]
    '''
    l = []
    listStr.replace("，",",") # 如果有大写逗号，替换为小写逗号
    for item in listStr.split(","):
        item = item.replace("[","")
        item = item.replace("]","")
        item = item.replace(" ","")
        l.append(item)
    return l
    
if __name__ == '__main__':
    fileNames = getAllFiles()
    undatedFiles = []
    datedFiles = []
    for fileName in fileNames:
        headers = readHeaders(fileName)
        if(headers.get('date') == None):
            undatedFiles.append(fileName)
        else:
            datedFiles.append(fileName)
    
    print(undatedFiles)
    print(datedFiles)
        # if(headers.get('title') == None or headers.get('tags') == None):
        #     continue
        # title = headers['title'].replace(" ","")
        # tags = listString2list(headers['tags'])
        # date = headers["date"]
        # print(title)
        # print(date)

    
