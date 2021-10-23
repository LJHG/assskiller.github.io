---
title: 使用xor来找只出现了一次的数字---LeetCode-m56
date: 2020-04-28 17:16:40
tags: [位运算, 亦或]
---
### 题目描述：  
一个整型数组 nums 里除两个数字之外，其他数字都出现了两次。请写程序找出这两个只出现一次的数字。要求时间复杂度是O(n)，空间复杂度是O(1)。


### 示例：   
```cpp
示例 1：

输入：nums = [4,1,4,6]
输出：[1,6] 或 [6,1]
示例 2：

输入：nums = [1,2,10,4,1,4,3,3]
输出：[2,10] 或 [10,2]
 

限制：

2 <= nums <= 10000

```

### 解题思路:  
给两个解法，一个是排序后找只出现了一次的，还有一个是用亦或运算，其实应该还可以用哈希映射来做，但空间复杂度有点高。这道题和joma那个视频不是很像吗2333。

### 排序后找只出现了一次的
排序后如果出现了两次的会相邻，根据这个特性，遍历一次就可以找出只出现了一次的

```cpp
class Solution {
public:
    vector<int> singleNumbers(vector<int>& nums) {
        sort(nums.begin(),nums.end());
        vector<int> ans;
        for(int i=0;i<nums.size();i++)
        {
            if(i == nums.size()-1)
            {
                if(nums[i] != nums[i-1])
                {
                    ans.push_back(nums[i]);
                }
            }
            else{
                if(nums[i] == nums[i+1])
                {
                    i++;
                }
                else{
                    ans.push_back(nums[i]);
                }
            }
        }
        return ans;
    }
};
```

<br/>
<br/>

### 采用xor来做
只出现过一次的数字，可以通过亦或找出来，但是这里有两个数字，所以找出来的结果是两个结果的抑或，所以需要将两个结果分开，分成两组，然后分别亦或找出结果。而要区别这两个结果，这两个数可以通过亦或结果里的1来区分，这里取最低位的1。  
注意与运算和==运算的优先级，与要加括号。  

```cpp
class Solution {
public:
    int lowbit(int x)
    {
        return x&(-x);
    }

    vector<int> singleNumbers(vector<int>& nums) {
        vector<int> ans;
        int xorResult = 0;
        int length = nums.size();
        for(int i=0;i<length;i++)
            xorResult ^= nums[i];
        //这里计算出来的xorResult是那两个不同的数抑或出来的结果，下面要找出这两个数
        //这两个数可以通过亦或结果里的1来区分，这里取最低位的1
        int diff= lowbit(xorResult);
        int ans1 = 0;
        int ans2 = 0;
        for(int i=0;i<length;i++)
        {
            //这里与要加括号，优先级的问题
            if( (diff & nums[i]) == 0)
            {
                ans1 ^= nums[i];
            }
            else
            {
                ans2 ^= nums[i];
            }
        }
        ans.push_back(ans1);
        ans.push_back(ans2);
        return ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/