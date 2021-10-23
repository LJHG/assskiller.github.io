---
title: 从前序与中序遍历序列构造二叉树---LeetCode105
date: 2020-05-22 14:53:04
tags: [递归, 树]
---
### 题目描述：  
根据一棵树的前序遍历与中序遍历构造二叉树。
注意:
你可以假设树中没有重复的元素。

### 示例：   
```cpp
例如，给出
前序遍历 preorder = [3,9,20,15,7]
中序遍历 inorder = [9,3,15,20,7]

返回如下的二叉树：
    3
   / \
  9  20
    /  \
   15   7

```
<!-- more -->


### 解题思路:  
这道题主要就是用递归的方法来做，先在中序遍历中找到根，然后就可以知道左子树和右子树的数量，然后就可以在前序遍历中找到左子树和右子树，根据新的左子树前序遍历和中序遍历 以及 右子树前序遍历和中序遍历，继续往下构建树，思想很简单，其实写起来还是有点复杂的。  
这道题还有一个迭代的做法，我有点没看懂，就不写了。  

### 优化前的递归
优化前我是在每次递归时都去构建了新的vector来作为参数传下去，所以有点慢。
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
    
    void helper(vector<int>& preorder, vector<int>& inorder,TreeNode* root)
    {
        //前序遍历的第一个元素是根，通过在中序遍历中找到根可以判断出左子树和右子树的个数
        //根据左子树和右子树的个数可以在前序遍历中找到左儿子和右儿子
        int preLength = preorder.size();
        int inLength = inorder.size();
        //如果当前只有一个元素 或者说没有root，直接返回
        if(preLength == 1 || root==NULL) return;
        int cnt = 0;
        for(int i=0;i<inLength;i++)
        {
            if(inorder[i] != preorder[0])
            {
                 cnt++;
            }
            else
            {
                break;
            }
        }

        if(cnt == 0)
            root->left = NULL;
        else
            root->left = new TreeNode(preorder[1]);
        
        if( cnt+1 == inLength)
            root->right = NULL;
        else
            root->right = new TreeNode(preorder[1+cnt]);

        //构建新的left 和 right的vector
        vector<int> leftPre;
        vector<int> leftIn;
        vector<int> rightPre;
        vector<int> rightIn;


        int temp = 0;
        for(int i=1;i<preLength;i++)
        {
            if(temp < cnt)
            {
                leftPre.push_back(preorder[i]);
                temp++;
            }
            else{
                rightPre.push_back(preorder[i]);
            }
        }

        temp = 0;
        for(int i=0;i<inLength;i++)
        {
            if(temp < cnt)
            {
                leftIn.push_back(inorder[i]);
                temp++;
            }
            else if (temp == cnt)
            {
                temp++;
                continue;
            }
            else{
                rightIn.push_back(inorder[i]);
            }
        }

        //打印当前的vector
        // cout<<"这里是左子树的前序: [";
        // for(int i=0;i<leftPre.size();i++) cout<<leftPre[i]<<" ";
        // cout<<"] "<<endl;
        // cout<<"这里是左子树的中序: [";
        // for(int i=0;i<leftIn.size();i++) cout<<leftIn[i]<<" ";
        // cout<<"] "<<endl;
        // cout<<"这里是右子树的前序: [";
        // for(int i=0;i<rightPre.size();i++) cout<<rightPre[i]<<" ";
        // cout<<"] "<<endl;
        // cout<<"这里是右子树的中序: [";
        // for(int i=0;i<rightIn.size();i++) cout<<rightIn[i]<<" ";
        // cout<<"] "<<endl;

        // cout<<"*********************"<<endl;



        helper(leftPre,leftIn,root->left);
        helper(rightPre,rightIn,root->right);
        return;
    }

    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) { 
        if(preorder.size() == 0 ) return NULL;
        TreeNode* root = new TreeNode(preorder[0]);
        helper(preorder,inorder,root);
        return root;
    }
};
```

</br>

### 优化后的递归
但是其实不用每次都去构建vector，只需要把对应的左边和右边的index记录一下就可以了。
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
    vector<int> preOrder;
    vector<int> inOrder;

    void helper(TreeNode* root,int preLeftIndex,int preRightIndex,int inLeftIndex,int inRightIndex)
    {
        //在中序遍历中寻找root
        if(preRightIndex-preLeftIndex == 0 || root == NULL ) return;
        int cnt = 0;
        for(int i=inLeftIndex ;i<=inRightIndex;i++)
        {
            if(inOrder[i] != root->val)
            {
                cnt++;
            }
            else
            {
                break;
            }
        }
        //确定左子树和右子树的根
        if(cnt == 0)
            root->left = NULL;
        else
            root->left = new TreeNode(preOrder[preLeftIndex+1]);
        
        if(cnt +1 == inRightIndex-inLeftIndex +1) //如果cnt+1就是length
            root->right = NULL;
        else
            root->right = new TreeNode(preOrder[preLeftIndex+1+cnt]);

        //建立左子树和右子树
        helper(root->left,preLeftIndex+1,preLeftIndex+cnt,inLeftIndex,inLeftIndex+cnt-1);
        helper(root->right,preLeftIndex+cnt+1,preRightIndex,inLeftIndex+cnt+1,inRightIndex);
    }

    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        //存一下，递归懒得传参
        if(preorder.size() == 0 ) return NULL;
        preOrder = preorder;
        inOrder = inorder;
        TreeNode* root = new TreeNode(preOrder[0]);
        int length = preorder.size();
        helper(root,0,length-1,0,length-1);
        return root;
    }
};
```


### 题目链接：  
https://leetcode-cn.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/