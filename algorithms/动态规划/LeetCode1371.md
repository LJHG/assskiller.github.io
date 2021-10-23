---
title: 每个元音包含偶数次的最长子字符串---LeetCode1371(前缀和+哈希优化+状态压缩)
date: 2020-05-20 17:20:29
tags: [状压, 前缀和]
---
## 题目描述：  
给你一个字符串 s ，请你返回满足以下条件的最长子字符串的长度：每个元音字母，即 'a'，'e'，'i'，'o'，'u' ，在子字符串中都恰好出现了偶数次。

## 示例：   
```cpp
示例 1：
输入：s = "eleetminicoworoep"
输出：13
解释：最长子字符串是 "leetminicowor" ，它包含 e，i，o 各 2 个，以及 0 个 a，u 。

示例 2：
输入：s = "leetcodeisgreat"
输出：5
解释：最长子字符串是 "leetc" ，其中包含 2 个 e 。

示例 3：
输入：s = "bcbcbc"
输出：6
解释：这个示例中，字符串 "bcbcbc" 本身就是最长的，因为所有的元音 a，e，i，o，u 都出现了 0 次。

提示：
1 <= s.length <= 5 x 10^5
s 只包含小写英文字母。
```
<!-- more -->
## 解题思路:  
### 状压dp
这道题一看就是状态压缩，于是我首先就写了一发状压dp，但是因为s太长了，这里开的dp是二维的，最后就爆内存了。  
其实这种状态压缩的写法并不好，写的时候就感觉很奇怪，之所以奇怪是因为这道题本质上是前缀和，可以用一维的来写，我偏偏写成了二维，最后写出来反正也爆内存了，不过至少这种方法是对的。
```cpp
const int MAXN= 10000;
class Solution {
public:
    int findTheLongestSubstring(string s) {
        //状压dp？
        int dp[MAXN][MAXN]; //居然可以开这么大 dp[i][j]代表的是从index i到j五个元音的出现情况
        memset(dp,0,sizeof(dp));
        int ans = 0;
        //初始化dp
        int length = s.length();
        for(int i=0;i<length;i++)
        {
            if(s[i] == 'a') dp[i][i] ^= 1;
            if(s[i] == 'e') dp[i][i] ^= 2;
            if(s[i] == 'i') dp[i][i] ^= 4;
            if(s[i] == 'o') dp[i][i] ^= 8;
            if(s[i] == 'u') dp[i][i] ^= 16;
            if(dp[i][i] == 0) ans = 1;
        }
        for(int k=2;k<=length;k++)
        {
            for(int i=k-1;i<length;i++)
            {
                int j=i-k+1;
                dp[j][i] = dp[j][j] ^ dp[j+1][i];
                if(dp[j][i] == 0)
                {
                    ans = k;
                }
            }
        }
        return ans;
    }
};
```

</br>

### 前缀和
发现这道题实际上是前缀和后，我立马写了一发前缀和，然后又超时了。
```cpp
const int MAXN= 500050;
class Solution {
public:
    int findTheLongestSubstring(string s) {
       //前缀和
        int prefix[MAXN];
        memset(prefix,0,sizeof(prefix));
        int ans =0;
        if(s[0] == 'a' ) prefix[0] ^= 1;
        if(s[0] == 'e' ) prefix[0] ^= 2;
        if(s[0] == 'i' ) prefix[0] ^= 4;
        if(s[0] == 'o' ) prefix[0] ^= 8;
        if(s[0] == 'u' ) prefix[0] ^= 16;
        
       int len = s.length();
       for(int i=1;i<len;i++)
       {
            if(s[i] == 'a' ) prefix[i] = prefix[i-1]^ 1;
            else if(s[i] == 'e' ) prefix[i] = prefix[i-1]^ 2;
            else if(s[i] == 'i' ) prefix[i] = prefix[i-1]^ 4;
            else if(s[i] == 'o' ) prefix[i] = prefix[i-1]^ 8;
            else if(s[i] == 'u' ) prefix[i] = prefix[i-1]^ 16;
            else prefix[i] = prefix[i-1];
       }

    //for(int i=0;i<len;i++) cout<<prefix[i]<<endl;
       for(int k=1;k<=len;k++)
       {
           for(int i=0;i+k-1<len;i++)
           {
                if(i-1 < 0)
                {
                    if( prefix[i+k-1] == 0 ) 
                    {
                        ans = k;
                    }
                }   
                else
                {
                    if( (prefix[i+k-1] ^ prefix[i-1]) == 0 )
                    {
                        ans = k;
                    } 
                }                 
           }
       }
       return ans;
    }
};
```
</br>

### 前缀和+哈希优化
当我发现前缀和超时了，我就猜到这道题多半要用到哈希优化了(难道是前缀和基本操作吗)。  
当前缀和加上哈希优化，最显著的变化就是不需要再开前缀和数组了，直接拿一个值一直累加(累亦或)下去就行了，以前还碰到一道[前缀和+哈希的题](https://www.assskiller.cn/2020/05/15/LeetCode560/)，可以看一下。  
可以把式子稍微推一下，目标是找到prefrx[i] ^ prefix[j-1] = 0，变换一下可以变成prefix[i] = prefix[j-1]。这样一变就很明显了，把前缀和一直类推下去，然后把出现过的值的最小坐标记录一下，再次碰到时，将两个Index减一下就行了。  
需要注意的是需要把records[0]设置为-1，同时还要标记当前的值是否出现过，那就只好把没出现过的值设置为-2了。(我感觉这种做法比较weird,但是至少是对的)。
```cpp
const int MAXN= 500050;
class Solution {
public:
    int findTheLongestSubstring(string s) {
        //前缀和 + 哈希优化
        int records[100]; //用来记录已经出现的值的位置 records[x]=i;表示前缀和为x的index为i
        for(int i=0;i<100;i++) records[i] = -2; //-2表示没有访问过
        int length =s.length();
        int cur=0;
        int ans=0;
        records[0] = -1;
        for(int i=0;i<length;i++)
        {
            if(s[i] == 'a') cur = cur^1;
            if(s[i] == 'e') cur = cur^2;
            if(s[i] == 'i') cur = cur^4;
            if(s[i] == 'o') cur = cur^8;
            if(s[i] == 'u') cur = cur^16;
            if(records[cur] != -2)
            {
                ans =max(ans,i-records[cur]);
                records[cur] = min(records[cur],i);
            } 
            else
            {
                records[cur] = i;
            }
          
        }
        return ans;
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/find-the-longest-substring-containing-vowels-in-even-counts/