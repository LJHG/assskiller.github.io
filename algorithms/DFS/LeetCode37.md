---
title: 解数独---LeetCode37(优化的力量)
date: 2020-09-15 16:21:16
tags: [dfs,回溯]
---
## 题目描述：  
编写一个程序，通过已填充的空格来解决数独问题。
一个数独的解法需遵循如下规则：
数字 1-9 在每一行只能出现一次。
数字 1-9 在每一列只能出现一次。
数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。
空白格用 '.' 表示。

## 示例：   
```
解就完事了
```
<!-- more -->

## 解题思路:  
这道题一共采用三个方法(算是吧)，逐步优化，还是挺有意思的。  
### 最老实的递归(636ms)
这个方法真的非常朴素，就是一点都不取巧那种。   
我专门编写了一个check函数来看当前的数独是否满足条件，目标就是每次填了数字后查看是否满足条件(后面的方法你会发现没必要专门编写一个函数来check，后面再说吧)。  
我专门编写了一个findPos函数来每次都去查找第一个没有填的位置(其实也没必要，后面就知道了)。  
我还编写了一个isFull函数来看当前的数独是否填满了。(其实也没必要，后面就知道了)。  
虽然很多没有必要，但是回溯至少是没毛病的，💪。  
```cpp
class Solution {
public:
    int flag[10];
    vector<vector<char>> ans;
    bool checkSudoku(vector<vector<char>>& board){
        //检查每一行
        for(int i=0;i<9;i++){
            memset(flag,0,sizeof(flag));
            for(int j=0;j<9;j++){
                if(board[i][j] > 48){
                    int temp = board[i][j] -48;
                    if(flag[temp]){
                        return false;
                    }
                    flag[temp] = 1;
                }
            }
        }
        //检查每一列
        for(int i=0;i<9;i++){
            memset(flag,0,sizeof(flag));
            for(int j=0;j<9;j++){
                if(board[j][i] > 48){
                    int temp = board[j][i] -48;
                    if(flag[temp]){
                        return false;
                    }
                    flag[temp] = 1;
                }
            }
        }
        //检查每一个宫格
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                memset(flag,0,sizeof(flag));
                for(int m=0;m<3;m++){
                    for(int n=0;n<3;n++){
                        if(board[i*3+m][j*3+n] > 48){
                            int temp = board[i*3+m][j*3+n] - 48;
                            if(flag[temp]){
                                return false;
                            }
                            flag[temp] = 1;
                        }
                    }
                }
            }
        }
        return true;

    }
    bool isFull(vector<vector<char>>& board){
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board[i][j] == '.')return false;
            }
        }
        return true;
    }
    pair<int,int> findPos(vector<vector<char>>& board){
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board[i][j] == '.'){
                    return make_pair(i,j);
                }
            }
        }
        return make_pair(-1,-1);
    }
    void dfs(vector<vector<char>>& board){
        if(checkSudoku(board)){
            if(isFull(board)){
                ans = board;
                return;
            }
            //找到第一个没有填的位置
            pair<int,int> pos = findPos(board);
            int posi = pos.first;
            int posj = pos.second;
            for(int num=1;num<=9;num++){
                board[posi][posj] = num +48;
                dfs(board);
                board[posi][posj] = '.';
            }
        }else{
            return;
        }
    }
    void solveSudoku(vector<vector<char>>& board) {
        //硬暴力来一发试试
        dfs(board);
        board = ans;
        
    }
};
```

### check啥呀，不用check啊(48ms)
每一次dfs都去check一下真的很费时间，所以如果能够把check去掉，岂不美哉。  
是可以的，我们可以记录每一行，每一列，每一个block可以填的数字序列，然后在填'.'的时候只填那些满足条件的数字不就行了么。  
```cpp
class Solution {
public:
    int flag[10];
    vector<vector<char>> ans;
    int row[10][10];
    int col[10][10];
    int block[3][3][10];
    bool isFull(vector<vector<char>>& board){
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board[i][j] == '.')return false;
            }
        }
        return true;
    }
    pair<int,int> findPos(vector<vector<char>>& board){
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board[i][j] == '.'){
                    return make_pair(i,j);
                }
            }
        }
        return make_pair(-1,-1);
    }
    void dfs(vector<vector<char>>& board){
        if(isFull(board)){
            ans = board;
            return;
        }
        //找到第一个没有填的位置
        pair<int,int> pos = findPos(board);
        int posi = pos.first;
        int posj = pos.second;
        for(int num=1;num<=9;num++){
            if(row[posi][num] == 0 && col[posj][num] == 0 && block[posi/3][posj/3][num] == 0)
            {
                board[posi][posj] = num +48;
                row[posi][num] = 1;
                col[posj][num] = 1;
                block[posi/3][posj/3][num] =1;
                dfs(board);
                board[posi][posj] = '.';
                row[posi][num] = 0;
                col[posj][num] = 0;
                block[posi/3][posj/3][num] =0;
            } 
        }
    }
    void solveSudoku(vector<vector<char>>& board) {
        //硬暴力来一发试试
        memset(row,0,sizeof(row));
        memset(col,0,sizeof(col));
        memset(block,0,sizeof(block));
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board[i][j] > 48){
                    row[i][board[i][j] - 48] = 1;
                    col[j][board[i][j] - 48] = 1;
                    block[i/3][j/3][board[i][j] - 48] = 1;
                }
               
            }
        }
        dfs(board);
        board = ans; 
    }
};
```

### 也别判full了，别findPos了，带上位置一起dfs吧(8ms)
进一步想，一直判满和找第一个'.'的位置不也挺奇怪的吗。  
然后想到这个这种dfs其实是可以按顺序一个一个走的，类比组合数的一个一个位置判断取不取，八皇后的一行一行来。。。。  
所以我们可以带上位置dfs，满就是走到最后一个位置，findPos也没必要了，毕竟我都是一个一个走下来的。
```cpp
class Solution {
public:
    vector<vector<char>> ans;
    int row[10][10];
    int col[10][10];
    int block[3][3][10];

    void dfs(vector<vector<char>>& board,int i,int j){
        if(i==9){
            ans = board;
            return;
        }
        if(board[i][j] == '.'){
            for(int num=1;num<=9;num++){
                if(row[i][num] == 0 && col[j][num] == 0 && block[i/3][j/3][num] == 0)
                {
                    board[i][j] = num +48;
                    row[i][num] = 1;
                    col[j][num] = 1;
                    block[i/3][j/3][num] =1;
                    dfs(board,i+(j+1>=9),(j+1)%9);
                    board[i][j] = '.';
                    row[i][num] = 0;
                    col[j][num] = 0;
                    block[i/3][j/3][num] =0;
                } 
            }
        }
        else{
            dfs(board,i+(j+1>=9),(j+1)%9);
        }
    }
   
    void solveSudoku(vector<vector<char>>& board) {
        //硬暴力来一发试试
        memset(row,0,sizeof(row));
        memset(col,0,sizeof(col));
        memset(block,0,sizeof(block));
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board[i][j] > 48){
                    row[i][board[i][j] - 48] = 1;
                    col[j][board[i][j] - 48] = 1;
                    block[i/3][j/3][board[i][j] - 48] = 1;
                }
               
            }
        }
        dfs(board,0,0);
        board = ans; 
    }
};
```

这道题还可以做一些更nb的优化，这里就就不多说了。  

## 题目链接：  
https://leetcode-cn.com/problems/sudoku-solver/