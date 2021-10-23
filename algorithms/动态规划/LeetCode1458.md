---
title: 两个子序列的最大点积---LeetCode1458(双序列dp)
date: 2020-05-26 00:16:05
tags: [双序列dp]
---
## 题目描述：  
给你两个数组 nums1 和 nums2 。
请你返回 nums1 和 nums2 中两个长度相同的 非空 子序列的最大点积。
数组的非空子序列是通过删除原数组中某些元素（可能一个也不删除）后剩余数字组成的序列，但不能改变数字间相对顺序。比方说，[2,3,5] 是 [1,2,3,4,5] 的一个子序列而 [1,5,3] 不是。

<!-- more -->
## 示例：   
```cpp
示例 1：
输入：nums1 = [2,1,-2,5], nums2 = [3,0,-6]
输出：18
解释：从 nums1 中得到子序列 [2,-2] ，从 nums2 中得到子序列 [3,-6] 。
它们的点积为 (2*3 + (-2)*(-6)) = 18 。

示例 2：
输入：nums1 = [3,-2], nums2 = [2,-6,7]
输出：21
解释：从 nums1 中得到子序列 [3] ，从 nums2 中得到子序列 [7] 。
它们的点积为 (3*7) = 21 。

示例 3：
输入：nums1 = [-1,-1], nums2 = [1,1]
输出：-1
解释：从 nums1 中得到子序列 [-1] ，从 nums2 中得到子序列 [1] 。
它们的点积为 -1 。

提示：
1 <= nums1.length, nums2.length <= 500
-1000 <= nums1[i], nums2[i] <= 100

```

## 解题思路:  
记录一下双序列dp，当时直接写没写出来，看了解答后发现也不是很难。  
这个题和最大公共子序列，和那个编辑距离（还没做过）貌似很像，像这种双序列的dp一般是有套路的，都是像下面那种，**dp[i][j] = max(dp[i-1][j-1]+xxx, dp[i][j-1], dp[i-1][j])** 这种的吧。   
算是在leetcode上第一次碰到这种类型吧，记录一下。

```cpp
const int MAXN = 550;
class Solution {
public:
    int maxDotProduct(vector<int>& nums1, vector<int>& nums2) {
        //双序列dp
        int dp[MAXN][MAXN]; //dp[i][j]表示Nums1的从0到indexi个元素和nums2的从0到Indexj个元素的最小点积
        int length1 = nums1.size();
        int length2 = nums2.size();
        //初始化
        for(int i=0;i<length1;i++)
        {
            for(int j=0;j<length2;j++)
            {
                dp[i][j] = nums1[i]*nums2[j];
            }
        }

        for(int i=0;i<length1;i++)
        {
            for(int j=0;j<length2;j++)
            {
                if(i>0 && j>0)dp[i][j] = max(dp[i][j],dp[i-1][j-1] + nums1[i]*nums2[j]);
                if(i>0) dp[i][j] = max(dp[i][j],dp[i-1][j]);
                if(j>0) dp[i][j] = max(dp[i][j],dp[i][j-1]);
            }
        }
        return dp[length1-1][length2-1];   
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/max-dot-product-of-two-subsequences/