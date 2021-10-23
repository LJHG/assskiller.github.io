---
title: 不同的二叉搜索树 II---LeetCode95
date: 2020-07-21 09:50:23
tags: [二叉树,二叉搜索树]
---
## 题目描述：  
给定一个整数 n，生成所有由 1 ... n 为节点所组成的 二叉搜索树 。

## 示例：   
```cpp
输入：3
输出：
[
  [1,null,3,2],
  [3,2,null,1],
  [3,1,null,null,2],
  [2,1,3],
  [1,null,2,null,3]
]
解释：
以上的输出对应以下 5 种不同结构的二叉搜索树：

   1         3     3      2      1
    \       /     /      / \      \
     3     2     1      1   3      2
    /     /       \                 \
   2     1         2                 3
```
<!-- more -->

## 解题思路:  
看着树本来还是有点烦的，但是看了一下题解好像也不是那么难(还是看题解了233)。
这道题明显是递归，反正就是在一次递归里不断选择根，然后由根可以分出左子树和右子树，然后左子树和右子树又以这种方法来生成新的"树组"。  
需要注意的是在递归判断返回时，也就是说当left>right时，需要往vector中push一个nullptr，不然后面在某个子树中就遍历不到nullptr这个元素(null也是一种情况，所以需要被遍历！)。

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
    //根据左右边界来生成trees 
    vector<TreeNode*> getTrees(int left,int right)
    {
        vector<TreeNode*> ans;
        if(left > right){
            ans.push_back(nullptr);
            return ans;
        }
        //遍历选择根，并确定左子树的边界和右子树的边界
        for(int root=left;root<=right;root++){
            vector<TreeNode*> leftSubTrees = getTrees(left,root-1);
            vector<TreeNode*> rightSubTrees = getTrees(root+1,right);
            //根据当前左子树数组，右子树数组，根 形成一组答案
            for(auto leftSubTree : leftSubTrees){
                for(auto rightSubTree: rightSubTrees){
                    TreeNode* node = new TreeNode;
                    node->val = root;
                    node->left = leftSubTree;
                    node->right = rightSubTree;
                    ans.push_back(node);
                }
            }
        }
        return ans;
    } 
    
    vector<TreeNode*> generateTrees(int n) {
        vector<TreeNode*> ans;
        if(n==0) return ans; //对等于0的情况做特殊处理
        return getTrees(1,n);
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/unique-binary-search-trees-ii/