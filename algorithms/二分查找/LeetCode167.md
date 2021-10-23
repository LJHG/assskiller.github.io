---
title: 两数之和 II - 输入有序数组---LeetCode167(二分或双指针)
date: 2020-07-20 10:14:49
tags: [二分,双指针]
---
## 题目描述：  
给定一个已按照升序排列 的有序数组，找到两个数使得它们相加之和等于目标数。
函数应该返回这两个下标值 index1 和 index2，其中 index1 必须小于 index2。

说明:
返回的下标值（index1 和 index2）不是从零开始的。
你可以假设每个输入只对应唯一的答案，而且你不可以重复使用相同的元素。

## 示例：   
```cpp
输入: numbers = [2, 7, 11, 15], target = 9
输出: [1,2]
解释: 2 与 7 之和等于目标数 9 。因此 index1 = 1, index2 = 2 
```

## 解题思路:  
### 二分
看到了有序基本上就是要二分了，最开始我还天真地试了一发遍历O(n²)，果不其然超时了。
二分也没什么好说的，就是固定左边的index，去找右边的那个值。

```cpp
class Solution {
public:

    
    vector<int> twoSum(vector<int>& numbers, int target) {
        vector<int> ans;
        int len = numbers.size();
        for(int index1=0;index1<len-1;index1++){
            int left = index1+1;
            int right = len-1;
            int mid = (left+right)/2;

            while(1)
            {
                mid = (left+right) /2;
                int curVal = numbers[index1]+numbers[mid];
                if(curVal == target){
                    ans.push_back(index1+1);
                    ans.push_back(mid+1);
                    return ans;
                }else if(curVal < target){
                    if(left == right) break;
                    left = mid+1;
                }else{
                    if(left == right) break;
                    right = mid;
                }
            }

        }
            return ans;
        }
};
```

### 双指针 
这道题双指针的的写法很简单，就是指针分别指向左右，如果当前值小了，就移动左指针；如果当前值大了，就移动右指针。  
方法很简单，但我觉得该方法的证明还挺巧妙的。  
[证明见官方题解](https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/solution/liang-shu-zhi-he-ii-shu-ru-you-xu-shu-zu-by-leet-2/)

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int left=0;
        int right = numbers.size()-1;
        int sum = 0;
        while(1){
            sum = numbers[left] +numbers[right];
            if(sum > target){
                right --;
            }else if(sum < target){
                left ++;
            }else{
                vector<int> ans;
                ans.push_back(left+1);
                ans.push_back(right+1);
                return ans;
            }
        }
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/