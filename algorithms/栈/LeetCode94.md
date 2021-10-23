---
title: 二叉树中序遍历---LeetCode94(递归和栈)
date: 2020-09-14 10:17:19
tags: [dfs,递归,栈,stack]
---
## 题目描述：  
给一个二叉树，返回中序遍历。  

## 示例：   
```cpp
输入: [1,null,2,3]
   1
    \
     2
    /
   3
输出: [1,3,2]
```
<!-- more -->

## 解题思路:  
分两种方法解，一个是递归，一个是用栈。  
### 递归
没什么好说的  
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
    vector<int> ans;
    void dfs(TreeNode* root){
        if(root == nullptr) return;
        if(root->left != nullptr) dfs(root->left);
        ans.push_back(root->val);
        if(root->right != nullptr) dfs(root->right);
    }
    vector<int> inorderTraversal(TreeNode* root) {
        dfs(root);
        return ans;
    }
};
```
### 栈
栈这个方法还是要稍微注意一下，思路就是先一路一直压左边压到不能压，然后弹出一个后push进入答案，然后尝试对右子树疯狂压左边(同上)。  
通俗易懂代码：
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
    vector<int> inorderTraversal(TreeNode* root) {
        stack<TreeNode*> s;
        vector<int> ans;
        if(root == nullptr) return ans;
        while(root){
            s.push(root);
            root = root->left;
        }
        while(!s.empty()){
            TreeNode* temp = s.top();
            s.pop();
            ans.push_back(temp->val);
            root = temp->right;
            while(root){
                s.push(root);
                root = root->left;
            }
        }
        return ans;
        
    }
};
```
其实两个循环是可以合并为一个的，是简洁版代码，不过没这个好懂，懒得贴了，要看自己去Leetcode题解看。  

## 题目链接：  
https://leetcode-cn.com/problems/binary-tree-inorder-traversal/