---
title: Pow(x,n)---LeetCode50(快速幂)
date: 2020-05-11 14:32:42
tags: [快速幂]
---
### 题目描述：  
实现 pow(x, n) ，即计算 x 的 n 次幂函数。

<!-- more -->
### 示例：   
```cpp
示例 1:
输入: 2.00000, 10
输出: 1024.00000
```

### 解题思路:  
就是快速幂。快速幂的核心思想就是，通过把指数减半，底数平方来使得循环次数尽可能减少。

```cpp
//如果指数为奇数，底数与结果相乘。然后底数 = 底数*底数 ，指数 = 指数/2。这里其实是拿了一个底数^1与结果相乘，后面的当成偶指数情况变换。
//如果指数为偶数，直接 底数 = 底数*底数 ，指数 = 指数/2
double fastPow(double x,long long n)
{
    double res =1;
    while(n>0)
    {
        if(n&1)//如果n为奇数
        {
            res = res*x;
        }
        x = x*x;
        n = n>>1;
    }
    return res;
}
```

### 题目链接：  
https://leetcode-cn.com/problems/powx-n/  
[一个讲快速幂讲的很好的博客](https://blog.csdn.net/qq_19782019/article/details/85621386)