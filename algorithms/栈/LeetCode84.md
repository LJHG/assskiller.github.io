---
title: 柱状图中最大的矩形---LeetCode84(单调栈)
date: 2020-05-30 11:49:44
tags: [单调栈, stack]
---
## 题目描述：  
给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。
求在该柱状图中，能够勾勒出来的矩形的最大面积。

## 示例：
![](/images/leetcode84.png)
```cpp
输入: [2,1,5,6,2,3]
输出: 10
```
<!-- more -->
## 解题思路:  
最开始看到这道题以为是dp，然后写了半天递推公式发现是错的。  
这道题有两种解法，一种是暴力，一种是单调栈。

### 暴力
暴力的思想很简单，就是对于每一个位置中心展开就行了，时间复杂度是O(n^2)，但是这道题过不了。
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        //暴力
        int ans = 0;
        int length = heights.size();
        for(int i =0;i<length;i++)
        {
            int temp=heights[i];
            if(i>=1)
            {
                for(int j=i-1;j>=0;j--)
                {
                    if(heights[j] < heights[i])
                        break;
                    else
                        temp += heights[i];
                }
            }
            if(i<length-1)
            {
                for(int j=i+1;j<length;j++)
                {
                    if(heights[j] < heights[i])
                        break;
                    else
                        temp += heights[i];
                }
            }
            ans = max(ans,temp);
        }
        return ans;
    }
};
```

### 单调栈
一如既往的，看到栈就头晕，不过这次还是把这道题搞出来了。  
单调栈的方法是一直往栈中插入比当前栈顶元素大的元素(实际插入的是index，根据index也可以找出元素)，因为栈中的元素始终是递增的，所以叫做单调栈。  
如果当前元素碰到了比栈顶元素小，那么当前栈顶元素位置的最大面积就可以确定了(因为左右两边都比栈顶的长度小，所以可以确定展开的范围了)  
单调栈这种方法好就好在，不用每次都去中心展开遍历，当碰到比栈顶元素小需要确定答案时，右边界一定是当前元素，左边界一定是栈顶的下一个元素。从而就可以直接得出展开范围。  
需要注意的点是：  
1. 注意确定答案时的while循环。也就是说，当碰到比栈顶元素小需要确定答案时，只要栈顶元素比当前元素大，就可以确定答案，所以需要一直pop，直到不能确定答案。  
2. 注意当栈顶元素和当前元素相等时做的处理，把栈顶pop并加入当前元素。  
3. 在首尾加入height为0的元素，这样就不用做边界处理了，非常方便。  
大致就写这么多，总结一下，当遇到这种需要左右边界来确定答案时，可以用到单调栈。(其实为什么会想到这种方法我也不是很清楚，虽然题做完了，方法理解了，但是对于为什么会选择这种方法本身，还是存在疑惑)
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> s;
        s.push(0);
        int length = heights.size();
        if(length == 0) return 0;
        int ans = 0;
        heights.insert(heights.begin(),0); //前面添加一个0
        heights.push_back(0); //后面添加一个0
        length = heights.size();
        for(int i=1;i<length;i++)
        {
            int topNum = s.top();
            if(heights[i] > heights[topNum])
            {
                s.push(i);
            }
            else if(heights[i] == heights[topNum])
            {
                s.pop();
                s.push(i);
            }
            else
            {
                while(heights[s.top()] > heights[i])
                {
                    topNum = s.top();
                    s.pop();
                    int newTopNum = s.top();
                    ans = max(ans,(i-newTopNum-1)*heights[topNum]);
                    //cout<<i<<" "<<topNum<<" "<<ans<<endl;
                }
                s.push(i);
            }
        }
        return ans;
    }
};
```

## 题目链接：  
还不懂还可以再去看看官方题解。
https://leetcode-cn.com/problems/largest-rectangle-in-histogram/