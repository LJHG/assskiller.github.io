---
title: 最低票价---LeetCode983(简单dp)
date: 2020-05-06 15:13:13
tags: [dp]
---
### 题目描述：  
在一个火车旅行很受欢迎的国度，你提前一年计划了一些火车旅行。在接下来的一年里，你要旅行的日子将以一个名为 days 的数组给出。每一项是一个从 1 到 365 的整数。

火车票有三种不同的销售方式：

一张为期一天的通行证售价为 costs[0] 美元；
一张为期七天的通行证售价为 costs[1] 美元；
一张为期三十天的通行证售价为 costs[2] 美元。
通行证允许数天无限制的旅行。 例如，如果我们在第 2 天获得一张为期 7 天的通行证，那么我们可以连着旅行 7 天：第 2 天、第 3 天、第 4 天、第 5 天、第 6 天、第 7 天和第 8 天。

返回你想要完成在给定的列表 days 中列出的每一天的旅行所需要的最低消费。

### 示例：   
```cpp
示例 1：
输入：days = [1,4,6,7,8,20], costs = [2,7,15]
输出：11
解释： 
例如，这里有一种购买通行证的方法，可以让你完成你的旅行计划：
在第 1 天，你花了 costs[0] = $2 买了一张为期 1 天的通行证，它将在第 1 天生效。
在第 3 天，你花了 costs[1] = $7 买了一张为期 7 天的通行证，它将在第 3, 4, ..., 9 天生效。
在第 20 天，你花了 costs[0] = $2 买了一张为期 1 天的通行证，它将在第 20 天生效。
你总共花了 $11，并完成了你计划的每一天旅行。

示例 2：
输入：days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]
输出：17
解释：
例如，这里有一种购买通行证的方法，可以让你完成你的旅行计划： 
在第 1 天，你花了 costs[2] = $15 买了一张为期 30 天的通行证，它将在第 1, 2, ..., 30 天生效。
在第 31 天，你花了 costs[0] = $2 买了一张为期 1 天的通行证，它将在第 31 天生效。 
你总共花了 $17，并完成了你计划的每一天旅行。
 
提示：
1 <= days.length <= 365
1 <= days[i] <= 365
days 按顺序严格递增
costs.length == 3
1 <= costs[i] <= 1000
```

<!--more-->
### 解题思路:  
对每一个days里存在的天数进行dp，并在那一天进行买票（这里我默认只在days里有的天数买票，没有去考虑在其它天买票的情况，不知道有没有问题），并求出这一天买票cost最小的情况。当对某一天买了某一种票过后，在范围内的都不用买票，往后遍历，直到遇到第一个dp[k]不是0的，加上就是当前票的花费情况。(说的不清楚，看代码更清楚)

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        int dp[1000]; //dp[i]表示从第i天开始买票到最后的最小花费
        int daysLength = days.size();
        int costsLength = costs.size();

        memset(dp,0,sizeof(dp));
        //把最后一个先初始化了，没想到会有7天比1天便宜的情况，三个要求最小
        dp[days[daysLength-1]] = min(min(costs[0],costs[1]),costs[2]);
        //倒着dp
        for(int i=daysLength-2;i>=0;i--)
        {
            //遍历三种取值，取花费最小的
            int minCost = 999999;
            for(int j=0;j<3;j++)
            {
                int cost = costs[j];
                //如果days[i]+通行证天数 内的，就不用算钱，超过的就要加
                if(j==0)
                {
                    int flag= 0;
                    for(int k=days[i]+1;k<=days[daysLength-1];k++)
                    {
                        if(dp[k] != 0)
                        {
                            cost += dp[k];
                            break;
                        }
                    }
                        
                }
                else if(j == 1)
                {
                    int flag= 0;
                    for(int k=days[i]+7;k<=days[daysLength-1];k++)
                    {
                        if(dp[k] != 0)
                        {
                            cost += dp[k];
                            break;
                        }
                    }
                }
                else
                {
                    int flag= 0;
                    for(int k=days[i]+30;k<=days[daysLength-1];k++)
                    {
                        if(dp[k] != 0)
                        {
                            cost += dp[k];
                            break;
                        }
                    }
                }
                if(cost < minCost)
                    minCost = cost;
            }
            dp[days[i]] = minCost;
        }
        // for(int i=0;i<daysLength;i++)
        // {
        //     cout<<dp[days[i]]<<" ";
        // }
        return dp[days[0]];
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/minimum-cost-for-tickets/