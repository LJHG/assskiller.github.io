---
title: 山顶数组中查找目标值(二分法) --LeetCode1095
date: 2020-04-29 17:14:45
tags: [二分, BinarySerach]
---
## 题目描述：  
（这是一个 交互式问题 ）

给你一个 山脉数组 mountainArr，请你返回能够使得 mountainArr.get(index) 等于 target 最小 的下标 index 值。

如果不存在这样的下标 index，就请返回 -1。

 

何为山脉数组？如果数组 A 是一个山脉数组的话，那它满足如下条件：

首先，A.length >= 3

其次，在 0 < i < A.length - 1 条件下，存在 i 使得：

A[0] < A[1] < ... A[i-1] < A[i]
A[i] > A[i+1] > ... > A[A.length - 1]
 

你将 不能直接访问该山脉数组，必须通过 MountainArray 接口来获取数据：

MountainArray.get(k) - 会返回数组中索引为k 的元素（下标从 0 开始）
MountainArray.length() - 会返回该数组的长度
 

注意：

对 MountainArray.get 发起超过 100 次调用的提交将被视为错误答案。此外，任何试图规避判题系统的解决方案都将会导致比赛资格被取消。

为了帮助大家更好地理解交互式问题，我们准备了一个样例 “答案”：https://leetcode-cn.com/playground/RKhe3ave，请注意这 不是一个正确答案。

### 示例：   
```cpp
示例 1：

输入：array = [1,2,3,4,5,3,1], target = 3
输出：2
解释：3 在数组中出现了两次，下标分别为 2 和 5，我们返回最小的下标 2。
示例 2：

输入：array = [0,1,2,4,2,1], target = 3
输出：-1
解释：3 在数组中没有出现，返回 -1。
 

提示：

3 <= mountain_arr.length() <= 10000
0 <= target <= 10^9
0 <= mountain_arr.get(index) <= 10^9

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-in-mountain-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

### 解题思路:  
这道题不能直接从头到尾遍历，因为题目说请求index的数据过多会报错，所以明显只能二分。  
先通过二分找出山顶位置，然后在山顶位置前二分找出第一个答案，山顶位置后找出第二个答案就可以了。  
注意山顶前的排序是从小到大，山顶后的排序是从大到小，两个的二分是反着来的。

```cpp
/**
 * // This is the MountainArray's API interface.
 * // You should not implement it, or speculate about its implementation
 * class MountainArray {
 *   public:
 *     int get(int index);
 *     int length();
 * };
 */

int binarySerach(MountainArray &mountainArr, int target, int start, int end)
{
    int left = start;
    int right = end;
    int middle = 0;
    while(left <= right)
    {
        middle = (left+right) /2;
        if(mountainArr.get(middle) == target)
            return middle;
        if(target < mountainArr.get(middle))
        {
            right = middle -1;
        }
        else
        {
            left = middle+1;
        }
    }
    return -1;
}

int reverseBinarySerach(MountainArray &mountainArr, int target, int start, int end)
{
    int left = start;
    int right = end;
    int middle = 0;
    while(left <= right)
    {
        middle = (left+right) /2;
        if(mountainArr.get(middle) == target)
            return middle;
        if(target < mountainArr.get(middle))
        {
            left = middle+1;
        }
        else
        {
            right = middle -1;
        }
    }
    return -1;
}




class Solution {
public:
    int findInMountainArray(int target, MountainArray &mountainArr) {
        int length = mountainArr.length();
        //find moutain top
        int left = 1; //山顶不会出现在0或者length-1
        int right = length -2;
        int middle = 0;
        int moutainTopIndex = 0;
        while(1)
        {
            //left =1  right = 2 middle = 1
            middle = (left+right)/2;
            //山顶不会出现在0或者length-1
            int curLeft = mountainArr.get(middle-1);
            int cur = mountainArr.get(middle);
            int curRight = mountainArr.get(middle+1);
            if(cur > curLeft && cur > curRight)
            {
                moutainTopIndex = middle;
                break;
            }
            else if(curLeft < cur && cur < curRight)
            {
                //左边山
                left = middle +1;
            }
            else if(curLeft > cur && cur > curRight)
            {
                ///右边山
                right = middle -1;
            }
        }
        cout<<"length: "<<length<<endl;
        cout<<"山顶的index是： "<<moutainTopIndex<<endl;

        //找到山顶的index后，分两边二分查找
        int leftAnsIndex = -1;
        int rightAnsIndex = -1;
        leftAnsIndex = binarySerach(mountainArr,target,0,moutainTopIndex);
        rightAnsIndex = reverseBinarySerach(mountainArr,target,moutainTopIndex+1,length-1);
        cout<<leftAnsIndex<<" "<<rightAnsIndex;
        if(leftAnsIndex != -1)
            return leftAnsIndex;
        else
        {
            if(rightAnsIndex != -1)
                return rightAnsIndex;
            return -1;
        }
    }
};

```

### 题目链接：  
https://leetcode-cn.com/problems/find-in-mountain-array/