---
title: 跳跃游戏---LeetCode45
date: 2020-05-04 14:34:35
tags: [dp, 动态规划, 贪心]
---
### 题目描述：  
给定一个非负整数数组，你最初位于数组的第一个位置。
数组中的每个元素代表你在该位置可以跳跃的最大长度。
你的目标是使用最少的跳跃次数到达数组的最后一个位置。

### 示例：   
```cpp
输入: [2,3,1,1,4]
输出: 2
解释: 跳到最后一个位置的最小跳跃数是 2。
     从下标为 0 跳到下标为 1 的位置，跳 1 步，然后跳 3 步到达数组的最后一个位置。
说明:

假设你总是可以到达数组的最后一个位置。
```

### 解题思路:  
这道题给两个解题思路，一个是贪心，一个是dp。

<!--more-->

### 贪心
贪心的策略是每次的选择要使得未来能够跳的最远，其实也很好理解，因为未来能够跳的最远，那么也可以跳的很近，也就是说，未来能够跳的最远的选择其实是包括了跳的近的选择的。证明差不多就是这个思路。  


```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        int ans =0;
        int length = nums.size();
        int i=0;
        while(i<length-1)
        {
            //选择一个未来能够跳的最远的点
            ans++;
            int max =0;
            int maxj = 0;
            for(int j=1;j<=nums[i];j++)
            {
                //如果这次就能直接跳到终点，那么就直接返回
                if(i+j >= length-1)
                    return ans;
                //i+j+nums[i+j]是未来能够跳到最远的Index
                if(i+j+nums[i+j] > max)
                {
                    max = i+j+nums[i+j];
                    maxj  = j;
                }
            }
            i += maxj;
        }
        return ans;
    }
};
```


<br/>

### 动态规划
dp的思路很简单，就是从后往前推，dp[i]表示从Index i 到最后的最小跳数。不过这道题直接这么搞会超时，所以加了一个same数组。same[i]表示Index为i位置往后包括自己跳到重点答案相同的个数，这样就没有必要为了相同的答案遍历很多次，但是有点难想到，因为最开始我并没有分析到超时是因为有很多相同的答案，还是看了评论区才知道的。  
ps： memset不能用于赋值为1，所以这里用的循环赋值。

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        int dp[100000]; //dp[i]表示从index为i的位置跳到最后需要的最小跳跃次数
        int same[100000];//same[i]表示Index为i位置往后包括自己跳到重点答案相同的个数
        int length = nums.size();
        for(int i=0;i<length;i++) 
        {
            dp[i]=0;
            same[i]=1;
        }
        for(int i=length-2;i>=0;i--)
        {
            int temp = 99999;
            //加一个剪枝，如果当前能够直接跳到终点，那么就直接赋值并continue
            if(i+nums[i] >= length-1)
            {
                dp[i] = 1;
                continue;
            }
            for(int j=1;j<=nums[i];j+=same[i+j])
            {
                //cout<<"当前Index为："<<i<<" 跳的长度为"<<j<<endl;
                temp = min(temp,dp[i+j]+1);
            }
            dp[i] = temp;
            if(dp[i] == dp[i+1])
                same[i] = same[i+1]+1;
        }
        return dp[0];
    }
};

```

### 题目链接：  
https://leetcode-cn.com/problems/jump-game-ii/