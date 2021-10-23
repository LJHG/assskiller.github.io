---
title: 旅行终点站---LeetCode5400
date: 2020-05-03 15:52:09
tags: [集合, set, map, 出度入度]
---
### 题目描述：  
给你一份旅游线路图，该线路图中的旅行线路用数组 paths 表示，其中 paths[i] = [cityAi, cityBi] 表示该线路将会从 cityAi 直接前往 cityBi 。请你找出这次旅行的终点站，即没有任何可以通往其他城市的线路的城市。

题目数据保证线路图会形成一条不存在循环的线路，因此只会有一个旅行终点站。

### 示例：   
```cpp
示例 1：
输入：paths = [["London","New York"],["New York","Lima"],["Lima","Sao Paulo"]]
输出："Sao Paulo" 
解释：从 "London" 出发，最后抵达终点站 "Sao Paulo" 。本次旅行的路线是 "London" -> "New York" -> "Lima" -> "Sao Paulo" 。

示例 2：
输入：paths = [["B","C"],["D","B"],["C","A"]]
输出："A"
解释：所有可能的线路是：
"D" -> "B" -> "C" -> "A". 
"B" -> "C" -> "A". 
"C" -> "A". 
"A". 
显然，旅行终点站是 "A" 。

示例 3：
输入：paths = [["A","Z"]]
输出："Z"
 
提示：
1 <= paths.length <= 100
paths[i].length == 2
1 <= cityAi.length, cityBi.length <= 10
cityAi != cityBi
所有字符串均由大小写英文字母和空格字符组成。

```

<!--more-->

### 解题思路:  
这道题看到的第一眼想到的是dfs，打这场周赛时，看到什么题都想dfs，后来都果不其然的超时了。  
正确的解法是统计入度和出度，因为题目说了必定会有结果，所以可以知道，重点站的入度为1，出度为0，所以只需要统计所有的起点站，然后统计所有的城市，如果没有起点站的城市，就是终点站。

```cpp
class Solution {
public:
    string destCity(vector<vector<string>>& paths) {
        //因为这道题保证会有结果，终点站只有入度没有出度
        map<string,int> cnt;
        set<string> city;
        int length = paths.size();
        for(int i=0;i<length;i++)
        {
            cnt[paths[i][0]] ++;
            city.insert(paths[i][0]);
            city.insert(paths[i][1]);
        }
        for(auto c:city)
        {
            if(cnt[c] == 0)
                return c;
        }
        return "";
    }
};
```

### PS:超时的dfs
```cpp
class Solution {
public:
    string go(vector<vector<string>>& paths, string start)
    {
        int length = paths.size();
        if(length == 1)
        {
            if(paths[0][0] == start)
                return paths[0][1];
            else 
                return "nowhere";
        }
        int mark = -1;
        for(int i=0;i<length;i++)
        {
            if(paths[i][0] == start)
            {
                mark = i;
            }
        }
        if(mark == -1)
        {
            return "nowhere";
        }
        else
        {
            vector<vector<string>> lastPath;
            for(int i=0;i<length;i++)
            {
                if(i==mark)
                {
                    start = paths[i][1];
                    continue;
                }
                lastPath.push_back(paths[i]);
            }
            
            return go(lastPath,start);
        }
    }
    
    string destCity(vector<vector<string>>& paths) {
        int length = paths.size();
        for(int i=0;i<length;i++)
        {
            string start = paths[i][0];
            string ans = go(paths,start);
            if(ans != "nowhere")
                return ans;
        }
        return "nowhere";
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/destination-city/