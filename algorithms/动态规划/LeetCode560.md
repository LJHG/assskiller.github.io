---
title: 找和为k连续子数组---LeetCode560(前缀和+哈希优化)
date: 2020-05-15 17:07:05
tags: [前缀和, prefix]
---
### 题目描述：  
给定一个整数数组和一个整数 k，你需要找到该数组中和为 k 的连续的子数组的个数。

### 示例：   
```cpp
示例 1 :
输入:nums = [1,1,1], k = 2
输出: 2 , [1,1] 与 [1,1] 为两种不同的情况。

说明 :
数组的长度为 [1, 20,000]。
数组中元素的范围是 [-1000, 1000] ，且整数 k 的范围是 [-1e7, 1e7]。
```
<!-- more -->

### 解题思路:  
这道题一看就是前缀和，但是没有想到前缀和还可以加上哈希表再优化。  
这里贴三种做法：暴力，前缀和，前缀和+哈希表优化
### 暴力
暴力法要注意可以通过sum的累加来让它不那么暴力，当然一步到位的还是前缀和。
```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        int count = 0;
        for (int start = 0; start < nums.size(); ++start) {
            int sum = 0;
            for (int end = start; end >= 0; --end) {
                sum += nums[end];
                if (sum == k) {
                    count++;
                }
            }
        }
        return count;
    }
};
```

### 前缀和
一开始想到的就是这个方法，抱着试一试的心态就直接过了
```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        //前缀和？
        int prefix[20050];
        prefix[0] = nums[0];
        int length = nums.size();
        for(int i=1;i<length;i++)
        {
            prefix[i] = prefix[i-1] + nums[i];
        }
        
        int ans=0;
        for(int i=0;i<length;i++)
        {
            for(int j=i;j>=0;j--)
            {
                //求i 到 j的和
                int temp=0;
                if(j-1 >= 0) temp=prefix[i] - prefix[j-1];
                else temp = prefix[i];
                if(temp == k) ans++;
            }
        }
        return ans;
    }
};
```

### 前缀和+哈希表
这个真的没想到了，首先，用这种方法都不用事先把前缀和求出来，因为他是一步一步推上去的。  
同时，这里这个m[i]的意思是，当前前缀和为i的数量有几个。 
解释得更清楚一些：  
目标是找出 prefix[i] - prefix[j-1] == k  
经过移项可以得到 prefix[i] - k == prefix[j-1]  
所以要找出**index为i时，子数组和为k**，就是要找出**i之前前缀和为prefix[i]-k**的情况，而这里的prefix[i]就直接使用sum来代替了。  
ps：需要设置一个m[0]=1，即表示初始化前缀和为0的数量为1。

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        map<int,int> m; // m[i]代表前缀和为i的个数
        int length = nums.size();
        int ans = 0;
        int sum=0;
        m[0] = 1;
        for(int i=0;i<length;i++)
        {
            sum += nums[i];
            ans += m[sum-k];
            m[sum]++;
        }
        return ans;   
    }
};
```
### 题目链接：  
https://leetcode-cn.com/problems/subarray-sum-equals-k/