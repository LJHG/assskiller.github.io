---
title: 验证二叉搜索树---LeetCode98
date: 2020-05-06 16:22:13
tags: [二叉树, tree, BST, DFS, 中序遍历]
---
### 题目描述：  
给定一个二叉树，判断其是否是一个有效的二叉搜索树。
假设一个二叉搜索树具有如下特征：
节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。

### 示例：   
```cpp
示例 1:
输入:
    2
   / \
  1   3
输出: true

示例 2:
输入:
    5
   / \
  1   4
     / \
    3   6
输出: false
解释: 输入为: [5,1,4,null,null,3,6]。
     根节点的值为 5 ，但是其右子节点值为 4 。

```
<!--more-->
### 解题思路:  
这里给两个解题思路，一个是递归(dfs),另一个是中序遍历

### DFS
要写好DFS,就要明确知道二叉搜索树的定义，二叉搜索树就是一棵树，他的左子树上的数字都比根节点小，右子树上的数组都比根节点大。  
所以在确定如何进行dfs时，可以这样想：当拿到一个节点时，只需要判断自己的上下界来看自己是否满足要求：
1. 如果是左子树，那么上界就是根节点的值，下界就是根节点的下界。
2. 如果是右子树，那么下界就是根节点的值，上界就是根节点的上界。
把这些捋明白了，就很好写了。

```cpp
class Solution {
public:
    bool judgeCurrentNode(TreeNode* root,long long  upper, long long  lower)
    {
        if(root==NULL) return true;
        if(root->val >= upper || root->val <= lower) return false;
        return judgeCurrentNode(root->left,root->val,lower)&&judgeCurrentNode(root->right,upper,root->val);
    }
    bool isValidBST(TreeNode* root) {
        return judgeCurrentNode(root,LONG_MAX,LONG_MIN);
    }
};
```

<br/>


### 中序遍历
对树进行中序遍历，如果不是递增，就return false

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
    long long min = LONG_MIN;
    bool isValidBST(TreeNode* root) {
        //中序遍历
        bool leftOk = false;
        bool rightOk = false;
        if(root == NULL) return true;
        //左
        if(root->left != NULL)
            leftOk=isValidBST(root->left);
        else
            leftOk = true;

        //中
        if(root->val > min)   
            min = root->val;
        else
            return false;

        //右
        if(root->right != NULL) 
            rightOk=isValidBST(root->right);
        else 
            rightOk = true;
        return leftOk&&rightOk;
    }
};

```


### 题目链接：  
https://leetcode-cn.com/problems/validate-binary-search-tree/