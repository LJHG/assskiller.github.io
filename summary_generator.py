from glob import glob
import os

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
    if(contents[0] != '---\n'):
        # 不以 --- 开始，直接返回空字典
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



if __name__ == '__main__':
    fileNames = getAllFiles()
    for fileName in fileNames:
        print(readHeaders(fileName))