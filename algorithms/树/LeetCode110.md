---
title: 平衡二叉树---LeetCode110
date: 2020-08-17 11:46:25
tags: [二叉树]
---
## 题目描述：  
给定一个二叉树，判断它是否是高度平衡的二叉树。
本题中，一棵高度平衡二叉树定义为：
一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过1。

## 示例：   
```cpp
示例 1:
给定二叉树 [3,9,20,null,null,15,7]

    3
   / \
  9  20
    /  \
   15   7
返回 true 。

示例 2:
给定二叉树 [1,2,2,3,3,null,null,4,4]

       1
      / \
     2   2
    / \
   3   3
  / \
 4   4
返回 false 。
```
<!-- more -->

## 解题思路:  
这道题我写了老半天,太菜了呃呃呃.  
说一下思路吧,这道题有两个解法,一个是自顶向下,一个是自底向上。  
### 自顶向下法
这是一个比较自然的做法，首先要写一个求节点高度的函数(也是用递归实现的)，然后对于原树做遍历(先判断自己是不是平衡的，然后再判断左右子树是不平衡的)。但是这个方法有一个不好的地方，就是当你判断一个节点是不是平衡时，你会调用很多次height函数。

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
    int height(TreeNode* root,int depth){
        if(root == NULL) return depth-1;
        return max(height(root->left,depth+1),height(root->right,depth+1));
    }
    bool isBalanced(TreeNode* root) {
        //自顶向下的遍历
        if(root == NULL) return true;
        if(abs(height(root->left,0)-height(root->right,0))>1){
            return false;
        }else{
            return isBalanced(root->left)&&isBalanced(root->right);
        }
    }
};
```
### 自底向上法
这个方法叫做自底向上法。  
这个方法为什么叫做自底向上法我是这么理解的：当你要求一个节点的高度，你会去求下面的两个节点的高度，然后依次类推，会一直走到叶节点，叶节点的高度为0，然后一路往上推，求出当前节点的高度，而在往上回溯的过程中，如果某个子节点不平衡了，那么就可以一路推上去不平衡(通过return -1)。  
这个方法比起第一个要巧妙了许多，因为你会发现，他对于每一个节点只调用了一次height函数，但是第一种方法会调用多次height函数。  
我想了一下，为什么同样是通过求高度实现，两种方法的差异会如此之大。我认为是这样的：
1. 第一种方法的本质在于判断当前节点是否平衡，而判断平衡的方法是对于左右节点求高度，然后比较，如此一来，就会求很多次高度，我们可以认为这里有两次递归，一次是在遍历树，一次是在每一次对于一个节点的求高度。
2. 而第二种方法就仅仅是求高度而已，可以看到，我们实际上就只是求了root高度，而要在求的过程中保存不平衡节点的信息，就通过return -1的方式来实现，真的十分巧妙。
虽然这是一道简单题，但是真的还是很有意思的。
```cpp
class Solution {
public:
    int height(TreeNode* root){
        if(root == NULL) return 0;
        int leftHeight = height(root->left);
        int rightHeight = height(root->right);
        if(leftHeight == -1 || rightHeight == -1 || abs(leftHeight-rightHeight) > 1){
            return -1;
        }
        return max(leftHeight,rightHeight)+1;
    }
    bool isBalanced(TreeNode* root) {
        if(height(root)>=0) return true;
        return false;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/balanced-binary-tree/