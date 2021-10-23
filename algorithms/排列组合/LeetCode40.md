---
title: 组合总和2---LeetCode40(答案去重)
date: 2020-09-10 11:31:58
tags: [排列组合,dfs,回溯]
---
## 题目描述：  

给定一个数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的每个数字在每个组合中只能使用一次。

说明：
所有数字（包括目标数）都是正整数。
解集不能包含重复的组合。
<!-- more -->

## 示例：   
```cpp
示例 1:
输入: candidates = [10,1,2,7,6,1,5], target = 8,
所求解集为:
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]

示例 2:
输入: candidates = [2,5,2,1,2], target = 5,
所求解集为:
[
  [1,2,2],
  [5]
]
```

## 解题思路:  
这道题大体和其他几道组合差不多，重点就是答案如何去重 比如 1 1 2 和 1 2 1，这种就是重复的。  
去重的方法很简单，如果前面选了1，后面才能选，如果没有选，那么后面就都不要选。  
感觉没啥毛病，但运行得有点慢。  
```cpp
class Solution {
public:
    vector<vector<int>> ans;
    int len;
    int Target;
    vector<int> record;
    void dfs(vector<int>& candidates,int pos,int sum,map<int,int>& unvis){
        if(pos >= len){
            if(sum == Target){
                ans.push_back(record);
            }
            return;
        }
        if(sum == Target) {
            ans.push_back(record);
            return;
        }
        if(sum > Target){
            return;
        }

        //如果当前位置unvis>0,那么就不能选(如果你前面没有选这个数，那么后面都别选了)
        if(unvis[candidates[pos]] >=1){
            dfs(candidates,pos+1,sum,unvis);
        }else{
            //可以选这一个地方 
            record.push_back(candidates[pos]);
            dfs(candidates,pos+1,sum+candidates[pos],unvis);
            record.pop_back();
            //也可以不选这个地方
            unvis[candidates[pos]] ++;
            dfs(candidates,pos+1,sum,unvis);
            unvis[candidates[pos]] --;

        }
        
    }
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        record.clear();
        len = candidates.size();
        Target = target;
        map<int,int> unvis;
        dfs(candidates,0,0,unvis);
        return ans;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/combination-sum-ii/