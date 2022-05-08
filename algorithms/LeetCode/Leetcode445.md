---
title: Leetcode445 两数相加(Stack)
date: 2020-04-22 20:32:36
tags: [STL, Stack]
---
### 题目描述：  
给你两个 非空 链表来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储一位数字。将这两数相加会返回一个新的链表。

你可以假设除了数字 0 之外，这两个数字都不会以零开头。

进阶： 

如果输入链表不能修改该如何处理？换句话说，你不能对列表中的节点进行翻转。

### 示例：   
```cpp
输入：(7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 8 -> 0 -> 7
```

### 解题思路:  
看到这种需要倒过来加的，就去用Stack

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */

 //使用栈
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* ans = NULL;
        stack<int> s1;
        stack<int> s2;
        while(l1 != NULL)
        {
            s1.push(l1->val);
            l1 = l1 ->next;
        }
        while(l2 != NULL)
        {
            s2.push(l2->val);
            l2 = l2 ->next;
        }

        int c = 0;
        while(!s1.empty() || !s2.empty() || c!=0)
        {
            int add1 = 0;
            int add2 = 0;

            if(!s1.empty())
            {
                add1 += s1.top();
                s1.pop();
            } 
            if(!s2.empty())
            {
                add2 += s2.top();
                s2.pop();
            }

            int sum = add1 +add2 + c;
            c = 0;
            while(sum>=10)
            {
                c++;
                sum -= 10;
            }
            ListNode* tmpNode  =new ListNode();
            tmpNode->val = sum;
            tmpNode->next = ans;
            ans = tmpNode;
        }  
    return ans;        
        
    }
};
```
