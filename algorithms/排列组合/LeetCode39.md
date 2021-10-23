---
title: 组合总和---LeetCode39(wsl)
date: 2020-09-09 09:10:02
tags: [排列组合,回溯,dfs]
---
## 题目描述：  
给定一个无重复元素的数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的数字可以无限制重复被选取。
说明：
所有数字（包括 target）都是正整数。
解集不能包含重复的组合。 

<!-- more -->

## 示例：   
```cpp
示例 1：
输入：candidates = [2,3,6,7], target = 7,
所求解集为：
[
  [7],
  [2,2,3]
]

示例 2：
输入：candidates = [2,3,5], target = 8,
所求解集为：
[
  [2,2,2,2],
  [2,3,3],
  [3,5]
]
```

## 解题思路:  
这道题的重点就是在于可重复吧，除了这个没什么好说的。  
### 错误示范
最开始我没看到可重复，然后就写了一个无重复版本的，后来将其改为了可以有重复元素版本，可以见代码如下：
可以看到，我在可以选择该元素里面写了两个dfs(其实是加了一个),粗略一想，选择该元素时，可以去下一个节点，也可以不去嘛；不选择该元素时，直接去下一个节点。。。。没毛病。  
确实没毛病，但是这样写就会有重复元素(这里不过多解释，稍微画一个图就很清楚了)。  
没办法，只好加一个set去重，险过。  
```cpp
class Solution {
public:
    vector<vector<int>> ans;
    int len;
    int Target;
    vector<int> record;
    void dfs(vector<int>& candidates,int pos,int sum){
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
        //不选择当前位置
        dfs(candidates,pos+1,sum);

        //选择当前位置
        record.push_back(candidates[pos]);
        dfs(candidates,pos+1,sum+candidates[pos]);
        dfs(candidates,pos,sum+candidates[pos]);
        record.pop_back();
    }
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        record.clear();
        len = candidates.size();
        Target = target;
        dfs(candidates,0,0);
        //拙劣的去重
        set<vector<int>> s;
        for(auto x:ans){
            s.insert(x);
        }
        ans.clear();
        for(auto x:s){
            ans.push_back(x);
        }
        return ans;
    }
};
```

### 正确示范
再转而一想(一看题解)，在一个节点不选该元素->去下一个节点；选择该元素->原地不动。不就行了么，而且还不会重复。瞬间感觉自己是个zz。  
```cpp
class Solution {
public:
    vector<vector<int>> ans;
    int len;
    int Target;
    vector<int> record;
    void dfs(vector<int>& candidates,int pos,int sum){
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
        //不选择当前位置
        dfs(candidates,pos+1,sum);

        //选择当前位置
        record.push_back(candidates[pos]);
        dfs(candidates,pos,sum+candidates[pos]);
        record.pop_back();
    }
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        record.clear();
        len = candidates.size();
        Target = target;
        dfs(candidates,0,0);
        return ans;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/combination-sum/