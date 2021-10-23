---
title: LeetCode69
date: 2020-05-09 22:04:14
tags: [二分, 牛顿迭代法]
---
## 题目描述：  
实现 int sqrt(int x) 函数。
计算并返回 x 的平方根，其中 x 是非负整数。
由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。
<!-- more -->

### 示例：   
```cpp
示例 1:
输入: 4
输出: 2
示例 2:

输入: 8
输出: 2
说明: 8 的平方根是 2.82842..., 
     由于返回类型是整数，小数部分将被舍去。
```

### 解题思路:  
正确方式：return sqrt(x) (雾)  
这里贴两种方法，二分法和牛顿迭代法

### 二分法
没什么好说的，注意一下left 和 right 每次是middle-1 和 middle+1，我以后二分都这么写了，不然一堆死循环。
class Solution {
public:
    int mySqrt(int x) {
        int l = 0, r = x, ans = -1;
        while (l <= r) {
            int mid = (l+r)/2;
            if ((long long)mid * mid <= x) {
                ans = mid;
                l = mid + 1;
            }
            else {
                r = mid - 1;
            }
        }
        return ans;
    }
};


### 牛顿迭代法
大佬做法，推式子，逼近零点。  
具体做法就是，先求出方程，要找零点。 
为此，先求初始化点(一个随便找的x)的切线方程，把与x轴的交点作为下一个x，然后一直迭代。  
[具体去看LeetCode题解吧](https://leetcode-cn.com/problems/sqrtx/solution/x-de-ping-fang-gen-by-leetcode-solution/)

```cpp
class Solution {
public:
    int mySqrt(int x) {
        if (x == 0) {
            return 0;
        }

        double C = x, x0 = x;
        while (true) {
            double xi = 0.5 * (x0 + C / x0);
            if (fabs(x0 - xi) < 1e-7) {
                break;
            }
            x0 = xi;
        }
        return int(x0);
    }
};

```

### 题目链接：  
https://leetcode-cn.com/problems/sqrtx/