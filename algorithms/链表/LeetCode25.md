---
title: K个一组翻转链表---LeetCode25(指针地狱)
date: 2020-05-16 19:39:18
tags: [链表]
---
### 题目描述：  
给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。
k 是一个正整数，它的值小于或等于链表的长度。
如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。

### 示例：   
```cpp
示例：
给你这个链表：1->2->3->4->5
当 k = 2 时，应当返回: 2->1->4->3->5
当 k = 3 时，应当返回: 3->2->1->4->5

说明：
你的算法只能使用常数的额外空间。
你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。
```
<!-- more -->

### 解题思路:  
这道题的核心思想并不难，就是不断地选择链表进行交换就行了，同时需要让被交换链表前的next指向交换后链表的头，交换后链表的尾指向交换链表后的第一个元素。  但是需要各种各样的指针，最后很容易就昏了。
这道题我选择的链表交换的方法是从前往后遍历，记录每一个节点的前驱节点，然后再遍历一次反转next。这样做出来的结果就是把**start->1->2->end**变成了**start<-1<-2<-end**。这样明显是不好的，我不可能让外面去从end开始遍历。所以我思考了很久，该怎么把start和end交换一下，使用了若干方法，都无济于事(感觉自己指针白学了呃呃呃呃啊啊啊啊)。最后实在没办法，就把start 和 end return出去，在外面改。  
可能还有更好的链表交换方法，这里也不深究了。  
这就是这道题hard的原因吧，链表真的烦，下次试试不用c++写，链表+指针简直要命。  

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
    pair<ListNode*,ListNode*> reverseList(ListNode* start, ListNode* end)
    {
        vector<ListNode*> recoredPrev;
        ListNode* cur = start;
        while(cur != end)
        {
            recoredPrev.push_back(cur);
            cur = cur->next;
        }
        cur = start->next;
        for(auto prev:recoredPrev)
        {
            ListNode* temp = cur->next;
            cur->next = prev;
            cur = temp;
        }
        start->next = NULL;
        
        return make_pair(end,start); //还是不交换了，直接返回出去在外面改吧 
    }
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* prev = NULL;
        ListNode* start;
        ListNode* cur;
        ListNode* end;
        int cnt = 0;

        cur = head;
        start = head;
        prev = NULL;
        int flag = 0;
        while(cur != NULL)
        {
            cnt++;
            if(cnt == k)
            {
                end = cur;
                cur = cur->next;
                pair<ListNode*,ListNode*> ret = reverseList(start,end);
                start = ret.first;
                //***********处理一下head********
                if(flag==0)
                {
                    head = start;
                    flag = 1;
                }
                //***********
                end = ret.second;
                end->next = cur;
                if(prev != NULL)
                    prev->next = start;
                prev = end;
                start = cur;
                cnt=0;
            }
            else
            {
                cur = cur->next;
            }
            
        }    
        return head;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/reverse-nodes-in-k-group/