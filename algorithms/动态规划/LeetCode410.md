---
title: 分割数组的最大值---LeetCode410(dp)
date: 2020-07-25 10:00:14
tags: [动态规划,dp]
---
## 题目描述：  
给定一个非负整数数组和一个整数 m，你需要将这个数组分成 m 个非空的连续子数组。设计一个算法使得这 m 个子数组各自和的最大值最小。

注意:
数组长度 n 满足以下条件:
1 ≤ n ≤ 1000
1 ≤ m ≤ min(50, n)


## 示例：   
```cpp
输入:
nums = [7,2,5,10,8]
m = 2

输出:
18

解释:
一共有四种方法将nums分割为2个子数组。
其中最好的方式是将其分为[7,2,5] 和 [10,8]，
因为此时这两个子数组各自的和的最大值为18，在所有情况中最小。
```
<!-- more -->

## 解题思路:  
呃哈哈，没看题解直接ac的感觉就是爽~。  
说一下这道题如何dp。  
dp[x][m]表示从位置x开始到最后分为m个子数组的最小最大值，之前也想过用dp[x][y][m]这种用来表示从位置x到y划分为m个子数组，但其实根本没有必要。仔细想一想，根本不会出现这种情况，因为我们对于一个数组，可以认为是选择一个位置切一刀，然后剩下的丢给后面，也就是说，切很多刀的情况，只会出现在(x,n)的子数组里。这里想明白了，就可以开始dp了。这道题还用了前缀和什么的，很简单，就不多说了。  
状态转移方程： dp[i][m] = min(dp[i][m],max(prefix[j]-prefix[i-1],dp[j+1][m-1]))

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int m) {
        long long dp[1001][51]; // dp[x][m]表示从下标为x到n-1,分为m个子数组的最小最大值
        long long  prefix[1001]; 
        prefix[0] = nums[0];
        int len = nums.size();
        for(int i=1;i<len;i++)
            prefix[i] = prefix[i-1] + nums[i];
        
        //初始化dp
        for(int i=0;i<len;i++){
            for(int M=1;M<=m;M++)
                dp[i][M]=4294967295;
        }
        for(int i=0;i<len;i++){
            if(i==0)
                dp[0][1] = prefix[len-1];
            else
                dp[i][1] = prefix[len-1] - prefix[i-1];
        }

        for(int M=2;M<=m;M++){
            for(int i=0;i<len;i++)
            {
                for(int j=i;j<len-1;j++){
                    //在下标为j的地方切一刀，分为 i...j 和 j+1...n-1两个子数组
                    long long  left = 0;
                    long long right = 0;
                    if(i==0){
                        left = prefix[j];
                    }else{
                        left = prefix[j]-prefix[i-1];
                    }
                    right = dp[j+1][M-1];
                    dp[i][M] = min(dp[i][M],max(left,right));
                }
            }
        }
        return dp[0][m];
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/split-array-largest-sum/