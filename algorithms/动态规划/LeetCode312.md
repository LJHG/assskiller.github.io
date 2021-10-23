---
title: 戳气球---LeetCode312(dp)
date: 2020-07-19 11:30:59
tags: [dp,动态规划]
---
## 题目描述：  
有 n 个气球，编号为0 到 n-1，每个气球上都标有一个数字，这些数字存在数组 nums 中。
现在要求你戳破所有的气球。如果你戳破气球 i ，就可以获得 nums[left] * nums[i] * nums[right] 个硬币。 这里的 left 和 right 代表和 i 相邻的两个气球的序号。注意当你戳破了气球 i 后，气球 left 和气球 right 就变成了相邻的气球。
求所能获得硬币的最大数量。
说明:
你可以假设 nums[-1] = nums[n] = 1，但注意它们不是真实存在的所以并不能被戳破。
0 ≤ n ≤ 500, 0 ≤ nums[i] ≤ 100

## 示例：   
```cpp
输入: [3,1,5,8]
输出: 167 
解释: nums = [3,1,5,8] --> [3,5,8] -->   [3,8]   -->  [8]  --> []
     coins =  3*1*5      +  3*5*8    +  1*3*8      + 1*8*1   = 167
```

<!-- more -->

## 解题思路:  
好久没写题了，一上来就是一道hard的dp orz  
磨了一个多小时还是写出来了(抄出来了)  
这道题最开始我看到想的办法是dfs+备忘录，但是写着写着发现n有500个，记录状态貌似有一点麻烦，随后就废弃了，转而使用dp。
首先把首尾都添一个1，这没什么好说的。    
dp这道题有一个很巧妙的点，就是在定义dp时，设置的是开区间，也就是说，**dp[i][j]表示的是i到j之间(i和j没有戳)所有的气球被戳破后，能够获得的最大分数**。其实这里还要注意一下，就是里面的气球被戳破和，虽然是开区间，但是结果和ij是有关系的。  
由此可以举出几个例子，例如dp[0][2]的结果其实是nums[0] * nums[1] * nums[2] + dp[0][1] + dp[1][2]， 这里也要注意一下就是dp[0][1]这种当j-i的值小于等于1时，是没有意义的，所以结果为0。
总结一下，这道题的递推公式就是 **dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + nums[i] * nums[j] * nums[k])** ,k是最后一个被戳破的气球的下标。  
这道题真的蛮巧妙的，最好试试推一下dp[0][3]这种是怎么最后算出来的，就可以很好地理解了。

```cpp
class Solution {
public:
    int maxCoins(vector<int>& nums) {
        //首尾加上1
        nums.insert(nums.begin(),1);
        nums.push_back(1);
        int len = nums.size();

        int dp[502][502]; //dp[i][j]代表index i 到 index j之间的所有气球都被戳破
        memset(dp,0,sizeof(dp));
        //然后从长度为2开始遍历
        for(int l=2;l<=len-1;l++)
        {
            for(int i=0;i+l<len;i++)
            {
                int j = i+l;
                for(int k=i+1;k<=j-1;k++)
                {
                    dp[i][j] = max(
                        dp[i][j],
                        dp[i][k] + dp[k][j] + nums[i]*nums[j]*nums[k]
                    );
                }
            }
        }
        return dp[0][len-1]; 
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/burst-balloons/  
[一个讲的很好的题解](https://leetcode-cn.com/problems/burst-balloons/solution/dong-tai-gui-hua-tao-lu-jie-jue-chuo-qi-qiu-wen-ti/)