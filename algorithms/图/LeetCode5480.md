---
title: 可以到达所有点的最少点数目---LeetCode5480
date: 2020-08-23 21:58:43
tags: [图]
---
## 题目描述：  
给你一个 有向无环图 ， n 个节点编号为 0 到 n-1 ，以及一个边数组 edges ，其中 edges[i] = [fromi, toi] 表示一条从点  fromi 到点 toi 的有向边。
找到最小的点集使得从这些点出发能到达图中所有点。题目保证解存在且唯一。
你可以以任意顺序返回这些节点编号。

<!-- more -->

## 示例：   
```cpp
输入：n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
输出：[0,3]
解释：从单个节点出发无法到达所有节点。从 0 出发我们可以到达 [0,1,2,5] 。从 3 出发我们可以到达 [3,4,2,5] 。所以我们输出 [0,3] 。
```

## 解题思路:
这次的双周赛和周赛，其他的题稍微整一整还是能整出来，这道题是真的掉坑里面去了，记录一下。  
这道题最开始我使用了两种方法，稍微记录一下自己的心路历程。  
### 方法1---暴力查找每一个点的超父
总而言之，就是对于每一个点找到它的源头，复杂度尤其之高，加入一个记录数组后会好很多，但还是一个非常非常低效的方法。  
具体的实现就是对于一个节点，在edges里找到一个节点指向它，然后把起点作为新的节点来再找.....
无脑暴力不可取，这道题想到这种方法还是走远了。  
```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        //关键就是找到最爸爸
        int ultiFather[10010];
        for(int i=0;i<10010;i++)ultiFather[i] = -1;
        //开始对每一个节点找最爸爸
        int len = edges.size();
        for(int node=0;node<n;node++){
            int curNode = node;
            while(1){
                int flag=0;
                int isfind = 0;
                for(int i=0;i<len;i++){
                    if(curNode == edges[i][1]){
                        flag = 1;
                        if(ultiFather[edges[i][0]]!=-1){
                            ultiFather[curNode] = ultiFather[edges[i][0]];
                            ultiFather[node] = ultiFather[edges[i][0]];
                            isfind = 1;
                            //curNode = ultiFather[edges[i][0]];
                            break;
                        }else{
                            curNode = edges[i][0];
                            break;
                        }
                    }
                }
                if(isfind==1) break;
                if(flag == 0){
                    ultiFather[node] = curNode;
                    break;
                }
            }   
        }
        vector<int> ans;
        int vis[10010];
        memset(vis,0,sizeof(vis));
        for(int i=0;i<n;i++){
            //cout<<ultiFather[i]<<endl;
            if(!vis[ultiFather[i]]){
                ans.push_back(ultiFather[i]);
                vis[ultiFather[i]]=1;
            }
        }
        return ans;

    }
};
```

### 方法2---统计入度为0的点
还是比较容易想到的(我没想到),一想到这个，一枪秒了，有什么好说的。  
然后一不小心又掉坑里了
```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        int len = edges.size();
        vector<int> ans;
        for(int node=0;node<n;node++){
            int flag = 1;
            for(int i=0;i<len;i++){
                if(edges[i][1] == node){
                    flag=0;
                    break;
                }
            }
            if(flag){
                ans.push_back(node);
            }
        }
        return ans;
    }
    
};

```

可以见到，上面的做法我是对于每一个节点做外层循环，然后去统计每一个点的入度，还是太慢了，其实对edges数组扫一遍就完事了。
```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        int len = edges.size();
        vector<int> ans;
        int indegree[100010];
        memset(indegree,0,sizeof(indegree));
        for(int i=0;i<len;i++){
            indegree[edges[i][1]]++;
        }
        for(int i=0;i<n;i++)
        {
            if(indegree[i]==0) ans.push_back(i);
        }
        return ans;
    }
    
};
```

## 题目链接：  
https://leetcode-cn.com/problems/minimum-number-of-vertices-to-reach-all-nodes/