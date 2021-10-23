---
title: 快乐数---LeetCode202判断链表环
date: 2020-04-30 11:31:22
tags: [链表找环, 快慢指针]
---
### 题目描述：  
编写一个算法来判断一个数 n 是不是快乐数。

「快乐数」定义为：对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。如果 可以变为  1，那么这个数就是快乐数。

如果 n 是快乐数就返回 True ；不是，则返回 False 。

### 示例：   
```cpp
输入：19
输出：true
解释：
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1
```

### 解题思路:  
这里给两个解题思路，一个是暴力法，一个是快慢指针法

### 暴力法
使用的方法就是用一个数组来存储已经走过的数据，如果再次访问，那么必定存在环。
```cpp
class Solution {
public:
    int flag[1000];
    bool isHappyFunc(int num)
    {
        while(num != 1)
        {
            //cout<<num<<" ";
            int sum = 0;
            while(num != 0)
            {
                sum += (num%10)*(num%10);
                num /= 10;
            }
            //cout<<endl;
            num = sum;
            if(flag[sum]==1)
                return false;
            flag[sum] = 1;
        }
        return true;           
    }
    bool isHappy(int n) {
        //memset(flag,0,sizeof(flag));
        return isHappyFunc(n);
    }
};
```

<br/>
<br/>

### 快慢指针法
快慢指针法也叫做弗洛伊德的龟兔法，可以用来判断链表中是否存在环，时间复杂度为O(n)。这道题实际上就是判断是否存在环。 
![图示](/images/Floyed'sR&T.png)
快指针每次移动两格，慢指针每次移动一格，如果存在环，即无线循环，那么快慢指针必定会相遇，return false, 否则快指针会先到达1，return true。

```cpp
class Solution {
public:

    int squareSum(int num)
    {
        int sum = 0;
        while(num != 0)
        {
            sum += (num%10)*(num%10);
            num /= 10;
        }
        return sum;
    }

    bool isHappy(int n) {
       //快慢指针法
       int fast = n;
       int slow = n;
       do{
            fast = squareSum(fast);
            fast = squareSum(fast);
            slow = squareSum(slow);
            if(fast == 1)
                return true;
       }while(fast != slow);
        return false;
    }
};

```

### 题目链接：  
https://leetcode-cn.com/problems/happy-number/