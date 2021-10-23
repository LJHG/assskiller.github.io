---
title: 寻找两个正序数组的中位数---LeetCode04(噩梦级边界判断)
date: 2020-05-24 13:35:56
tags: [二分]
---
## 题目描述：  
给定两个大小为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。
请你找出这两个正序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
你可以假设 nums1 和 nums2 不会同时为空。

## 示例：   
```cpp
示例 1:
nums1 = [1, 3]
nums2 = [2]
则中位数是 2.0

示例 2:
nums1 = [1, 2]
nums2 = [3, 4]
则中位数是 (2 + 3)/2 = 2.5
```
<!-- more -->

## 解题思路:  
这道题首先可以看到复杂度是O(log(m + n))，所以一般用的像归并，以及双指针的方法就不行了。这道题一看就是二分，但是一开始我也没看懂怎么二分，最后就直接看题解了。  
这道题首先要把问题进行一个转换，要找到中位数实际上就是要找到第k个数，这里的k是 (length1+length2+1)/2 和 (length1+length2+2)/2，这里之所以要取两个k是因为奇数个数的中位数和偶数个数的中位数可以通过这种方法来进行一个统一。在奇数的情况下，(length1+length2+1)/2和(length1+length2+2)/2是相同的，在偶数的情况下，(length1+length2+1)/2和(length1+length2+2)/2就是中间的那两个数。所以两个加起来除以2就是最终答案。  
知道了这道题的本质就是找到第k个数后，就可以开始二分了。这道题的二分非常巧妙，就是拿两个数组的第k/2个数进行比较，小的那个数组的第k/2个数以及前面的全部数都不可能是第k个数了，所以就把前面舍去(就是更新offset)，然后更新k，最后就相当于两个新的数组，找到新的第k个数(递归)。(这里面涉及了非常多的边界判定，说不清楚了，具体的见注释吧。)

```cpp
class Solution {
public:
    int findKSmallestNum(vector<int>& nums1, vector<int>& nums2, int offset1,int offset2,int k)
    {
        int length1 = nums1.size();
        int length2 = nums2.size();
        //如果数组为空，那么就直接返回
        if(offset1 >= length1)
        {
            return nums2[offset2+k-1];
        }
        if(offset2 >= length2)
        {
            return nums1[offset1+k-1];
        }
        //如果数组越界，取越界数组的最后一个元素来和另一个的k/2来比
        if(offset1 + k/2 -1  >= length1)
        {
            //如果越界的最后一个更小
            if(nums1[length1-1] < nums2[offset2 + k/2 -1])
            {
                k = k - (length1-offset1);
                return nums2[offset2+k-1];
            }
            else
            {
                offset2 += k/2;
                k -= k/2;
                return findKSmallestNum(nums1,nums2,offset1,offset2,k);
            }
        }
        if(offset2 + k/2 -1 >= length2)
        {
            if(nums2[length2-1] < nums1[offset1 + k/2 -1])
            {
                //如果越界的最后一个更小
                k = k - (length2-offset2);
                return nums1[offset1+k-1];
            }
            else
            {
                offset1 += k/2;
                k -= k/2;
                return findKSmallestNum(nums1,nums2,offset1,offset2,k);
            }
        }
        //如果k为1，直接返回两个数组的开头两个的最小的那个
        if(k==1) return min(nums1[offset1],nums2[offset2]);
        //比较两个数组的k/2
        if(nums1[k/2+offset1-1] < nums2[k/2+offset2-1])
        {
            //nums1前面都不是第k小
            offset1 += k/2;
            k -= k/2;
        }
        else
        {
            offset2 += k/2;
            k -= k/2;
        }
        return findKSmallestNum(nums1,nums2,offset1,offset2,k);
    }

    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        //寻找第k小的数就是拿两个数组的k/2相比，小的那个数组的第k/2包括前面的都不可能是第k小的，然后把k -= k/2,再从新的数组开始找
        int length1 = nums1.size();
        int length2 = nums2.size();
        int offset1 = 0;
        int offset2 = 0;
        int k1 = (length1+length2+1) /2;
        int k2 = (length1+length2+2) /2;
        // cout<<"k1:"<<k1<<endl;
        // cout<<"k2:"<<k2<<endl;
        int a = findKSmallestNum(nums1,nums2,0,0,k1);
        int b = findKSmallestNum(nums1,nums2,0,0,k2);
        // cout<<a<<endl;
        // cout<<b<<endl;
        return ((double)a+ (double)b)/2;
    }
        
};
```

## 题目链接：  
https://leetcode-cn.com/problems/median-of-two-sorted-arrays/