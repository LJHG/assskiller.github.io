---
title: 课程表---LeetCode210(拓扑排序)
date: 2020-05-17 23:22:17
tags: [拓扑排序, 图]
---
### 题目描述：  
现在你总共有 n 门课需要选，记为 0 到 n-1。
在选修某些课程之前需要一些先修课程。 例如，想要学习课程 0 ，你需要先完成课程 1 ，我们用一个匹配来表示他们: [0,1]
给定课程总量以及它们的先决条件，返回你为了学完所有课程所安排的学习顺序。
可能会有多个正确的顺序，你只要返回一种就可以了。如果不可能完成所有课程，返回一个空数组。
### 示例：   
```cpp
输入: 4, [[1,0],[2,0],[3,1],[3,2]]
输出: [0,1,2,3] or [0,2,1,3]
解释: 总共有 4 门课程。要学习课程 3，你应该先完成课程 1 和课程 2。并且课程 1 和课程 2 都应该排在课程 0 之后。
     因此，一个正确的课程顺序是 [0,1,2,3] 。另一个正确的排序是 [0,2,1,3] 。
```
<!-- more -->
### 解题思路:  
似曾相识的拓扑排序，感觉好像在算法课上讲过，这里也就当时温习(yuxi)一下了。  
这道题有两个思路，一个是dfs，一个是bfs。
### dfs
dfs想起来要稍微麻烦一些，当处理一个节点时，先要将他标记为正在处理(2)，然后去处理自己的相邻节点，如果发现了环，这里有两种情况：  
1. 我的相邻节点状态为正在处理(2)，那么存在环
2. 我的相邻节点在自己处理时发现了环
这两种情况，直接return false, 当自己和相邻节点都处理过后，把自己标记为完成处理(1)。
ps: 答案的记录是使用一个栈来记录的，最后再一个个弹出来就是正确答案了。
```cpp
class Solution {
public:
    vector<int> edges[10000]; //记录i节点指向的边
    int vis[10000]; //记录是否已经被加入栈
    stack<int> ansStack;

    bool dfs(int cur)
    {
        vis[cur] = 2; //表示尝试加入
        for(int i=0;i<edges[cur].size();i++)
        {
            if(vis[edges[cur][i]] == 2) {
                return false;
            }
            else if(vis[edges[cur][i]] == 0){
                if(!dfs(edges[cur][i])) return false;
            } 
            else{
                //nothing
            }
        }
       
        ansStack.push(cur);
        vis[cur] =1;
        return true;
    }


    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<int> ans;
       
        for(int i=0;i<numCourses;i++) edges[i].clear();
        memset(vis,0,sizeof(vis));
        int length = prerequisites.size();
        for(int i=0;i<length;i++)
        {
            edges[prerequisites[i][1]].push_back(prerequisites[i][0]);
        }
       
        for(int i=0;i<numCourses;i++)
        {
            if( vis[i]==0 ) {
                if(!dfs(i)) return ans;
            }
        }

     
        
        //把stack里的传到ans vector里面
        while(!ansStack.empty())
        {
            ans.push_back(ansStack.top());
            ansStack.pop();
        }

        
        // for(int i=0;i<numCourses;i++)
        // {
        //     for(int j=0;j<edges[i].size();j++)
        //     {
        //         cout<<edges[i][j]<<" ";
        //     }
        //     cout<<endl;
        // }

        return ans;
    }
};
```

### bfs
bfs的解法就简单很多了，一句话，一直找入度为0的点就行了，当处理完一个点，更新相邻节点的入度。

```cpp
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        //bfs实现
        vector<int> ans;
        //先统计入度
        int inD[10000];
        vector<int> edges[10000]; //邻接表
        for(int i=0;i<numCourses;i++) inD[i]=0;
        int length = prerequisites.size();
        for(int i=0;i<length;i++)
        {
            edges[prerequisites[i][1]].push_back(prerequisites[i][0]);
            inD[prerequisites[i][0]]++;
        }

        // //打印一下入度
        // for(int i=0;i<numCourses;i++) cout<<i<<"的入度为："<<inD[i]<<endl;

        // //打印一下边
        // for(int i=0;i<numCourses;i++) 
        // {
        //     cout<<i<<"的边为：";
        //     for(auto e :edges[i])
        //        cout<<e<<" ";
        //     cout<<endl;
        // }

        //一直把入度为0的点推进队列
        queue<int> q;
        for(int i=0;i<numCourses;i++)
        {
            if(inD[i] == 0)
                q.push(i);
        }
        while(!q.empty())
        {
            int cur = q.front();
            for(int i=0;i<edges[cur].size();i++)
            {
                inD[edges[cur][i]]--;
                if(inD[edges[cur][i]] ==0 )
                {
                    q.push(edges[cur][i]);
                }
            }
            ans.push_back(cur);
            q.pop();
            
        }
        //扫一遍，如果还存在入度不为0的，就return false
        for(int i=0;i<numCourses;i++)
        {
            if(inD[i] != 0) 
            {
                ans.clear();
                return ans;
            }
        }
        return ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/course-schedule-ii/