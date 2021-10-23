---
title: 递增子序列---LeetCode491(dp失败QAQ)
date: 2020-08-25 14:38:04
tags: [全排列,哈希去重]
---
## 题目描述：  
给定一个整型数组, 你的任务是找到所有该数组的递增子序列，递增子序列的长度至少是2。

## 示例：   
```cpp
示例:
输入: [4, 6, 7, 7]
输出: [[4, 6], [4, 7], [4, 6, 7], [4, 6, 7, 7], [6, 7], [6, 7, 7], [7,7], [4,7,7]]
说明:
给定数组的长度不会超过15。
数组中的整数范围是 [-100,100]。
给定数组中可能包含重复数字，相等的数字应该被视为递增的一种情况。
```
<!-- more -->

## 解题思路:  
这道题我看到的第一眼就是dp，dp就完事了，然后写得超级复杂，果断超时。  
然后去看了一下题解，全排列，数组长度最长15，emmm确实可以，反正比dp快多了。  
### dp
虽然dp奇慢无比，但还是说一下吧，毕竟是我的第一想法，而且长度太大了你也不能全排列了啊。   
说一下dp的思路，dp[i][j]表示从indexi到indexj里所有的递增序列(emmm，其实像这种dp里存的是向量的这种，我应该意识到多半不行了，毕竟存的东西还是太多了)  
dp[i][j] = Σ(dp[i][k-1] 拼上 k  + k拼上dp[k+1][j] + dp[i][k-1]拼上dp[k+1][j])  
贴下代码(写完一看，下面的循环都多少层了orz，这一看就过不了啊23333)
但是这里用的set去重，如果是用的哈希，或许能过，不过dp还是算了吧，跟全排列比起来还是太慢了  
```cpp
class Solution {
public:
    vector<vector<int>> findSubsequences(vector<int>& nums) {
        set<vector<int>> dp[16][16]; //dp[i][j]表示从下标i到下标j的所有递增子序列
        for(int i=0;i<16;i++)
            for(int j=0;j<16;j++)
                dp[i][j].clear();
        
        //这里先把单个的数字当作是递增子序列，这样比较好处理
        int len = nums.size();
        //按照长度为1进行初始化
        for(int i=0;i<len;i++)
        {
            vector<int> temp;
            temp.push_back(nums[i]);
            dp[i][i].insert(temp);
        }
        //按照长度为2来进行初始化
        for(int i=0;i+1<len;i++){
            vector<int> temp;
            if(nums[i+1]>nums[i]){
                temp.push_back(nums[i]);
                temp.push_back(nums[i+1]);
                dp[i][i+1].insert(temp);
            }
        }
        //按照选取数组长度作为外层循环
        for(int l=3;l<=len;l++){
            for(int i=0;i+l-1<len;i++){
                set<vector<int>> temp;
                for(int k=i;k<=i+l-1;k++){
                    
                    //左部分 dp[i][k-1]
                    //中间的数 nums[k]
                    //有部分 dp[k+1][j]
                    set<vector<int>> left;
                    int middle = nums[k];
                    set<vector<int>> right;

                    if(k-i >= 1){
                        //有左部分
                        left = dp[i][k-1];
                    }
                    if(i+l-1-k>=1){
                        //有右部分
                        right = dp[k+1][i+l-1];
                    }
                    int rlen = right.size();
                        for(auto x:right){
                            int vlen = x.size();
                            if(vlen > 0){
                                temp.insert(x);
                                if(x[0] >= middle){
                                    vector<int> pushV;
                                    pushV.push_back(middle);
                                    for(int kk=0;kk<vlen;kk++)
                                        pushV.push_back(x[kk]);
                                    temp.insert(pushV);
                                }
                            }
                        }
                    int llen = left.size();
                        for(auto x:left){
                            int vlen = x.size();
                            if(vlen > 0) {
                                temp.insert(x);
                                if(x[vlen-1] <= middle ){
                                    vector<int> pushV = x;
                                    pushV.push_back(middle);
                                    temp.insert(pushV);
                                }
                            }
                        }
                    //无视中间，左右互博
                    if(llen >0 && rlen>0){
                        for(auto lelement:left){
                            for(auto relement:right){
                                int llsize = lelement.size();
                                int rrsize = relement.size();
                                if(lelement[llsize-1] <= relement[0]){
                                    //拼一块形成新的序列
                                    vector<int> hhh;
                                    for(auto idk:lelement)
                                        hhh.push_back(idk);
                                    for(auto idk:relement)
                                        hhh.push_back(idk);
                                    temp.insert(hhh);
                                }
                            }
                        }
                    }
                }
                dp[i][i+l-1] = temp;
            }
        }
        vector<vector<int>> ans;
        for(auto x:dp[0][len-1]){
            if(x.size() >1)
                ans.push_back(x);
        }
        return ans;
    }
};
```

### 全排列
因为长度只有15，所以其实一共也就2^15种情况，不多，直接暴力枚举  
枚举完了需要去重，官方的题解是用的一个[很高级的哈希函数](https://leetcode-cn.com/problems/increasing-subsequences/solution/di-zeng-zi-xu-lie-by-leetcode-solution/)来映射的(这方法很牛逼，本来这个哈希才是这道题的精髓，不过对于我来说，全排列也很精髓了2333)，我这里就直接用set来去重了，效率不高，勉强过了。  
```cpp
class Solution {
public:
    vector<vector<int>> findSubsequences(vector<int>& nums) {
        int len = nums.size();
        int maxn = 1<<len;
        set<vector<int>> s;
        
        for(int i=0;i<=maxn;i++){
            vector<int> curV;
            int prev = -101;
            int isValid = 1;
            for(int k=0;k<len;k++){
                int curNum = 1<<k;
                if( (curNum & i) >= 1){
                    if(nums[k] >= prev){
                        prev = nums[k];
                        curV.push_back(nums[k]);
                    }else{
                        isValid = 0;
                        break;
                    }
                }
            }
            if(isValid && curV.size()>1){
                s.insert(curV);
            }
        }
        vector<vector<int>> ans;
        for(auto x:s){
            ans.push_back(x);
        }
        return ans;
    }
};
```
还可以用dfs的方式来进行枚举，大同小异
```cpp
class Solution {
public:
    int len;
    set<vector<int>> s;
    void dfs(int cur,vector<int> myNums,vector<int> & nums){
        if(cur == len){
            if(isValid(myNums)){
                s.insert(myNums);
            }
            return;
        }
        dfs(cur+1,myNums,nums);
        myNums.push_back(nums[cur]);
        dfs(cur+1,myNums,nums);
    }
    bool isValid(vector<int>& myNums){
        int prev = -101;
        int mylen = myNums.size();
        for(int i=0;i<mylen;i++){
            if(myNums[i] < prev){
                return false;
            }
            prev = myNums[i];
        }
        return true;
    }
    vector<vector<int>> findSubsequences(vector<int>& nums) {
        len = nums.size();
        vector<int> myNums;
        myNums.clear();
        dfs(0,myNums,nums);
        vector<vector<int>> ans;
        for(auto x:s){
            if(x.size() > 1)
                ans.push_back(x);
        }
        return ans;
    }
};
```
## 题目链接：  
https://leetcode-cn.com/problems/increasing-subsequences/