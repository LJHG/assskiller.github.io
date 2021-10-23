---
title: 二叉树层序遍历----LeetCode102
date: 2020-05-13 21:04:39
tags: [树, bfs]
---
### 题目描述：  
给你一个二叉树，请你返回其按 层序遍历 得到的节点值。（即逐层地，从左到右访问所有节点）。

### 示例：   
```cpp
示例：
二叉树：[3,9,20,null,null,15,7],
    3
   / \
  9  20
    /  \
   15   7
返回其层次遍历结果：
[
  [3],
  [9,20],
  [15,7]
]
```
<!-- more -->
### 解题思路:  
昨天的题太水了，没更新，今天的稍微有一点写的价值吧(shuiyixia)。  
这里讲两个思路，一个是正常人做法(略微繁琐)，另一个要稍微多想一步。

### 方法一
正常bfs，创建一个结构体，来记录level，然后bfs遍历过程中，把level对应的结果存下来，最后再整理输出，略微繁琐，因为要遍历两次。
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

struct myNode{
    TreeNode* node;
    int level;
};

class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<int> record[1000];
        vector<vector<int>> ans;
        for(int i=0;i<1000;i++) record[i].clear();
        queue<myNode> q;
        myNode start;
        start.node = root;
        start.level = 0;
        q.push(start);

        while(!q.empty())
        {
            myNode temp  = q.front();
            if(temp.node != NULL)
            {
                myNode newAdd;
                record[temp.level].push_back(temp.node->val);
                //push left node
                newAdd.node = temp.node->left;
                newAdd.level = temp.level+1;
                q.push(newAdd);
                //push right node
                newAdd.node = temp.node->right;
                newAdd.level = temp.level+1;
                q.push(newAdd);
            }
            q.pop();
        }
        for(int i=0;i<1000;i++)
        {
            if(record[i].size() == 0)
                break;
            vector<int> temp;
            for(int j=0;j<record[i].size();j++) temp.push_back(record[i][j]);
            ans.push_back(temp);
        }
        return ans;
    }
};
```

### 方法二
第二个方法不像第一个方法，其实稍微多想一下会发现，其实可以通过每次**多处理几个元素来实现每次可以把一个Level给处理完**。做法就是，进入时，先**统计queue的长度**(显然在这种做法下，可以保证在queue中的都在同一个level)。然后每次就处理queue长度这么多个元素，然后就可以直接得出结果，而不需要向上面一样，先统计，再输出结果。
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
    vector<vector<int>> levelOrder(TreeNode* root) {
        queue<TreeNode*> q;
        if(root != NULL)
            q.push(root);
        vector<vector<int>> ans;
        while(!q.empty())
        {
            int length = q.size();
            vector<int> tempv;
            for(int j=0;j<length;j++)
            {
                TreeNode* temp = q.front();
                tempv.push_back(temp->val);
                q.pop();
                if(temp->left != NULL) q.push(temp->left);
                if(temp->right != NULL) q.push(temp->right);
            }
            ans.push_back(tempv);
        }
        return ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/binary-tree-level-order-traversal/