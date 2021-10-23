---
title: 乘积最大子数组---LeetCode152(不会真的有人以为是前缀和吧)
date: 2020-05-18 13:39:27
tags: []
---
### 题目描述：  
给你一个整数数组 nums ，请你找出数组中乘积最大的连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。

### 示例：   
```cpp
示例 1:
输入: [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。

示例 2:
输入: [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。
```
<!-- more -->
### 解题思路:  
这道题第一眼看以为是前缀和，秒了!  
然后越写越不对劲，后来发现可能是dp，然后写了一个虚假的dp，再最后发现dp也不需要，搞两个变量记录一下步就行了嘛。  
下面展示一下我是如何一步步优化的。 
ps: 这道题的精髓就是，要使用两个变量来记录，一个最大，一个最小，因为是乘法，所以最大可能下一次就变成最小，最小可能下一次就变成最大，所以都要记录一下。   
### 虚假的dp
因为计算每一个点时都需要用到前面的，自然而然的想到了dp。 
```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        pair<int,int> dp[100000]; //dp[i]表示到i为止的最大值,最小值
        dp[0] = make_pair(nums[0],nums[0]);
        int length = nums.size();
        int ans=nums[0];
        for(int i=1;i<length;i++)
        {
            
            int a = dp[i-1].first*nums[i];
            int b = dp[i-1].second*nums[i];

            int mulMax = max(a,b);
            mulMax = max(mulMax,nums[i]);
            int mulMin = min(a,b);
            mulMin = min(mulMin,nums[i]);
            dp[i].first = mulMax;
            dp[i].second = mulMin;

            ans = max(mulMax,ans);
        }
        return ans;    
    }
};
```


</br>

### 要什么dp
但是每次都是只需要前一次的数据，那还要什么dp，白费内存，直接搞两个变量记录一下呗。
```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int curMax = nums[0];
        int curMin = nums[0];
        int length = nums.size();
        int ans=nums[0];
        int a,b,mulMax,mulMin;
        for(int i=1;i<length;i++)
        {  
            a = curMax*nums[i];
            b = curMin*nums[i];
            mulMax = max(a,b);
            mulMax = max(mulMax,nums[i]);
            mulMin = min(a,b);
            mulMin = min(mulMin,nums[i]);
            curMax = mulMax;
            curMin = mulMin;
            ans = max(mulMax,ans);
        }
        return ans;    
    }
};
```


</br>

### 连比较都不用了
如果是Nums[i]是负数，那么最大就会变成最小，最小就会变成最大。不然最大还是最大，最小还是最小，所以循环体里面是不用比较的。
```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int curMax = nums[0];
        int curMin = nums[0];
        int length = nums.size();
        int ans=nums[0];
        for(int i=1;i<length;i++)
        {  
            if(nums[i] < 0 )
            {
                int temp = curMax;
                curMax = curMin;
                curMin = temp;
            }
            curMax = max(curMax*nums[i],nums[i]);
            curMin = min(curMin*nums[i],nums[i]);
            ans = max(curMax,ans);
        }
        return ans;    
    }
};
```


总而言之，这道题和前缀和没半点关系。
### 题目链接：  
https://leetcode-cn.com/problems/maximum-product-subarray/