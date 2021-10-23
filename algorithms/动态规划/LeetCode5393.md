---
title: 可获得最大点数（乱用DP=炸内存）
date: 2020-04-26 13:41:36
tags: [周赛186, 前缀和, 后缀和, 不要乱用dp]
---
### 题目描述：  
几张卡牌 排成一行，每张卡牌都有一个对应的点数。点数由整数数组 cardPoints 给出。

每次行动，你可以从行的开头或者末尾拿一张卡牌，最终你必须正好拿 k 张卡牌。

你的点数就是你拿到手中的所有卡牌的点数之和。

给你一个整数数组 cardPoints 和整数 k，请你返回可以获得的最大点数。

### 示例：   
```cpp
示例 1：

输入：cardPoints = [1,2,3,4,5,6,1], k = 3
输出：12
解释：第一次行动，不管拿哪张牌，你的点数总是 1 。但是，先拿最右边的卡牌将会最大化你的可获得点数。最优策略是拿右边的三张牌，最终点数为 1 + 6 + 5 = 12 。
示例 2：

输入：cardPoints = [2,2,2], k = 2
输出：4
解释：无论你拿起哪两张卡牌，可获得的点数总是 4 。
示例 3：

输入：cardPoints = [9,7,7,9,7,7,9], k = 7
输出：55
解释：你必须拿起所有卡牌，可以获得的点数为所有卡牌的点数之和。
示例 4：

输入：cardPoints = [1,1000,1], k = 1
输出：1
解释：你无法拿到中间那张卡牌，所以可以获得的最大点数为 1 。 
示例 5：

输入：cardPoints = [1,79,80,1,1,1,200,1], k = 3
输出：202
 

提示：

1 <= cardPoints.length <= 10^5
1 <= cardPoints[i] <= 10^4
1 <= k <= cardPoints.length
```

### 解题思路:  
最近看到什么题都想用dp，然后都无一例外的。。。炸内存超时了，笑死。  

先来展示一下正确姿势，可以叫做前缀和后缀和，也可以不用刻意去求前缀和后缀和，总之就是前默认全部取左边，然后左边减一个，右边加一个，然后求出最大的sum就可以了




```cpp
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        //先全部拿左边的，然后左边放一个，右边加一个，求最大值
        int sum = 0;
        for(int i=0;i<k;i++) sum += cardPoints[i];

        int length = cardPoints.size();
        int leftLength =k;
        int max=sum;
        for(int i=0;i<k;i++)
        {
            sum -= cardPoints[leftLength-1];
            sum += cardPoints[length-i-1];
            leftLength--;
            if(sum > max)
               max = sum;
        }
        return max;
    }
};
```

<br/>
<br/>

再来展示一下错误示范，当我看到这道题时，第一反应就是，ok，给了个区间，ok,有一个动态变化的k，ok可以dp了，于是就直接搞了个三维dp。  
```cpp
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        int dp[100][100][1000]; // dp[i][j][k]表示 从indexi到indexj 剩余天数为k能拿的最大值
        memset(dp,0,sizeof(dp));
        
        int length = cardPoints.size();
        
        for(int d=1; d<=k; d++)
        {
            for(int i=0;i<length;i++)
            {
                for(int j=i;j<length;j++)
                {
                    if(d==1)
                    {
                        dp[i][j][1] = max(cardPoints[i],cardPoints[j]); 
                    }
                    else
                    {
                        if(j-1 >= 0)
                            dp[i][j][d]  = max(dp[i+1][j][d-1]+cardPoints[i], dp[i][j-1][d-1] +cardPoints[j]);
                        else
                            dp[i][j][d] = cardPoints[j];
                    }
                }
            }
        }
        return dp[0][length-1][k];
    }
};
```

以后别这么搞了，233

### 题目链接：  
https://leetcode-cn.com/problems/maximum-points-you-can-obtain-from-cards/