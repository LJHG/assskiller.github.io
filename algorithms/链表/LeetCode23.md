---
title: 合并K个排序链表
date: 2020-04-26 15:36:10
tags: [链表, list]
---
### 题目描述：  
合并 k 个排序链表，返回合并后的排序链表。请分析和描述算法的复杂度。

### 示例：   
```cpp
输入:
[
  1->4->5,
  1->3->4,
  2->6
]
输出: 1->1->2->3->4->4->5->6
```

### 解题思路:  
贴一个最简单粗暴的方法，就是比然后插，主要记录一下链表操作方法，其实这一道题我感觉我像搞了两个头节点一样，有点奇怪，也没想好怎么优化

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        ListNode* currentNode[10000];
        int length = lists.size();
        for(int i=0;i<length;i++) currentNode[i] = lists[i];
        ListNode* head = new ListNode;
        ListNode* minNode =new ListNode;
        head->val = 0;
        head->next = minNode;

        
        while(1)
        {
            int flag =0;
            int minVal = 99999;
            int minIndex = 0;
            for(int i=0;i<length;i++)
            {
                if(currentNode[i] != NULL)
                {
                    flag =1;
                    if(currentNode[i]->val < minVal)
                    {
                        minVal = currentNode[i]->val;
                        minIndex = i;
                    }      
                }
            }
            if(flag == 0)
            {
                minNode = NULL;
                return head->next->next;
            }
            else
            {
                ListNode* newNode= new ListNode;
                newNode->next = NULL;
                newNode->val = minVal;
                currentNode[minIndex] = currentNode[minIndex]->next;
                //minNode->val = minVal;
                minNode->next = newNode;
                minNode = newNode;
            }
        }
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/merge-k-sorted-lists/