---
title: 第k个排列---LeetCode60(优化的力量)
date: 2020-09-05 11:21:25
tags: [dfs,递归,全排列,数学,剪枝]
---
## 题目描述：  
给出集合 [1,2,3,…,n]，其所有元素共有 n! 种排列。
按大小顺序列出所有排列情况，并一一标记，当 n = 3 时, 所有排列如下：
"123"
"132"
"213"
"231"
"312"
"321"
给定 n 和 k，返回第 k 个排列。
说明：
给定 n 的范围是 [1, 9]。
给定 k 的范围是[1,  n!]。

## 示例：   
```cpp
示例 1:
输入: n = 3, k = 3
输出: "213"

示例 2:
输入: n = 4, k = 9
输出: "2314"
```
<!-- more -->

## 解题思路:  
dfs五分钟，优化两小时。  
这道题还可以用数学的方法做，这里就不列出来了，这里主要说dfs。  
直接无脑dfs会超时的，超的很惨，这里就不列出来了，我改了超级多最后才ac，说一下优化的几个点吧。  
1. 最开始我是想从数字中直接看出这个数的顺序是第几个，其实应该是做得到的，但是我做的时候搞成幂了，一直在纠结次方什么的，其实这道题是阶乘啊。我们这里主要说dfs，所以偏数学的就不考虑了，最后采用的方法是使用一个count来记录当前的顺序。(使用一个全局的count来记录，这种方法其实也不赖)。  
2. 剪枝。如果当前的cnt+后面所有未访问数的全排列小于k，那么说明暂时还到不了k，直接剪掉。  
3. 记录访问了哪些元素最好还是传引用，用回溯法。切记不要传一个vector然后在那里复制啊，删除啊什么的，太蠢了。  
4. 记录结果时不要用string在dfs中传参，奇慢无比(不知道为啥)，改成数组记录结果后就过了。  

真优化吐了，可能本来就不是什么好方法吧，不过是把一坨💩打扮得好看了一点。  
```cpp
class Solution {
public:
    int target;
    string ans;
    int count =0;
    int factor[10]={1,1,2,6,24,120,720,5040,40320,362880};
    int record[10];
    void dfs(vector<int>& vis,int unvisited,int recordi){
        int len = vis.size();
        if(count + factor[unvisited] < target) { //剪枝1
            count += factor[unvisited];
            return;
        }
        
        if(unvisited == 1){
            count++;
            for(int i=0;i<len;i++)
                if(!vis[i]){
                    record[recordi] =i+1;
                    break;
                }
            
            if(count == target){
                for(int i=0;i<vis.size();i++){
                    ans += to_string(record[i]);
                }
                return;
            }
            return;
        }
        for(int i=0;i<len;i++){
            if(!vis[i]){
                record[recordi] =i+1;
                vis[i] = 1;
                dfs(vis,unvisited-1,recordi+1);
                vis[i] = 0;
            }
            
        }
    }

    string getPermutation(int n, int k) {
        //我觉得可以用一种更加数学的方式来解，不过有点难想，我要递归了
        memset(record,0,sizeof(record));
        target = k;
        count = 0;
        vector<int> vis;
        for(int i=1;i<=n;i++) vis.push_back(0);
        string hhh="";
        dfs(vis,n,0);
        return ans;
    }   
};
```

## 题目链接：  
https://leetcode-cn.com/problems/permutation-sequence/