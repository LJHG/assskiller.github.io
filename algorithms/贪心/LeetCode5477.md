---
title: 排布二进制网格的最少交换次数---LeetCode5477
date: 2020-08-02 15:55:48
tags: [贪心]
---
## 题目描述：  
给你一个 n x n 的二进制网格 grid，每一次操作中，你可以选择网格的 相邻两行 进行交换。
一个符合要求的网格需要满足主对角线以上的格子全部都是 0 。
请你返回使网格满足要求的最少操作次数，如果无法使网格符合要求，请你返回 -1 。
主对角线指的是从 (1, 1) 到 (n, n) 的这些格子。

## 示例：   
```cpp
输入：grid = [[0,0,1],[1,1,0],[1,0,0]]
输出：3
```
<!-- more -->

## 解题思路:  
这道题我没做出来，因为我没想到这道题是真模拟啊。。。我还以为不需要去swap什么的，然后还去考虑了一下交换后其他行的开销+1什么什么的，想麻烦了，谁想到这道题还真就是直接swap，而且还是贪心。  
说一下贪心的思路: 从该行往下，寻找第一个能够放到该行的行。  
这样想想还真的没毛病，最开始我还在想，会不会有本来有很多0的行去放到一个比较靠下的位置从而使得上面一个需要这么多0的行无行可选，这种情况是不可能的！因为是从上往下遍历的，所以一定会优先去满足上面的位置，也就是说，就算一个行把0最多的选了也没关系，因为它就是目前需要0最多的。  
贪心的话，也没什么好证明的，就这样吧。

```cpp
class Solution {
public:
    void swap(int* mem,int i,int j){
        int temp = mem[i];
        mem[i] = mem[j];
        mem[j] = temp;
    }

    int minSwaps(vector<vector<int>>& grid) {
        int len = grid.size();
        int mem[200];
        memset(mem,0,sizeof(mem));
        for(int i=0;i<len;i++)
        {
            int j = len;
            int num = 0;
            while(j--){
                if(grid[i][j] == 0 )
                {
                    num++;
                }else{
                    break;
                }
            }
            mem[i]=num; //第i行0的个数为num
        }
        int ans = 0;
        for(int i=0;i<len;i++){
            if(mem[i] >= len-i-1) continue;
            int swapRow = -1;
            for(int j=i+1;j<len;j++){
                if(mem[j] >= len-i-1){
                    swapRow = j;
                    break;
                }
            }
            if(swapRow == -1) return -1;
            //找到交换的行，开始交换
            for(int j=swapRow;j>=i+1;j--){
                swap(mem,j,j-1);
                ans++;
            }
        }
        return ans;

    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/minimum-swaps-to-arrange-a-binary-grid/