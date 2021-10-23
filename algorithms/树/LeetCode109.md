---
title: 有序链表转换二叉搜索树---LeetCode109
date: 2020-08-18 14:23:47
tags: [二叉搜索树, BST, 链表, 快慢指针]
---
## 题目描述：  
给定一个单链表，其中的元素按升序排序，将其转换为高度平衡的二叉搜索树。
本题中，一个高度平衡二叉树是指一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过 1。

## 示例：   
```cpp
这里放测试样例给定的有序链表： [-10, -3, 0, 5, 9],
一个可能的答案是：[0, -3, 9, -10, null, 5], 它可以表示下面这个高度平衡二叉搜索树：
      0
     / \
   -3   9
   /   /
 -10  5

```
<!-- more -->
## 解题思路:  
思路有两个，一个是一直找中心点，一个是用中序遍历。
### 找中心点
想要得到一个平衡的二叉搜索树，最重要的就是如何选择二叉搜索树的根，很自然的想法就是一直选取中心点。
选择中心点的方法有两种：
1. 将链表转为数组，然后直接选。
2. 使用快慢指针法，将两个指针都设置在头节点，然后同时开始走，慢指针每次走一格，快指针每次走两格，当快指针走到尾部，满指针刚好走到中间。(这个方法看起来很巧妙，但是在数据规模小的时候，还是转数组比较香)。
```cpp
class Solution {
public:
    int num[100000];

    TreeNode* makeTree(int left,int right){
        if(left>right) return nullptr;
        if(left == right){
            return new TreeNode(num[left]);
        }
        int mid = (left+right)/2;
        TreeNode* midNode = new TreeNode(num[mid]);
        midNode->left = makeTree(left,mid-1);
        midNode->right = makeTree(mid+1,right);
        return midNode;
    }

    TreeNode* sortedListToBST(ListNode* head) {
        //先把链表转为数组
        TreeNode* ans = new TreeNode();
        int length = 0;
        
        memset(num,0,sizeof(num));
        while(head!=nullptr){
            num[length] = head->val;
            head = head->next;
            length++;
        }
        return makeTree(0,length-1);
    }
};
```

### 中序遍历
这个方法真的妙，要使用这个方法你首先要意识到对一个BST进行中序遍历得到的就是一个有序的序列，于是我们就可以反过来根据有序的序列来构建出这个BST。 
构建BST的过程也很妙，用到了一个全局的遍历链表的指针，然后每次在设置一个子树的root的值时，使用这个指针的val然后指针后移。这样就实现了遍历链表和建树的同步。  
```cpp
class Solution {
public:
    ListNode* curNode;
    TreeNode* buildBST(int left,int right){
        if(left > right) return nullptr;
        int mid = (left+right)/2;
        //先建立左子树
        TreeNode* leftSubTree = buildBST(left,mid-1);
        TreeNode* root = new TreeNode(curNode->val);
        curNode = curNode->next;
        TreeNode* rightSubTree = buildBST(mid+1,right);
        root->left = leftSubTree;
        root->right = rightSubTree;
        return root;
    }

    TreeNode* sortedListToBST(ListNode* head) {
        //搞一个全局的指针来遍历链表
        //然后中序遍历填值，这样遍历链表和建树就是同步的 
        ListNode* cur = head;
        int len = 0;
        while(cur!=nullptr){
            len++;
            cur = cur->next;
        }
        curNode = head;
        return buildBST(0,len-1);
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/convert-sorted-list-to-binary-search-tree/