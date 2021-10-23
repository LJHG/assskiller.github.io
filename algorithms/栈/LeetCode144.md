---
title: 二叉树的前序遍历---LeetCode144
date: 2020-10-27 11:24:49
tags: [栈,Stack]
---
## 题目描述：  
给定一个二叉树，返回它的 前序 遍历。

## 示例：   
```cpp
示例:
输入: [1,null,2,3]  
   1
    \
     2
    /
   3 

输出: [1,2,3]
```
<!-- more -->

## 解题思路:  
好久没写博客了，或者说好久没写leetcode了= =，来水一发。  
水题，两种方法，一个递归，一个迭代。
### 递归
```cpp
class Solution {
public:
    vector<int> ans;
    void dfs(TreeNode* root){
        if(root == nullptr) return;
        ans.push_back(root->val);
        dfs(root->left);
        dfs(root->right);
    }
    vector<int> preorderTraversal(TreeNode* root) {
        ans.clear();
        dfs(root);
        return ans;
    }
};
```

### 迭代
迭代时使用的是栈，要注意，栈是先push右边，再push左边，因为需要在pop时先pop左边，再pop右边。
```cpp
class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> ans;
        //stack
        stack<TreeNode*> s;
        if(root!=nullptr) s.push(root);
        while(!s.empty()){
            TreeNode* topNode = s.top();
            s.pop();
            ans.push_back(topNode->val);
            if(topNode->right != nullptr) s.push(topNode->right);
            if(topNode->left != nullptr) s.push(topNode->left);
        }
        return ans;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/binary-tree-preorder-traversal/