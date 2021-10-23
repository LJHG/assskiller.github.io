---
title: N皇后---LeetCode51(递归和回溯还是有区别的)
date: 2020-09-03 11:11:15
tags: [dfs,回溯]
---
## 题目描述：  
n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。
给定一个整数 n，返回所有不同的 n 皇后问题的解决方案。
每一种解法包含一个明确的 n 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。
皇后彼此不能相互攻击，也就是说：任何两个皇后都不能处于同一条横行、纵行或斜线上。

## 示例：   
```
输入：4
输出：[
 [".Q..",  // 解法 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // 解法 2
  "Q...",
  "...Q",
  ".Q.."]
]
解释: 4 皇后问题存在两个不同的解法。
```
<!-- more -->
## 解题思路:  
久闻大名的八皇后问题，一直没做，今天终于做了。  
这道题就是dfs，其实也不难。   
下面列三个解法吧，展示一下自己是如何一步一步优化下去的。  

### 无脑递归
无脑递归法就是看到有'.'，我就尝试在那个地方放一个Q，然后这样递归下去，超级慢，n=7就超时了。  
最后得到的结果还有可能重复，所以我还用set去了个重(看了一圈题解，根本就没有去重的，说明根本就没有人用这种方法23333)。  
```cpp
class Solution {
public:
    vector<vector<string>> ans;
    //先来一发无脑递归吧
    void dfs(int qqq,vector<vector<char>> matrix)
    {
        int n = matrix.size();
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<n;j++){
                if(matrix[i][j] == '.'){
                    //检查三个方向上是否有Q
                    int hasQ = 0;
                    int right = i+1;
                    int left = i-1;
                    int up = j-1;
                    int down = j+1;
                    while(right<n){
                        if(matrix[right][j] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        right++;
                    }
                    while(left>=0){
                        if(matrix[left][j] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        left--;
                    }
                    while(up>=0){
                        if(matrix[i][up] == 'Q'){
                            hasQ=1;
                            break;
                        }
                        up--;
                    }
                    while(down<n){
                        if(matrix[i][down] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        down++;
                    }
                    //还有主对角线判别一下
                    int duix = i+1;
                    int duiy = j+1;
                    while(duix<n && duiy<n){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix++;
                        duiy++;
                    }
                    duix = i-1;
                    duiy = j-1;
                    while(duix>=0 && duiy>=0){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix--;
                        duiy--;
                    }

                    //还有次对角线判别一下
                    duix = i+1;
                    duiy = j-1;
                    while(duix<n && duiy>=0){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix++;
                        duiy--;
                    }
                    duix = i-1;
                    duiy = j+1;
                    while(duix>=0 && duiy<n){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        duix--;
                        duiy++;
                    }

                    if(!hasQ){
                        vector<vector<char>> newMatrix = matrix; //这里要创建一个新数组
                        newMatrix[i][j] = 'Q';
                        if(qqq==n){
                            vector<string> vtemp;
                            for(int i=0;i<n;i++){
                                string temp;
                                for(int j=0;j<n;j++){
                                    temp  += newMatrix[i][j];
                                }
                                vtemp.push_back(temp);
                            }
                            ans.push_back(vtemp);//我觉得应该会有很多重复。。。。
                        }else{
                            dfs(qqq+1,newMatrix);
                        }
                    }
                }
            }
        }
    }
    void initMatrix(vector<vector<char>>& matrix,int n)
    {
        for(int i=0;i<n;i++){
            vector<char> temp;
            temp.clear();
            for(int j=0;j<n;j++){
                temp.push_back('.');
            }
            matrix.push_back(temp); 
        }
    }
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<char>> matrix;
        initMatrix(matrix,n);
        dfs(1,matrix);
        //用set去重?
        set<vector<string>> s;
        int len = ans.size();
        for(int i=0;i<len;i++){
            s.insert(ans[i]);
        }
        vector<vector<string>> newAns;
        for(auto x:s){
            newAns.push_back(x);
        }
        return newAns;
    }
};
```

### 有脑递归
稍微想一下就可以发现，每一行一定是只能放一个Q的，所以其实我就可以让第一个Q放在第一行，第二个放在第二行。。。。。也就是说，在第一行中找一个'.'来放Q，而不是在整个矩阵中看到'.'就放Q。这样一来，就可以直接去掉一重循环，而且去重也不需要了，优化效果爆表。  

```cpp
class Solution {
public:
    vector<vector<string>> ans;
    void dfs(int qqq,vector<vector<char>> matrix)
    {
        int n = matrix.size();
        // for(int i=0;i<n;i++)
        // {
            int i =qqq-1;
            for(int j=0;j<n;j++){
                if(matrix[i][j] == '.'){
                    //检查三个方向上是否有Q
                    int hasQ = 0;
                    int right = i+1;
                    int left = i-1;
                    int up = j-1;
                    int down = j+1;
                    while(right<n){
                        if(matrix[right][j] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        right++;
                    }
                    while(left>=0){
                        if(matrix[left][j] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        left--;
                    }
                    while(up>=0){
                        if(matrix[i][up] == 'Q'){
                            hasQ=1;
                            break;
                        }
                        up--;
                    }
                    while(down<n){
                        if(matrix[i][down] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        down++;
                    }
                    //还有主对角线判别一下
                    int duix = i+1;
                    int duiy = j+1;
                    while(duix<n && duiy<n){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix++;
                        duiy++;
                    }
                    duix = i-1;
                    duiy = j-1;
                    while(duix>=0 && duiy>=0){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix--;
                        duiy--;
                    }

                    //还有次对角线判别一下
                    duix = i+1;
                    duiy = j-1;
                    while(duix<n && duiy>=0){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix++;
                        duiy--;
                    }
                    duix = i-1;
                    duiy = j+1;
                    while(duix>=0 && duiy<n){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        duix--;
                        duiy++;
                    }

                    if(!hasQ){
                        vector<vector<char>> newMatrix = matrix; //这里要创建一个新数组
                        newMatrix[i][j] = 'Q';
                        if(qqq==n){
                            vector<string> vtemp;
                            for(int i=0;i<n;i++){
                                string temp;
                                for(int j=0;j<n;j++){
                                    temp  += newMatrix[i][j];
                                }
                                vtemp.push_back(temp);
                            }
                            ans.push_back(vtemp);//我觉得应该会有很多重复。。。。
                        }else{
                            dfs(qqq+1,newMatrix);
                        }
                    }
                }
            }
        
    }
    void initMatrix(vector<vector<char>>& matrix,int n)
    {
        for(int i=0;i<n;i++){
            vector<char> temp;
            temp.clear();
            for(int j=0;j<n;j++){
                temp.push_back('.');
            }
            matrix.push_back(temp); 
        }
    }
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<char>> matrix;
        initMatrix(matrix,n);
        dfs(1,matrix);
        // //用set去重?
        // set<vector<string>> s;
        // int len = ans.size();
        // for(int i=0;i<len;i++){
        //     s.insert(ans[i]);
        // }
        // vector<vector<string>> newAns;
        // for(auto x:s){
        //     newAns.push_back(x);
        // }
        // return newAns;
        return ans;
    }
};
```

### 回溯
这里要说明一下回溯法和递归的区别。可以看到，在上面的方法中，为了不改变原有的矩阵，我没有用引用，而是采用复制一个新矩阵的方式来传参的。而如果采用回溯法，就可以直接传引用了。这样就可以避免到数组复制的时间，从而得到很大的性能提升。  
回溯法的思想很简单
```
matrix[i][j] = 'Q'; //改变原数组(尝试在这个地方放Q)
dfs(i+1,matrix); //求解
matrix[i][j] = '.' //还原
```
啊你可能会想(我可能会想)，dfs里面不是改变了matrix的很多其它位置吗，你最后把自己还原了有啥用？  
其实是这样的，当dfs这一行执行完后，dfs里面套的dfs等等等其实都执行完了，所以其实最后全都被还原为'.'了,所以其实是没毛病的。
回溯法比纯递归要稍微绕一点点，多想一想就行了，而且带来的性能提升是巨大的，以后如果想要不复制新数组传参，不妨想一想是否能用回溯法来实现引用传参。  
```cpp
class Solution {
public:
    vector<vector<string>> ans;
    //回溯法
    void dfs(int qqq,vector<vector<char>>& matrix)
    {
        int n = matrix.size();
            int i =qqq-1;
            for(int j=0;j<n;j++){
                if(matrix[i][j] == '.'){
                    //检查三个方向上是否有Q
                    int hasQ = 0;
                    int right = i+1;
                    int left = i-1;
                    int up = j-1;
                    int down = j+1;
                    while(right<n){
                        if(matrix[right][j] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        right++;
                    }
                    while(left>=0){
                        if(matrix[left][j] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        left--;
                    }
                    while(up>=0){
                        if(matrix[i][up] == 'Q'){
                            hasQ=1;
                            break;
                        }
                        up--;
                    }
                    while(down<n){
                        if(matrix[i][down] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        down++;
                    }
                    //还有主对角线判别一下
                    int duix = i+1;
                    int duiy = j+1;
                    while(duix<n && duiy<n){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix++;
                        duiy++;
                    }
                    duix = i-1;
                    duiy = j-1;
                    while(duix>=0 && duiy>=0){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix--;
                        duiy--;
                    }

                    //还有次对角线判别一下
                    duix = i+1;
                    duiy = j-1;
                    while(duix<n && duiy>=0){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ =1;
                            break;
                        }
                        duix++;
                        duiy--;
                    }
                    duix = i-1;
                    duiy = j+1;
                    while(duix>=0 && duiy<n){
                        if(matrix[duix][duiy] == 'Q'){
                            hasQ = 1;
                            break;
                        }
                        duix--;
                        duiy++;
                    }

                    if(!hasQ){
                        matrix[i][j] = 'Q'; //先赋为Q
                        if(qqq==n){
                            vector<string> vtemp;
                            for(int i=0;i<n;i++){
                                string temp;
                                for(int j=0;j<n;j++){
                                    temp  += matrix[i][j];
                                }
                                vtemp.push_back(temp);
                            }
                            ans.push_back(vtemp);//我觉得应该会有很多重复。。。。
                        }else{
                            dfs(qqq+1,matrix);
                        }
                        matrix[i][j] = '.'; //然后再赋回来
                    }
                }
            }
        
    }
    void initMatrix(vector<vector<char>>& matrix,int n)
    {
        for(int i=0;i<n;i++){
            vector<char> temp;
            temp.clear();
            for(int j=0;j<n;j++){
                temp.push_back('.');
            }
            matrix.push_back(temp); 
        }
    }
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<char>> matrix;
        initMatrix(matrix,n);
        dfs(1,matrix);
        return ans;
    }
};
```


## 题目链接：  
https://leetcode-cn.com/problems/n-queens/
[一个讲的不错的题解](https://leetcode-cn.com/problems/n-queens/solution/nhuang-hou-jing-dian-hui-su-suan-fa-tu-wen-xiang-j/)