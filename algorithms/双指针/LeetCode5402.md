---
title: 绝对值差不超过限制的最长连续子数组---LeetCode5402
date: 2020-05-03 17:13:43
tags: [滑动窗口, 双指针, two pointers, set]
---
### 题目描述：  
给你一个整数数组 nums ，和一个表示限制的整数 limit，请你返回最长连续子数组的长度，该子数组中的任意两个元素之间的绝对差必须小于或者等于 limit 。

如果不存在满足条件的子数组，则返回 0 。

### 示例：   
```cpp
示例 1：
    输入：nums = [8,2,4,7], limit = 4
    输出：2 
    解释：所有子数组如下：
    [8] 最大绝对差 |8-8| = 0 <= 4.
    [8,2] 最大绝对差 |8-2| = 6 > 4. 
    [8,2,4] 最大绝对差 |8-2| = 6 > 4.
    [8,2,4,7] 最大绝对差 |8-2| = 6 > 4.
    [2] 最大绝对差 |2-2| = 0 <= 4.
    [2,4] 最大绝对差 |2-4| = 2 <= 4.
    [2,4,7] 最大绝对差 |2-7| = 5 > 4.
    [4] 最大绝对差 |4-4| = 0 <= 4.
    [4,7] 最大绝对差 |4-7| = 3 <= 4.
    [7] 最大绝对差 |7-7| = 0 <= 4. 
    因此，满足题意的最长子数组的长度为 2 。

示例 2：
    输入：nums = [10,1,2,4,7,2], limit = 5
    输出：4 
    解释：满足题意的最长子数组是 [2,4,7,2]，其最大绝对差 |2-7| = 5 <= 5 。

示例 3：
    输入：nums = [4,2,2,2,4,4,2,2], limit = 0
    输出：3

提示：
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^9
    0 <= limit <= 10^9

```
<!--more-->

### 解题思路:  
这道题我用了两种方法，一个是暴力法，一个是滑动窗口法，暴力法是直接超时了。

### 暴力法
就是对每个字符开始找最长，基本操作，这道题会TLE。(没错，我差点又做成DFS，疯了吧)。

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        //维护当前子数组最小和最大，每次加进来一个数字，如果大，就和最小的比，如果小，就和最大的比，在中间就不用比
        
        //这道题dfs必超时，我都懒得了
        
        //遍历吧
        int curmin =0;
        int curmax =0;
        int length = nums.size();
        int ans =1;
        for(int i=0;i<length;i++)
        {
            curmin = nums[i];
            curmax = nums[i];
            
            for(int j=i+1;j<length;j++)
            {
                if(nums[j] > curmax)
                {
                    if(nums[j] - curmin > limit)
                    {
                        break;
                    }
                    else
                    {
                        curmax = nums[j];
                        ans = ((j-i+1)>ans)?j-i+1:ans;
                    }
                }
                else if(nums[j] < curmin)
                {
                    if(curmax - nums[j] > limit)
                    {
                        break;
                    }
                    else
                    {
                        curmin = nums[j];
                        ans = ((j-i+1)>ans)?j-i+1:ans;
                    }
                }
                else
                {
                    //在中间
                    ans = ((j-i+1)>ans)?j-i+1:ans;
                }
            }
        }
        return ans;

    }
};
```

<br/>

### 滑动窗口法
暴力法挂了后，我很快就想到了滑动窗口，但是在写的过程中，不知道应该怎样去维护一个当前的最大最小值，所以最后也没有写出来。  
下来后去看了看题解，发现有用优先队列的，于是又用优先队列写了一下，发现优先队列不能删除指定元素，遂放弃。  
于是又看了一下，发现有用multiset的，这东西我第一次见，反正就是一个有序而且可以重复的set,amazing,于是就用了multiset。  
plus，这次我对于滑动窗口的写法较之前做了很大的改进，之前是**移动了右边后，看是否满足要求，不然就左移直到满足要求**。现在看来根本没必要啊，**左移时，也可以同时右移**，因为求的是最大长度，所以没有必要在左移时不右移，这样求出来满足了要求也一定比之前的长度短。

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        //滑动窗口+multiset
        //因为优先队列不能删指定元素，转而来用multiset
        multiset<int> curSet;
        int left = 0;
        int right = 0;
        int ans = 0;
        int length = nums.size();
        while(right < length)
        {
            curSet.insert(nums[right]);
            if(*curSet.rbegin() - *curSet.begin() <= limit)
            {
                ans = (right-left+1)>ans?right-left+1:ans;
            }
            else
            {
                left++;
                curSet.erase(curSet.find(nums[left-1]));
            }
            right++;
        }
        return ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/