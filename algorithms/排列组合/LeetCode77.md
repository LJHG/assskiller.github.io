---
title: 组合---LeetCode77(不小心把组合做成排列了)
date: 2020-09-08 10:42:51
tags: [组合,排列,回溯,dfs]
---
## 题目描述：  
给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。

## 示例：   
```cpp
示例:
输入: n = 4, k = 2
输出:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]
```
<!-- more -->

## 解题思路:  
我一看到这道题，就想到了前几天做的[全排列](https://www.assskiller.cn/2020/09/05/LeetCode60/)，心想这不是一样的题吗，秒了。  
虽然过了，但是出奇的慢，思索一番(看了一波题解)过后，发现我把组合的问题做成了排列。  
### 排列做法
排列做法和全排列的那道题一样，都是记录了一个vis数组，来看是否已经访问过。  
至于排列为什么需要一个vis数组呢，是因为排列后面的元素的后面是可以去访问前面的元素的，例如213这种，所以需要一个vis数组来进行记录。但是对于组合来说，123,213,321都是一样的，所以在做组合问题时用排列完全是大材小用了。  
在使用排列解决组合时，为了通过，我还使得往后添加的元素不得大于前面的元素，那排列这种方法就更显得可笑了。  
```cpp
class Solution {
public:
    vector<vector<int>> ans;
    int target;
    int N;
    void dfs(vector<int>& vis,int visNum,vector<int>& record){
        if(visNum == target){
            ans.push_back(record);
            return;
        }
        for(int i=1;i<=N;i++){
            if(!vis[i]){
                if(visNum == 0 || i>record[visNum-1]){
                    record.push_back(i);
                    vis[i] = 1;
                    dfs(vis,visNum+1,record);
                    vis[i] = 0;
                    record.pop_back();
                }
                
            }
        }
        
    }
    vector<vector<int>> combine(int n, int k) {
        vector<int> vis;
        for(int i=0;i<=n;i++) vis.push_back(0);
        N = n;
        target = k;
        vector<int> record;
        record.clear();
        dfs(vis,0,record);
        return ans;
        
    }
};
```

### 组合做法
组合的做法就很简单了，对于每一种位置，可以选择选或者不选，完了。  
可以稍微剪一下枝，更快。(不剪都比排列快)  
```cpp
class Solution {
public:
    vector<int> record;
    vector<vector<int>> ans;
    int target;
    void dfs(int n,int pos,int num){
        if(num == target){
            ans.push_back(record);
            return;
        }
        if(pos > n ) return;
        if(num + (n-pos)+1 < target) return; //到不了了 return
        //选择该位置
        record.push_back(pos);
        dfs(n,pos+1,num+1);
        record.pop_back();

        //不选择该位置
        dfs(n,pos+1,num);
    }
    vector<vector<int>> combine(int n, int k) {
        record.clear();
        target = k;
        dfs(n,1,0);
        return ans;
    }
};
```
## 题目链接：  
https://leetcode-cn.com/problems/combinations/