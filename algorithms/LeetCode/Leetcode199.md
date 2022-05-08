---
title: Leetcode199 二叉树右视图(DFS)
date: 2020-04-22 20:20:57
tags: [DFS]
---

开始在个人博客写一写leetcode题解，有tag功能归档还挺方便的，而且还可以水一水github contribution，美滋滋。(反正没人看，随便乱写一写)

### 题目描述：  
给定一棵二叉树，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

### 示例:
```
输入: [1,2,3,null,5,null,4]
输出: [1, 3, 4]
解释:

   1            <---
 /   \
2     3         <---
 \     \
  5     4       <---

```

### 解题思路:  
使用DFS优先遍历右子树，再遍历左子树，同时记录一个当前走到的最大深度，如果当前访问的位置没有到最大深度，那么就不把val加入到结果中，如果当前位置大于了最大深度，那么久加入ans

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
    int currentDepth;
    vector<int> ans;
    void addTreeRightToAns(TreeNode* node, int depth)
    {
        if(depth > currentDepth)
        {
            currentDepth = depth;
            ans.push_back(node->val);
        }
        if(node->right != NULL)
            addTreeRightToAns(node->right,depth+1);
        if(node->left != NULL)
            addTreeRightToAns(node->left,depth+1);
    }
    
    vector<int> rightSideView(TreeNode* root) {
        if(root == NULL)
            return ans;
        currentDepth = 0;
        addTreeRightToAns(root,1);
        return ans;
    }
};
```