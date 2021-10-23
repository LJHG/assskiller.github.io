---
title: 收集树上所有苹果---LeetCode5406(碰见树就GG)
date: 2020-05-10 14:54:20
tags: [树, dfs, 邻接表]
---
### 题目描述：  
给你一棵有 n 个节点的无向树，节点编号为 0 到 n-1 ，它们中有一些节点有苹果。通过树上的一条边，需要花费 1 秒钟。你从 节点 0 出发，请你返回最少需要多少秒，可以收集到所有苹果，并回到节点 0 。
无向树的边由 edges 给出，其中 edges[i] = [fromi, toi] ，表示有一条边连接 from 和 toi 。除此以外，还有一个布尔数组 hasApple ，其中 hasApple[i] = true 代表节点 i 有一个苹果，否则，节点 i 没有苹果。
![](/images/min_time_collect_apple_1.png)
<!-- more -->
### 示例：   
```cpp
输入：n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,true,false,true,true,false]
输出：8 
解释：上图展示了给定的树，其中红色节点表示有苹果。一个能收集到所有苹果的最优方案由绿色箭头表示。
```

### 解题思路:  
看见树我就会GG，果然，这次又栽了。最开始我写的DFS，极其复杂，简直就是在乱写，就懒得叙述了。 
首先这道题要明白最短开销是怎么来的，最短开销就是不走回头路，也就是说，每条边就走两次，最后转换过来，就是一个遍历。
这道题的正确思路，仍然是dfs，不过dfs的思想是，看子树是否有苹果，如果子树有苹果，那么就会去走那条边，如果没有，就不去走。最后的结果乘2就行了。 
在代码中，我dfs里的ans其实就是一个记录是否有苹果的，不管是1，是2，其实最后起到的作用，就是做一个判断，真正的答案是全局变量totalAns。  
另外，这道题需要把邻接矩阵（算是吧）转换成邻接表，不然会超时，当数据很大时，邻接表确实会快很多，不然每次都要对矩阵做遍历，很耗时。
另外，在转邻接表时，我是当成有向图转的，因为反正都是不走回头路，而且输入时，每一个都是属于[上，下]的这种，我就直接做成了有向图。

```cpp
const int MAXN = 1e5+50;
class Solution {
public:
//看子树有没有苹果，如果有苹果，路径长度+1，没有就停止了
vector<int> e[MAXN]; //把edges存一下
vector<bool> isApple; //其实就是一个把hasApple存一下的变量
int length;
int totalAns;
    int dfs(int cur)
    {
        int ans=0;
        for(auto ee:e[cur])
        {
            if( (dfs(ee) || isApple[ee] ))
            {
                ans += 1;
                totalAns += 1;
            }
        }
        for(int i =0;i<length;i++)
        {
            if(e[i][0] == cur && (dfs(e[i][1]) || isApple[e[i][1]] ))
            {
                ans += 1;
                totalAns += 1;
            }
        }
        //cout<<"Cur: "<<cur<<" ans: "<<ans<<endl;
        return ans;
    }


    int minTime(int n, vector<vector<int>>& edges, vector<bool>& hasApple) {
        isApple =hasApple;
        //要把edges转成向量形式，不然会超时
        for(auto ed:edges)
        {
            e[ed[0]].push_back(ed[1]);
        }
        totalAns = 0;
        dfs(0);
        return totalAns*2;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/minimum-time-to-collect-all-apples-in-a-tree/