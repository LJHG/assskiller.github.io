---
title: 秋季编程大赛记录
date: 2020-09-12 19:06:54
tags: 
---
感觉自己太菜了，就会签到。  
<!-- more -->
### 第一题
签到题。   
### 第二题  
第二题真的，我就是优化的方向错了。   
本来就是一个On²的嘛，然后呢，排序后早一点break我以为能过，不行。  
然后我就想到的上次用的那个map来存，我以为是重复数字太多了，然后试了一下，不行。  
然后换成两个map,不行。  
然后心态崩了，不知道该怎么优化。   
后来看了一下题解，怎么说呢，就是先对两个数组排序，然后一个正向遍历，一个反向遍历，这样两个数组都只走一遍就行了。（不得不说，看起来很简单，但是我真的没想到，也从来没有这么写过，真的学到了）。  
```cpp
class Solution {
public:
    int MOD = 1e9+7;
    int breakfastNumber(vector<int>& staple, vector<int>& drinks, int x) {
        int ans = 0;
        sort(staple.begin(),staple.end());
        sort(drinks.begin(),drinks.end());
        int pt = drinks.size()-1;
        for(int a:staple){
            while( pt>=0 && a + drinks[pt] > x ){
                pt--;
            }
            ans += pt+1;
            ans %= MOD;
        }
        return ans%MOD;
    }
};
```

### 第三题  
第三题我真的想了好久。最后大体思路对了，但还是差一点，可惜了。  
心路历程如下：这道题是个啥，好难->果然还是要dp->长度1e5开不了二维dp->果然还是要贪心->不会贪->咦，可以开一维dp->思考了好久怎么一维dp->居然用上了前缀和和后缀和->走上了不归路
说一下这道题的解法吧，就是可以这么想：  
ryr[i]表示从0到index i变成红黄红的最小次数。  
ry[i]表示i从0到index i变成红黄的最小次数。
r[i]表示从i到index i变成红的最最小次数
ryr(红黄红)是由ry或者ryr转移过来的(其实这个我写的时候并不是很确定，只能说是大胆猜想吧，稍微想一想好像还是没毛病)，然后就可以开始dp了。
同理ry是由ry或者r转移过来的(我当时就是没想到这一点，然后转而去直接计算ry，就是通过前缀和和后缀和来统计一个字符串前面的y数量和后部分的r数量，呃呃呃呃，复杂度直接就On²了，直接导致了超时)  

贴一发raw代码，这个思路大概是对了，但是超时了。  
```cpp
class Solution {
public:
    int INF = 9999999;
    int minimumOperations(string leaves) {
        //单侧dp即可
        int ry[100010];
        int ryr[100010];
        int prey[100010];
        int sufr[100010];
        memset(prey,0,sizeof(prey));
        memset(sufr,0,sizeof(sufr));
        
        
        //ry感觉不是推出来的，是算出来的
        int len = leaves.size();
        prey[0] = (leaves[0] == 'y');
        for(int i=1;i<len;i++){
            prey[i] = (leaves[i] == 'y') + prey[i-1];
        }
        sufr[len-1] = (leaves[len-1] == 'r');
        for(int i=len-2;i>=0;i--){
            sufr[i] = (leaves[i] == 'r') + sufr[i+1];
        }
        for(int i=0;i<len;i++){
            ry[i] = INF;
            ryr[i] = INF;
        }
        for(int i=1;i<len;i++){
            if(leaves[i] == 'y' && i>=2){
                ry[i] = ry[i-1];
            }
            else{
                for(int k=0;k<i;k++){
                ry[i] = min(ry[i],prey[k]+sufr[k+1]-sufr[i+1]);
                }
            }
            
        }
        for(int i=2;i<len;i++){
            if(leaves[i] == 'r'){
                ryr[i] = min(ryr[i-1],ry[i-1]);
            }else{
                ryr[i] = min(ry[i-1]+1,ryr[i-1]+1);
            }
        }
        return ryr[len-1];
        
    }
};
```

修改后的解法
```cpp
class Solution {
public:
    int INF = 9999999;
    int minimumOperations(string leaves) {
        //单侧dp即可
        int r[100010];
        int ry[100010];
        int ryr[100010];
        int len = leaves.size();
        for(int i=0;i<len;i++){
            r[i] = INF;
            ry[i] = INF;
            ryr[i] = INF;
        }
        r[0] = leaves[0]=='y';
        for(int i=1;i<len;i++){
            r[i] = r[i-1]+ (leaves[i] == 'y');
        }
        for(int i=1;i<len;i++){
            if(leaves[i] == 'y'){
                ry[i] = min(ry[i-1],r[i-1]);
            }else{
                ry[i] = min(ry[i-1]+1,r[i-1]+1);
            }
        }
        for(int i=2;i<len;i++){
            if(leaves[i] == 'r'){
                ryr[i] = min(ryr[i-1],ry[i-1]);
            }else{
                ryr[i] = min(ryr[i-1]+1,ry[i-1]+1);
            }
        }
        return ryr[len-1];
    }
};
```

### 总结
这次止步于第三题，总结一下就是，dp开始变得生疏了，做完后感觉好像也没那么难想，以及，如果优化方向错了(第二题)，再怎么也无济于事。  

### 链接
[题目链接](https://leetcode-cn.com/contest/season/2020-fall/?utm_campaign=contest_2020_fall&utm_medium=leetcode_contest_2020_fall_contest_banner&utm_source=contest&gio_link_id=QReO3Y3o)