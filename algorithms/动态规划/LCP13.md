---
title: 寻宝---LCP13(bfs+状压dp)
date: 2020-07-29 16:49:32
tags: [dp,动态规划,bfs,状态压缩]
---
## 题目描述：  
我们得到了一副藏宝图，藏宝图显示，在一个迷宫中存在着未被世人发现的宝藏。
迷宫是一个二维矩阵，用一个字符串数组表示。它标识了唯一的入口（用 'S' 表示），和唯一的宝藏地点（用 'T' 表示）。但是，宝藏被一些隐蔽的机关保护了起来。在地图上有若干个机关点（用 'M' 表示），只有所有机关均被触发，才可以拿到宝藏。
要保持机关的触发，需要把一个重石放在上面。迷宫中有若干个石堆（用 'O' 表示），每个石堆都有无限个足够触发机关的重石。但是由于石头太重，我们一次只能搬一个石头到指定地点。
迷宫中同样有一些墙壁（用 '#' 表示），我们不能走入墙壁。剩余的都是可随意通行的点（用 '.' 表示）。石堆、机关、起点和终点（无论是否能拿到宝藏）也是可以通行的。
我们每步可以选择向上/向下/向左/向右移动一格，并且不能移出迷宫。搬起石头和放下石头不算步数。那么，从起点开始，我们最少需要多少步才能最后拿到宝藏呢？如果无法拿到宝藏，返回 -1 。

## 示例：   
```cpp
输入： ["S#O", "M..", "M.T"]
输出：16

解释：最优路线为： S->O, cost = 4, 去搬石头 O->第二行的M, cost = 3, M机关触发 第二行的M->O, cost = 3, 我们需要继续回去 O 搬石头。 O->第三行的M, cost = 4, 此时所有机关均触发 第三行的M->T, cost = 2，去T点拿宝藏。 总步数为16。 
```
<!-- more -->

## 解题思路:  
一杯水，一包烟，一道dp写一天。  
这道题真神了，我记得当初春季大赛我第一看到就果断放弃，今天又看到这道题作为每日一题，心想着还是做一做，然后就做了一天23333。  
这道题主要有两个比较重要的点，一个是如何对数据进行预处理，一个是如何dp。  
先说如何对数据进行预处理吧，这道题的一个过程可以看作是从一个机关->石头->另一个机关这种方式在走，所以我们需要**先求出所有机关到所有石头的距离**(通过对每一个机关bfs来做)，为了方便计算，我们把开始点也当作一个机关。同时还要计算所有机关到终点的距离。  
然而要进行上面的操作，我们要**先找到所有的机关和石头**，所以先要进行一次全局的bfs来找这些东西，还要找开始位置和终点。  
在进行了所有的这些操作后，还没完，我们还要**预先把机关到机关的距离求出来**，因为这道题虽然说是从机关->石头->机关，但本质上可以看作是机关之间的跳转，所以还要算一算机关之间的最小距离(也就是说，从一个机关到另一个机关经过哪块石头距离最小)，把这些都算完了，才算预处理结束。(真的，NB)。  
然后我们就可以开始dp了，dp的式子是这样的dp[20][1<<17],**dp[i][j]表示以j为机关序列，最后一个处理的机关是i**，比如dp[1][3]就是序列为11的机关，最后一个处理的是index为1的机关。  
然后可以列出状态转移方程 **dp[i][state] = min(dp[j][state-(1<<i)+dis[i][j]])** 
然后还有一个要注意的点就是dp的循环该怎么写，最开始我一直没想到dp最外层的循环该怎么写，后来看了一下别人的代码，最外层的循环是state,而且就是从小到大遍历的，想了一下还是有道理。  

```cpp
class Solution{
public:
    int INF = 999999;
    struct node{
        int x;
        int y;
    };
    int togo[4][2]={ {-1,0},{0,-1},{1,0},{0,1} };
    int minimalSteps(vector<string>& maze) {
        //先找到所有的石头和机关
        //因为是100*100 所以没有必要构建结构体，直接把用x<<10 + y来表示坐标
        int xlen = maze.size();
        int ylen = maze[0].size();
        vector<int> stones;
        vector<int> triggers;
        int start;
        int target;
        queue<node> q;
        node n;
        n.x = 0;
        n.y = 0;
        q.push(n);
        int vis[101][101]; memset(vis,0,sizeof(vis));
        vis[0][0] =1;
        while(!q.empty()){
            node curNode = q.front();
            q.pop();
            if(maze[curNode.x][curNode.y] == 'O') stones.push_back((curNode.x << 10) + curNode.y);
            if(maze[curNode.x][curNode.y] == 'M') triggers.push_back((curNode.x << 10) + curNode.y);
            if(maze[curNode.x][curNode.y] == 'S') start = (curNode.x<<10)+curNode.y;
            if(maze[curNode.x][curNode.y] == 'T') target = (curNode.x<<10)+curNode.y;
            //vis[curNode.x][curNode.y] = 1;
            for(int i=0;i<4;i++){
                int x = togo[i][0] + curNode.x;
                int y = togo[i][1] + curNode.y;
                if(x>=0 && x<xlen && y>=0 && y<ylen && !vis[x][y]){
                    node newNode;
                    newNode.x = x;
                    newNode.y = y;
                    q.push(newNode);
                    vis[x][y] = 1; //加入了queue就要标记为vis,在处理时才标记就晚了
                }
            }
        }

        //找到了所有的坐标，现在可以开始计算机关和各个石头之间的距离了
        int dis[20][50];//dis[i][j]表示编号为i的机关，到编号为j的石头的距离，编号指的是在vector中的index
        int disToEnd[20];
        //把start当成是编号为0的机关
        triggers.insert(triggers.begin(),start);
        for(int i=0;i<20;i++){
            disToEnd[i] = INF;
            for(int j=0;j<50;j++)
                dis[i][j] = INF;
        }
            
        //对每一个机关做bfs
        struct node2{
            int x;
            int y;
            int dis;
        };
        for(int i=0;i<triggers.size();i++){
            node2 start;
            start.x = triggers[i]>>10;
            start.y = triggers[i]&1023;
            start.dis = 0;
            queue<node2> q;
            q.push(start);
            memset(vis,0,sizeof(vis));
            vis[start.x][start.y] = 1;
            while(!q.empty()){
                node2 curNode = q.front();
                q.pop();
                int x = curNode.x;
                int y = curNode.y;
                int curDis = curNode.dis;
                if(maze[x][y] == '#') continue; //遇到石头终止
                if(maze[x][y] == 'T') disToEnd[i] = curDis;
                if(maze[x][y] == 'O'){
                    for(int j=0;j<stones.size();j++){
                        if(stones[j] == (x <<10) + y){
                            dis[i][j] = curDis;
                            break;
                        }
                    }
                }
                for(int k=0;k<4;k++){
                    int tox = x + togo[k][0];
                    int toy = y + togo[k][1];
                    if(tox >=0 && tox < xlen && toy >=0 && toy<ylen && !vis[tox][toy]){
                        node2 newNode;
                        newNode.x = tox;
                        newNode.y = toy;
                        newNode.dis = curDis+1;
                        q.push(newNode);
                        vis[tox][toy] = 1;
                    }
                }
            }
            
        }
        int dp[20][1<<17]; //dp[i][j]表示当前在第i个机关，当前打开的机关序列的状态
        for(int i=0;i<20;i++){
            for(int j=0;j<(1<<17);j++)
            {
                dp[i][j] = INF;
            }
        }
         
        /**
        对每一个机关到其它所有机关的距离做一个预处理，不然要超时
        */
        int triggerDis[20][20];
        for(int i=0;i<20;i++)
            for(int j=0;j<20;j++)
                triggerDis[i][j]  = INF;
        
        for(int i=0;i<20;i++)
        {
            for(int j=0;j<20;j++)
            {
                if(i == j ){
                    triggerDis[i][j]  =0;
                    continue;
                } 
                for(int stoneNum = 0;stoneNum<stones.size();stoneNum++){
                    int temp = dis[i][stoneNum] + dis[j][stoneNum];
                    triggerDis[i][j] = min(triggerDis[i][j],temp);
                }
            }
        }
        

        dp[0][1] = 0; //当前在0号机关(start)，解锁机关为0号机关的开销为0
        int tlen = triggers.size();
        int slen = stones.size();
        for(int state=3;state<(1<<tlen);state++){
            if((state & 1) == 0 ) continue; //如果0号机关没有打开，是不可能的
            for(int finalTri = 1;finalTri<tlen;finalTri++){ //选定最后当前的trigger为finaltri
                if( (state &(1<<finalTri)) == 0 )continue;
                int hasLast = 0;
                for(int lastTri = 1;lastTri<tlen;lastTri++){//选定是从谁到finaltri
                    if(finalTri == lastTri ) continue;
                    if(state & (1<<lastTri)){
                        hasLast = 1;
                        dp[finalTri][state] = min(dp[finalTri][state],triggerDis[lastTri][finalTri]+dp[lastTri][state-(1<<finalTri)]);
                    }
                }
                if(!hasLast){ //那么lastTri肯定是0
                    dp[finalTri][state] = min(dp[finalTri][state],triggerDis[0][finalTri]+dp[0][state-(1<<finalTri)]);
                }
            }
            
        }
        int finalState = (1<<tlen) -1;
        int ans = INF;
        for(int i=1;i<tlen;i++)
        {
            ans = min(ans,dp[i][finalState] + disToEnd[i]);
        }
        if(tlen == 1){
            //没有trigger
            ans = disToEnd[0];
        }
        if(ans == INF) return -1;
        return ans;  
    }
};
```
## 题目链接：  
https://leetcode-cn.com/problems/xun-bao/