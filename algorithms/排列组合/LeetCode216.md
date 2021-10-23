---
title: 组合总和3---LeetCode216
date: 2020-09-11 09:10:39
tags: [排列组合,回溯,dfs]
---
## 题目描述：  
找出所有相加之和为 n 的 k 个数的组合。组合中只允许含有 1 - 9 的正整数，并且每种组合中不存在重复的数字。
说明：
所有数字都是正整数。
解集不能包含重复的组合。 
<!-- more -->
## 示例：   
```cpp
示例 1:
输入: k = 3, n = 7
输出: [[1,2,4]]

示例 2:
输入: k = 3, n = 9
输出: [[1,2,6], [1,3,5], [2,3,4]]
```

## 解题思路:  
这道题真的，在经过这一周排列组合的轰炸下，太简单了。  
没什么好说的，只是记录一下，凑个全家福。  

```cpp
class Solution {
public: 
    vector<vector<int>> ans;
    int target;
    int K;
    vector<int> record;
    void dfs(int count,int pos,int sum){
        if(count > K || pos>10) return;
        if(count == K){
            if(sum == target){
                ans.push_back(record);
            }
            return;
        }
        //选择当前位置
        record.push_back(pos);
        dfs(count+1,pos+1,sum+pos);
        record.pop_back();
        //不选择当前位置
        dfs(count,pos+1,sum);
       
    }

    vector<vector<int>> combinationSum3(int k, int n) {
        target = n;
        K = k;
        dfs(0,1,0);
        return ans;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/combination-sum-iii/