---
title: 最大正方形---LeetCode221(能想到怎么dp就很简单的dp)
date: 2020-05-08 12:46:13
tags: [dp, 矩阵]
---
### 题目描述：  
在一个由 0 和 1 组成的二维矩阵内，找到只包含 1 的最大正方形，并返回其面积。

### 示例：   
```cpp
输入: 
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0

输出: 4
```


### 解题思路:  
这道题一开始一看就是dp做，但是想了半天没想出来该怎么dp。  
后来去看了题解，发现dp[i][j]是指的右下角为i,j的正方形的xxx，豁然开朗。只要规定好是右下角，就很好写递归公式了。  
最开始还没想好边长为偶的正方形和边长为奇的正方形该怎么统一，但是画一下图就会发现，其实就是统一的。
边长为2的正方形的情况：  
![1](/images/LeetCode221_1.png)  
边长为3的正方形的情况：  
![2](/images/LeetCode221_2.png)  
递推公式为 dp[i][j] = min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])+1  

```cpp
class Solution {
public:
    int MAXN = 1e3;
    int maximalSquare(vector<vector<char>>& matrix) {
        if(matrix.size()==0)
            return 0;
        int dp[MAXN][MAXN];
        //i是纵坐标，j是横坐标
        int iLength = matrix.size();
        int jLength = matrix[0].size();
        //初始化dp
        for(int i=0;i<iLength;i++)
        {
            for(int j=0;j<jLength;j++)
            {
                if(matrix[i][j]=='0')
                    dp[i][j] = 0;
                else
                    dp[i][j] = 1;
            }
        }
        int ans = 0;
        for(int i=0;i<iLength;i++)
        {
            for(int j=0;j<jLength;j++)
            {
                if(dp[i][j] == 1 && i-1>=0 && j-1>=0 && dp[i-1][j]>0 && dp[i][j-1]>0 &&dp[i-1][j-1] >0 )
                {
                    dp[i][j] = min(min(dp[i-1][j],dp[i][j-1]),dp[i-1][j-1]) + 1;
                }
                //cout<<"i: "<<i<<" j: "<<j<<": dp[i][j]:"<<dp[i][j]<<endl;
                ans = max(dp[i][j],ans);
            }
        }
        return ans*ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/maximal-square/