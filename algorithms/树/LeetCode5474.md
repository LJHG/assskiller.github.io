---
title: 好叶子节点对的数量---LeetCode5474(记录路径)
date: 2020-07-26 15:06:42
tags: [记录路径]
---
## 题目描述：  
给你二叉树的根节点 root 和一个整数 distance 。
如果二叉树中两个叶节点之间的最短路径长度小于或者等于 distance ，那它们就可以构成一组 好叶子节点对 。
返回树中 好叶子节点对的数量 。

## 示例：   
```cpp
输入：root = [1,2,3,null,4], distance = 3
输出：1
解释：树的叶节点是 3 和 4 ，它们之间的最短路径的长度是 3 。这是唯一的好叶子节点对。
```

<!-- more -->

## 解题思路:  
这道题我的这个方法是好像比较非主流，然后去讨论区看了一下，也有人和我用相同的方法。  
我也不知道怎么给这个方法命名，不妨就叫记录路径法吧。  
大体思路是这样的：从根往叶子节点走，走左子树记录为0，走右子树记录为1，那么走到叶子节点后，每个节点都会对应有一个序列。比如上面那个例子，3号节点的序列就是1，4号节点的序列就是01，根据这个序列，就可以计算两个叶子之间的距离了。具体怎么计算的，看代码吧，反正就是左对齐然后一顿整。

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    
    vector<string> leaves;
    
    void dfs(TreeNode* curNode , string s){
        if(curNode -> left == nullptr && curNode->right == nullptr){
            leaves.push_back(s);        
        }
        if(curNode -> left != nullptr){
            dfs(curNode->left,s+'0');
        }
        if(curNode->right != nullptr){
            dfs(curNode->right,s+'1');
        }
    }
    int countPairs(TreeNode* root, int distance) {
        int ans = 0;
        string s = "";
        dfs(root,s);
        int len = leaves.size();
        int vis[1025][1025];
        memset(vis,0,sizeof(vis));
        //开始遍历所有叶子
        for(int i=0;i<len;i++){
            for(int j=0;j<len;j++){
                if(i == j || vis[i][j] || vis[j][i] )  continue;
                string s1 = leaves[i];
                string s2 = leaves[j];
                int len1 = leaves[i].length();
                int len2 = leaves[j].length();
                int curLen = 0;
                while(s1[curLen] == s2[curLen]){
                    curLen++;
                }
                int dis = (min(len1,len2) - curLen)*2 + max(len1,len2)-min(len1,len2);
                vis[i][j] = 1;
                if(dis <= distance) {
                    // cout<<s1<<endl;
                    // cout<<s2<<endl;
                    // cout<<endl;
                    ans++;
                }
                
            } 
        }
      return ans;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/number-of-good-leaf-nodes-pairs/