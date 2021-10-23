---
title: 把二叉搜索树转换为累加树---LeetCode538
date: 2020-09-21 09:44:56
tags: [BST,dfs,tree]
---
## 题目描述：  
给定一个二叉搜索树（Binary Search Tree），把它转换成为累加树（Greater Tree)，使得每个节点的值是原来的节点值加上所有大于它的节点值之和。

## 示例：   
```cpp
输入: 原始二叉搜索树:
              5
            /   \
           2     13

输出: 转换为累加树:
             18
            /   \
          20     13
```
<!-- more -->

## 解题思路:  
这道题很简单，但是还是很有味道的。  
因为那个全局的sum设置得太妙了，所以还是记录一下。  
```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    int sum = 0;
    TreeNode* convertBST(TreeNode* root) {
        if(root == nullptr) return root;
        convertBST(root->right);
        sum += root->val;
        root->val = sum;
        convertBST(root->left);
        return root;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/convert-bst-to-greater-tree/