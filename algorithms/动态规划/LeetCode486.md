---
title: 预测赢家---LeetCode486(博弈)
date: 2020-09-01 10:50:53
tags: [博弈,递归,动态规划,dp,dfs]
---
## 题目描述：  
给定一个表示分数的非负整数数组。 玩家 1 从数组任意一端拿取一个分数，随后玩家 2 继续从剩余数组任意一端拿取分数，然后玩家 1 拿，…… 。每次一个玩家只能拿取一个分数，分数被拿取之后不再可取。直到没有剩余分数可取时游戏结束。最终获得分数总和最多的玩家获胜。
给定一个表示分数的数组，预测玩家1是否会成为赢家。你可以假设每个玩家的玩法都会使他的分数最大化。

## 示例：   
```cpp
示例 1：
输入：[1, 5, 2]
输出：False
解释：一开始，玩家1可以从1和2中进行选择。
如果他选择 2（或者 1 ），那么玩家 2 可以从 1（或者 2 ）和 5 中进行选择。如果玩家 2 选择了 5 ，那么玩家 1 则只剩下 1（或者 2 ）可选。
所以，玩家 1 的最终分数为 1 + 2 = 3，而玩家 2 为 5 。
因此，玩家 1 永远不会成为赢家，返回 False 。

示例 2：
输入：[1, 5, 233, 7]
输出：True
解释：玩家 1 一开始选择 1 。然后玩家 2 必须从 5 和 7 中进行选择。无论玩家 2 选择了哪个，玩家 1 都可以选择 233 。
     最终，玩家 1（234 分）比玩家 2（12 分）获得更多的分数，所以返回 True，表示玩家 1 可以成为赢家。
```
<!-- more -->

## 解题思路: 
这种博弈的题很有意思，因为有两个角色，而且每个角色都试图寻找自己的最优解，最开始我做成贪心了，妄想能过，不过这种局部最优想要得到全局最优还是太难了。后来改成了dfs，最后改成了dp。  
不过对于这种存在两个角色的情况，dfs的返回值应该是什么呢,因为我需要同时记录两个角色不同的得分。emm，你可以选择返回一个结构体，保存两个数，也可以直接返回两个数的差值(妙啊),想到这里，就可以开始dfs了。  
### dfs
其实isA这个可传可不传哈，因为可以根据长度来判断当前是A还是B，下面DP就是这么弄的。  
**要注意是A在操作和B在操作时的不同return**。
```cpp
class Solution {
public:
    int dfs(bool isA,int start,int end,vector<int>& nums,int gap){
        if(start>end) return gap;
        int choose1 = isA?nums[start]:nums[start]*(-1);
        int choose2 = isA?nums[end]:nums[end]*(-1);
        if(isA)
            return max(dfs(!isA,start+1,end,nums,gap+choose1),dfs(!isA,start,end-1,nums,gap+choose2));
        else 
            return min(dfs(!isA,start+1,end,nums,gap+choose1),dfs(!isA,start,end-1,nums,gap+choose2));
    }

    bool PredictTheWinner(vector<int>& nums) {
        return dfs(true,0,nums.size()-1,nums,0)>=0;
    }
};
```

### 动态规划
dp也就没什么好说的了，就是把dfs倒过来写一遍就行了。
```cpp
class Solution {
public:
    bool PredictTheWinner(vector<int>& nums) {
        //试一试dp
        int dp[22][22]; //dp[i][j]表示在开始为i，结束为j的数组中，选择后的对于选择的人来说的两者差的最优解
        memset(dp,0,sizeof(0));
        //如果原长度是偶数，那么偶数长度时一定是A在选
        //如果原长度是奇数，那么奇数长度时一定是A在选
        int len = nums.size();
        int isOdd = (len%2) == 1;
        for(int i=0;i<len;i++){
            dp[i][i] = isOdd?nums[i]:nums[i]*(-1);
        }
        for(int curlen=2;curlen<=len;curlen++){
            for(int i=0;i+curlen-1<len;i++){
                int j=i+curlen-1;
                int choose1 = nums[i];
                int choose2 = nums[j];
                if( isOdd == (curlen%2)){
                    dp[i][j] = max(choose1+dp[i+1][j],choose2+dp[i][j-1]);
                }else{
                    dp[i][j] = min(choose1*(-1)+dp[i+1][j],choose2*(-1)+dp[i][j-1]);
                }
            }
        }
        return dp[0][len-1]>=0;
    }
};
```

### 贪 心 的 大 失 败
无脑贪心不可取，这里想的是拿左右端点的值去和左+1右-1比，然后巴拉巴拉。。。这只是局部最优啊，不过居然还过了不少的样例。  
```cpp
class Solution {
public:
    
    bool PredictTheWinner(vector<int>& nums) {
        //我能贪出来吗？
        int ansA=0;
        int ansB=0;
        if(nums.size()==1) return true;
        while(nums.size() != 0){
            //A
            if(nums.size() == 1){
                ansA += nums[0];
                break;
            }else if(nums.size()<=3){
                if(nums[0] > nums[nums.size()-1]){
                    ansA += nums[0];
                    nums.erase(nums.begin());
                }else{
                    ansA += nums[nums.size()-1];
                    nums.pop_back();
                }
            }else{
                int gap1 = nums[1]-nums[0];
                int gap2 = nums[nums.size()-2]-nums[nums.size()-1];
                if(gap1 < gap2){
                    ansA += nums[0];
                    nums.erase(nums.begin());
                }else{
                    ansA += nums[nums.size()-1];
                    nums.pop_back();
                }
            }
            //B
            if(nums.size() == 1){
                ansB += nums[0];
                break;
            }else if(nums.size()<=3){
                if(nums[0] > nums[nums.size()-1]){
                    ansB += nums[0];
                    nums.erase(nums.begin());
                }else{
                    ansB += nums[nums.size()-1];
                    nums.pop_back();
                }
            }else{
                int gap1 = nums[1]-nums[0];
                int gap2 = nums[nums.size()-2]-nums[nums.size()-1];
                if(gap1 < gap2){
                    ansB += nums[0];
                    nums.erase(nums.begin());
                }else{
                    ansB += nums[nums.size()-1];
                    nums.pop_back();
                }
            }
        }
        return ansA>=ansB;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/predict-the-winner/