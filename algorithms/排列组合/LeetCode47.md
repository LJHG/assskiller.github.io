---
title: 全排列Ⅱ---LeetCode47(去重)
date: 2020-09-18 10:13:54
tags: [排列,dfs,回溯,剪枝,去重]
---
## 题目描述：  
给定一个可包含重复数字的序列，返回所有不重复的全排列。

## 示例：   
```cpp
输入: [1,1,2]
输出:
[
  [1,1,2],
  [1,2,1],
  [2,1,1]
]
```
<!-- more -->

## 解题思路:  
最开始想到的是暴力set去重法，然后又去看了看题解，才知道了正确的去重方法。  

### set去重
万能的set去重，就是效率低了点。  
```cpp
class Solution {
public:
    set<vector<int>> ans;
    vector<int> record;
    int len;
    void dfs(vector<int>& nums,vector<int>& vis){
        int flag = 0;
        for(int i=0;i<len;i++){
            if(vis[i] == 0){
                flag = 1;
                record.push_back(nums[i]);
                vis[i] =1;
                dfs(nums,vis);
                vis[i]=0;
                record.pop_back();
            }
        }
        if(flag == 0){
            ans.insert(record);
        }
    }
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        //完了，我又只会set了
        len = nums.size();
        vector<int> vis;
        for(int i=0;i<len;i++) vis.push_back(0);
        dfs(nums,vis);
        vector<vector<int>> vans;
        for(auto x:ans){
            vans.push_back(x);
        }
        return vans;
    }
};
```

### 同一层不选择相同数字
这个应该就是这道题的核心去重方法了，就是说在同一层是(比如选择第一个数字时)，如果有相同的数字，那么就不选，然后就行了，就这么简单。  
我在记录时，是开了一个数组叫做choicesInLayer,最开始开成全局数组了，以为每一次memset一下就好了，结果是个深坑，稍微想一想就知道怎么可能是开全局数组啊，然后改成局部的就过了(搞得我还以为是算法除了啥问题)。  

```cpp
class Solution {
public:
    vector<vector<int>> ans;
    vector<int> record;
    int len;
    
    void dfs(vector<int>& nums,vector<int>& vis){
        int flag = 0;
        int choicesInLayer[1000];
        memset(choicesInLayer,0,sizeof(choicesInLayer));
        for(int i=0;i<len;i++){
            if(vis[i] == 0){
                flag = 1;
                if(choicesInLayer[nums[i]+100] == 0)
                {
                    record.push_back(nums[i]);
                    vis[i] =1;     
                    choicesInLayer[nums[i]+100] =1;
                    dfs(nums,vis);
                    vis[i]=0;
                    record.pop_back();
                }
            }
        }
        if(flag == 0){
            ans.push_back(record);
        }
    }
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        len = nums.size();
        vector<int> vis;
        for(int i=0;i<len;i++) vis.push_back(0);
        dfs(nums,vis);
        return ans;
    }
};
```
## 题目链接：  
https://leetcode-cn.com/problems/permutations-ii/