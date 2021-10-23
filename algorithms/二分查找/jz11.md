---
title: 剑指 Offer 11. 旋转数组的最小数字---(二分)
date: 2020-07-22 10:43:17
tags: [二分]
---
## 题目描述：  
把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。输入一个递增排序的数组的一个旋转，输出旋转数组的最小元素。例如，数组 [3,4,5,1,2] 为 [1,2,3,4,5] 的一个旋转，该数组的最小值为1。

## 示例：   
```cpp
示例 1：
输入：[3,4,5,1,2]
输出：1

示例 2：
输入：[2,2,2,0,1]
输出：0
```
<!-- more -->

## 解题思路:
### 暴力遍历
这不是遍历一下就完事了嘛，有什么好说的，其实也并不慢，都是O(n)了。

```cpp
class Solution {
public:
    int minArray(vector<int>& numbers) {
        int len = numbers.size();
        if(len == 1) return numbers[0];
        for(int i=1;i<len;i++){
            if(numbers[i] < numbers[i-1]){
                return numbers[i];
            }
        }
        return numbers[0];
    }
};
```

### 二分
但是既然都有序了，必然会二分。  
这里二分我的思路是看左边界和右边界，如果左边界比有边界要大，说明旋转点一定在其中(**其实并不是**，比如[3,3,1,3]，这个取第一次mid是3，然后就会出现两个左右都是3的子序列，然而明显旋转点在右边那个子序列中，所以后面我加了一个min，两边都走走看，然后取小的那个)  
这道题还要注意一下边界的判断，我这里是拿最后长度为2判定的，写得比较shit，判断得很迷，应该还有一些更好的做法。
```cpp
class Solution {
public:

    int binarySearch(int l,int r,vector<int>& numbers){
        if( l == r) return numbers[l];

        if(r-l == 1){
            if(numbers[l] < numbers[r]) return numbers[l];
            else return numbers[r];
        }

        if(numbers[l] >= numbers[r]){
            //左边的值比右边的大，说明旋转点在其中
            int mid = (l+r)/2;
            return min(binarySearch(l,mid,numbers),binarySearch(mid,r,numbers));
        }else{
            //旋转点不在其中
            return numbers[l];                                                
        }
        return numbers[l];
    }

    int minArray(vector<int>& numbers) {
        return binarySearch(0,numbers.size()-1,numbers);
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof/