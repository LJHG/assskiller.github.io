import os
import re
import json

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

def dateParse(date):
    # 输入一个date 形式可能有很多种
    # 形式1: yyyy-mm-dd xx:xx:xx
    # 目前也只有形式1
    pattern = "[2][0][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"
    parseDate = re.search(pattern, date, flags=0)
    return parseDate.group()

def isYear(year):
    # 判断一个year是不是20xx -> 毕竟活不到21xx了
    if(re.match("20[0-9][0-9]", year) != None): #其实这个有bug，如果是2022222也是对的，不过无所谓了。。。
        return True
    else:
        return False

class ArchiveArticle:
    def __init__(self, title, url, date) -> None:
        self.title = title
        self.url = url
        self.date = date


class ArchiveList:
    def __init__(self) -> None:
        self.archiveList = [] # [ArchiveArticle1, ArchiveArticle2...]
    
    def addItem(self, title, url, date):
        _title = title
        _url = url
        _date = date

        # 把日期解析为规定格式
        if(date != None):
            _date = dateParse(date)
        else:
            _date = "未指定日期"

        if(_title == None and _url == None):
            raise
        # 如果没有设定标题，那么把标题设置为文件名
        if(_title == None):   
            _title = url.split("/")[-1].split(".")[0]
        
        # 如果路径表示该文件是一个readme文件，那么就不添加了
        if(url.split("/")[-1] == "README.md" or url.split("/")[-1] == "readme.md"):
            return 
        
        # 将url的.md 转换为.html
        _url = _url[0:-3] + ".html"
        self.archiveList.append(ArchiveArticle(_title,_url,_date))
    
    def printAll(self):
        for item in self.archiveList:
            print("")
            print(item.title)
            print(item.url)
            print(item.date)
            print("")
    
    def deleteSpecificItem(self):
        delete_urls=[".//archive.html",
                    ".//SUMMARY.html",
                    "./algorithms/java/spring-boot-maven-plugin-error.html"
                    ]
        # 先求出对应的idx
        delete_idxs = []
        for idx, item in enumerate(self.archiveList):
            if(item.url in delete_urls):
                delete_idxs.append(idx)
        #对索引进行逆序，然后删除元素
        delete_idxs.reverse()
        for idx in delete_idxs:
            self.archiveList.pop(idx)
        return
    
    def sortByDate(self):
        # print(self.archiveList)
        self.archiveList.sort(key=lambda x:x.date, reverse=True)
        # print(self.archiveList)

    def writeJsonToFile(self,fileName):
        # 删除特定项
        self.deleteSpecificItem()

        # 对日期进行排序
        self.sortByDate()

        
        # 将文章按年份分开
        # 其实这一部分归档也可以交给js做
        yearArchives = {} # {"2021":[], "2020":[], "未归档":[]}
        for item in self.archiveList:
            year = item.date[0:4]
            if(isYear(year) == False):
                year = "未归档"
            if(year not in yearArchives.keys()):
                yearArchives[year] = []
            yearArchives[year].append(item.__dict__)
        with open(fileName, 'w') as f:
            json.dump(yearArchives, f,ensure_ascii=False)
        


if __name__ == '__main__':
    fileNames = getAllFiles()
    archiveList = ArchiveList()
    for fileName in fileNames:
        headers = readHeaders(fileName)
        archiveList.addItem(headers.get("title"),fileName,headers.get("date"))
    archiveList.writeJsonToFile("./archive.json")


    
