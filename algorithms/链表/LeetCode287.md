---
title: 寻找重复数---LeetCode287(快慢指针)
date: 2020-05-26 15:57:34
tags: [快慢指针法]
---
## 题目描述：  
给定一个包含 n + 1 个整数的数组 nums，其数字都在 1 到 n 之间（包括 1 和 n），可知至少存在一个重复的整数。假设只有一个重复的整数，找出这个重复的数。

## 示例：   
```cpp
示例 1:
输入: [1,3,4,2,2]
输出: 2

示例 2:
输入: [3,1,3,4,2]
输出: 3
说明：
不能更改原数组（假设数组是只读的）。
只能使用额外的 O(1) 的空间。
时间复杂度小于 O(n2) 。
数组中只有一个重复的数字，但它可能不止重复出现一次。
```
<!-- more -->


## 解题思路:  
这道题一看就是快慢指针，但是这道题要涉及到快慢指针找到环的入口的问题。  
先给出结论，要找到环的入口（重复的节点），需要在相遇后，slow从起点开始，fast从相遇点开始继续走，两个指针都每次走一格，相遇时的点就是环的入口。
[具体证明去看leetcode官方题解  ](https://leetcode-cn.com/problems/find-the-duplicate-number/solution/xun-zhao-zhong-fu-shu-by-leetcode-solution/)  
同时要注意快慢指针的模板写法，最开始是把**快指针和慢指针初始化为0**，然后**使用一个do while循环来找相遇点**。  
以及要记住快慢指针的前提是**链表**，所以如果要把数组转换为一个链表，使用 **slow = nums[slow]** 这种方式就可以了。

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
       //快慢指针
       int length = nums.size();
       int slow = 0;
       int fast = 0;
       do{
           slow = nums[slow];
           fast = nums[nums[fast]];
       }while(slow != fast);
       slow = 0;
       while(1)
       {
           if(slow == fast)
           {
               return slow;
           }
           slow = nums[slow];
           fast = nums[fast];
       }
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/find-the-duplicate-number/