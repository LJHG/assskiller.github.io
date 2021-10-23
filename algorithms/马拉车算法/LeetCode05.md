---
title: LeetCode05
date: 2020-04-23 21:10:40
tags: [回文串, dp, 马拉车算法]
---
### 题目描述：  
给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。

### 示例：   
```cpp
示例 1：
输入: "babad"
输出: "bab"
注意: "aba" 也是一个有效答案。

示例 2：
输入: "cbbd"
输出: "bb"
```

### 解题思路:  
这里给三个解题思路，分别是中心展开，dp，和马拉车  

### 中心展开
暴力对每一个位置进行展开看回文，为了避免偶回文，对字符串做了预处理

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
       //对s进行处理，避免偶回文的情况出现
       string newS = "#";
       for(int i=0;i<s.length();i++)
       {
           newS += s[i];
           newS += '#';
       }
       s = newS;
       int length = s.length();
       string ans="";
       int maxLength = 0;
       for(int i=0;i<length;i++)
       {
           string pre="";
           char middle = s[i];
           string back = "";
           for(int j=1; i+j<length && i-j>=0; j++)
           {
               if(s[i-j] == s[i+j])
               {
                   pre += s[i-j];
                   back += s[i+j];
               }           
               else
               {
                   break;
               }
           }

            //pre需要reverse一下
            std::reverse(pre.begin(),pre.end());
            string tmpAns = pre + middle + back;
            int tmpLength = tmpAns.length();
            if(tmpLength > maxLength)
            {
                ans = tmpAns;
                maxLength = tmpLength;
            }
            
       }
       //把输出结果中的#去掉
       string realAns = "";
       for(int i=0;i<ans.length();i++)
       {
           if(ans[i]=='#')
           {
               continue;
           }
           else{
               realAns += ans[i];
           }
       }
       return realAns;
    }
};
```
<br/>
<br/>
<br/> 

### dp
先初始化所有一回文和二回文的情况，然后再通过动态规划求出所有三回文直到length回文的情况  
递推公式 dp[i][j] = dp[i+1][j-1] ==1 && s[i]==s[j]  
注意两层循环，表示回文串长度的循环要放外面，不然就不对，因为这样可能在index为0时，会错过长度为4的回文，因为后面还没弄过。

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        //dp法
        int start =0;
        int end =0;
        int dp[1000][1000]; //dp[i][j]==1代表在s中(i,j)位置的是一个回文字串
        memset(dp,0,sizeof(dp));
        //初始化所有一回文和二回文的情况
        int length = s.length();
        for(int i=0;i<length;i++)
        {
            dp[i][i] =1;
            if(end-start <= 0)
            {
                start =i;
                end =i;
            }
            if(i+1 <length && s[i] == s[i+1])
            {
                dp[i][i+1] =1;
                start =i;
                end = i+1;
            }
        }

        //从3回文开始，一直找到length回文
        for(int l=2; l<length ;l++)
        {
            for(int i=0;i+l<length;i++)
            {
                int j = i+l;
                dp[i][j] = dp[i+1][j-1] && s[i]==s[j];
                if(dp[i][j] ==1)
                {
                    start=i;
                    end=j;
                    
                }
            }
        }

        //根据start end 求结果 注意 substr第一个参数是位置，第二个参数是长度
        return s.substr(start,end-start+1);    
    }
};

```
<br/>
<br/>
<br/> 

### 马拉车算法
在这里贴一个讲马拉车讲的很好的B站视频：  
https://www.bilibili.com/video/BV1ft4y117a4  

马拉车算法和中心展开其实很像，只不过很好地利用了回文串的对称性来避免重复计算  
对字符串预处理是为了让全部都变成奇回文串的情况  
马拉车算法维护了一个最右回文子串，当对一个字符串从左到右进行遍历求d[i]时，如果i在最右回文子串中，就可以利用对称性来为d[i]初始化一个值，然后再中心展开，不然就直接中心展开。  
最后得出结果时，可以发现，最终的回文串长度就是d[i]-1，最终的最长回文串在原始字符串中的起始index，就是修改后字符串中，(d[i]最大的index - d[i])/2  

```cpp
class Solution {
public:
    struct tarStringInfo{
        int index; //最长回文子串的开始位置
        int length; //最长回文子串的长度 
    };

    string preMake(string s)
    {
        //先对s做预处理
        string newS="@#";
        for(int i=0;i<s.length();i++)
        {
            newS += s[i];
            newS += '#';	
        }
        newS += "$";
        return newS;
    }

    tarStringInfo Manacher(string s)
    {
        s = preMake(s);
        int right = 0; //最右回文子串的右边界 
        int middle = 0; // 最右回文子串的中心
        int maxDis =0;  //记录最大di 
        int maxIndex=0; //最大di的index 
        vector<int> d; //d数组
        int length = s.length();
        d.push_back(0); //@对应位置的回文半径是0 
        d.push_back(1); //第一个字符对应的回文半径必定是1
        right =1;
        middle =1; 
        for(int i=2;i<length;i++)
        {
            d.push_back(1); //不管怎样，先push一个1 
            if(i<=right) //在最右回文子串内，利用对称初始化一个值 
            {
                d[i] = min(d[2*middle-i],right-i+1);
            }
            //暴力扩张
            int l = d[i];
            while(s[i+l] == s[i-l] && i-l>=1 && i+l < length-1 )
            {
                if(s[i+l] == s[i-l])
                {
                    d[i]++;
                }
                l++;
            }
            if(d[i] > maxDis)
            {
                maxDis = d[i];
                maxIndex=i;
            }
            right = i + d[i] -1;
            middle =i;
        }
        
        //对应回原字符串，回文长度就是d[i]-1，回文开始的位置就是 (index-d[i])/2 
        tarStringInfo ans;
        ans.length = maxDis -1;
        ans.index = (maxIndex - maxDis)/2;
        return ans;	 
    }

    string longestPalindrome(string s) {
        tarStringInfo ans = Manacher(s);
        return s.substr(ans.index,ans.length);    
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/longest-palindromic-substring/