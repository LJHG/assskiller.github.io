---
title: 下一个排列---LeetCode31(新的思路)
date: 2020-11-10 15:49:26
tags: [排列]
---
## 题目描述：  
实现获取下一个排列的函数，算法需要将给定数字序列重新排列成字典序中下一个更大的排列。
如果不存在下一个更大的排列，则将数字重新排列成最小的排列（即升序排列）。
必须原地修改，只允许使用额外常数空间。
<!-- more -->

## 示例：   
```cpp
以下是一些例子，输入位于左侧列，其相应输出位于右侧列。
1,2,3 → 1,3,2
3,2,1 → 1,2,3
1,1,5 → 1,5,1
```

## 解题思路:  
看到这道题就会想到很早以前做的一道第k个排列，不过这道题可以用这种做法会有点繁琐，可以用新的思路来做。  
求一个串的下一个排列，就是把这个串变得更大，而且是最接近的变大，也就是说，从后往前找，如果一个位后面有比他还大的，那么这一个位就可以变大。  
那么如何选择这个位变成哪一个数呢？很简单，从这个位往后遍历找比这个数大得最小的数就行了。  
变了后如何操作呢？swap一下，然后对**这个位后面排个序**就行了。

```cpp
class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        int len = nums.size();
        for(int i=len-1;i>=0;i--){
            int minPos = i;
            int minNum = 999999;
            for(int j=i+1;j<len;j++){
                if(nums[j] > nums[i] && nums[j] < minNum){
                    minPos = j;
                    minNum = nums[j];
                }
            }
            if(minPos != i){
                 //swap i and j 
                int temp = nums[i];
                nums[i] = nums[minPos];
                nums[minPos] = temp;
                //sort after j
                sort(nums.begin()+i+1,nums.end());
                return;
            }
        }
        sort(nums.begin(),nums.end());
        return;
    }
};
```

好久没写题解了，也好久没来图书馆了，来了图书馆就想写这些玩意。

## 题目链接：  
https://leetcode-cn.com/problems/next-permutation/