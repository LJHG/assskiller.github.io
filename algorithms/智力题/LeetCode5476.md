---
title: 找出数组游戏的赢家---LeetCode5476
date: 2020-08-02 15:25:05
tags: []
---
## 题目描述：  
给你一个由 不同 整数组成的整数数组 arr 和一个整数 k 。

每回合游戏都在数组的前两个元素（即 arr[0] 和 arr[1] ）之间进行。比较 arr[0] 与 arr[1] 的大小，较大的整数将会取得这一回合的胜利并保留在位置 0 ，较小的整数移至数组的末尾。当一个整数赢得 k 个连续回合时，游戏结束，该整数就是比赛的 赢家 。
返回赢得比赛的整数。
题目数据 保证 游戏存在赢家。


## 示例：   
```cpp
输入：arr = [2,1,3,5,4,6,7], k = 2
输出：5
因此将进行 4 回合比赛，其中 5 是赢家，因为它连胜 2 回合。
```
<!-- more -->

## 解题思路:  
这道题其实很简单，但是我做的很复杂，这里还是给两个解法吧，虽然我的那个解法不是很好，还是提一下2333。  
### 真就纯模拟呗
我看到这道题的第一眼，也想过一些其他的解法，比如从头到尾比一比可能就可以了之类的，但是也没想多，就否决了这些做法，然后搞了一个纯模拟。  
而且因为要模拟，为了避免数组的移动，我理所应当地使用了链表，真的麻烦。  

```cpp
class Solution {
public:
    struct node{
        int num;
        node* next;
        node(int x) : num(x), next(NULL) {}
    };
    

    int getWinner(vector<int>& arr, int k) {
        int len = arr.size();
        //先转成链表
        struct node* head = new node(0);
        struct node* curNode = head;
        for(int i=0;i<len;i++){
            struct node* newNode = new node(arr[i]);
            newNode->next = NULL;
            curNode->next = newNode;
            curNode = newNode;
        }
        struct node* lastNode = curNode;
        curNode = head;
        //构建完毕,开始模拟
        
            struct node* firstNode = head->next;
            struct node* secondNode = head->next->next;
            int cnt = 0;
            int i = 0;
            while(1)
            {
                i++;
                if(firstNode->num > secondNode->num){
                    firstNode->next = secondNode->next;
                    lastNode->next = secondNode;
                    secondNode->next = NULL;
                    lastNode = secondNode;
                    cnt++;
                    if(cnt > len) return firstNode->num;
                    if(cnt==k) return firstNode->num;
                }else{
                    head->next = secondNode;
                    lastNode->next = firstNode;
                    firstNode->next = NULL;
                    lastNode = firstNode;
                    
                    cnt = 1;
                    if(cnt == k) return secondNode->num;
                } 
                firstNode = head->next;
                secondNode = head->next->next;
            }   
        return 0;
    }
};
```

### 稍微想一想的做法
其实这道题稍微想一想就会发现，真的很简单。  
因为每次比赛都会把大的数作为擂主，所以当前的擂主就是当前最大的数，然后我从头到尾遍历一遍不就完了吗？  
所以一个数要么被一个更大的数替代，要么就连续赢了K次，可能你会说啊不是还没比到K次就结束了的情况吗？(OS)，你想一想，如果还没比到K次就结束了，那么当前的擂主一定是这整个数组中最大的数，那么他一定就是winner啊。  
```cpp
class Solution {
public:
    int getWinner(vector<int>& arr, int k) {
        int len = arr.size();
        int winner=arr[0];
        int cnt = 0;
        for(int i=1;i<len;i++){
            if(arr[i]<winner){
                cnt++;
            }else{
                cnt = 1;
                winner = arr[i];
            }
            if(cnt == k) return winner;
        }
        return winner;
    }
};
```



## 题目链接：  
https://leetcode-cn.com/problems/find-the-winner-of-an-array-game/