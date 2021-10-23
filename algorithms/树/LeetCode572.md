---
title: 另一个树的子树---LeetCode572
date: 2020-05-07 13:13:38
tags: [树, 双dfs]
---
### 题目描述：  
给定两个非空二叉树 s 和 t，检验 s 中是否包含和 t 具有相同结构和节点值的子树。s 的一个子树包括 s 的一个节点和这个节点的所有子孙。s 也可以看做它自身的一棵子树

### 示例：   
```cpp
示例 1:
给定的树 s:

     3
    / \
   4   5
  / \
 1   2
给定的树 t：

   4 
  / \
 1   2
返回 true，因为 t 与 s 的一个子树拥有相同的结构和节点值。

示例 2:
给定的树 s：

     3
    / \
   4   5
  / \
 1   2
    /
   0
给定的树 t：

   4
  / \
 1   2
返回 false。
```

<!--more-->

### 解题思路:  
这道题最开始我就是在isSubTree里这个函数里自己dfs自己的，后来发现不行，因为需要把t保存下来，所以不能在dfs的过程中改变t，这显然是不可能的，所以本来我打算创一个指针root来深拷贝t，后来搞了半天各种错，最后就转而来用了双dfs。  
在双dfs时，创建了两个函数，一个是isSame，用来判断从某个结点开始，是否和t树相同。一个是isSubTree,用来改变s树。可以看到，在isSubTree的dfs中，是不能改变t的值的。

```cpp
class Solution {
public:
    bool isSame(TreeNode* s, TreeNode* t)
    {
        if(s==NULL && t==NULL) return true;
        if(s==NULL || t==NULL) return false;
        if(s->val != t->val) return false;
        return isSame(s->left,t->left)&&isSame(s->right,t->right);
    }

    bool isSubtree(TreeNode* s, TreeNode* t) {
        if(isSame(s,t)) return true;
        if(s != NULL)
            return isSubtree(s->left,t) || isSubtree(s->right,t);  
        return false;     
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/subtree-of-another-tree/