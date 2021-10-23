---
title: 往字符串前面添字符形成的最短回文串---LeetCode214
date: 2020-08-29 14:17:57
tags: [回文,马拉车]
---
## 题目描述：  
给定一个字符串 s，你可以通过在字符串前面添加字符将其转换为回文串。找到并返回可以用这种方式转换的最短回文串。

## 示例：   
```cpp
示例 1:
输入: "aacecaaa"
输出: "aaacecaaa"

示例 2:
输入: "abcd"
输出: "dcbabcd"
```
<!-- more -->

## 解题思路:  
这道题官方的解题思路是KMP，但是我忘了，所以我用的回文串来做，最开始用的中心展开，然后超时了，后来改为了马拉车就过了。 
这两种方法都说一下吧
### 中心展开
中心展开的思想很简单，要让添加的字符最少，那么就是要在每一个位置中心展开，使之能够展开到开始位置并且长度最长，中心位置的选取只需要从(len-1)/2的位置往左取就行了。
```cpp
class Solution {
public:
    string getRidOfStar(string s){
        string newS;
        int len = s.size();
        for(int i=0;i<len;i++){
            if(s[i] != '*') newS+=s[i];
        }
        return newS;
    }
    string shortestPalindrome(string s) {
        if(s.size() == 0) return s;
        //思路 枚举中心位置在前面补字符串使得左右相等
        //有可能中心位置不在s上，所以构建新字符串
        string newS = "*";
        int len = s.size();
        for(int i=0;i<len;i++){
            newS += s[i];
            newS += "*";
        }
        s = newS;
        len = s.size();
        int middle = (len-1)/2;
        while(1){
            if(middle == 0 ){
                string rightStr = s.substr(middle+1);
                reverse(rightStr.begin(),rightStr.end());
                return getRidOfStar(rightStr+s);
            }else{
                int flag = 0;
                for(int i=1;middle-i>=0;i++){
                    if(s[middle-i]!=s[middle+i])
                    {
                        flag =1;
                        break;
                    }
                }
                if(flag){
                    middle--;
                }else{
                    string rightStr = s.substr(middle+middle,len-1-2*middle);
                    reverse(rightStr.begin(),rightStr.end());
                    return getRidOfStar(rightStr+s);
                }
                
            }
        }
        
        return "";
    }
};
```

### 🐎拉🚗
根据上面的分析可以看出，我们要求的东西就是一个从S[0]位置开始的最长回文串，那就可以直接马拉车了，需要稍微修改一下代码，就是在每一个i中心展开时，判断开始位置，并取所有开始位置为0的length的最大值就是从S[0]开始的回文串的最大长度
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
        tarStringInfo ans;
        ans.length = 0;
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
            if((i-d[i])/2 == 0 && d[i]-1 >ans.length ){
                ans.length = d[i]-1;
                ans.index = 0;
            }
        }
        
        //对应回原字符串，回文长度就是d[i]-1，回文开始的位置就是 (index-d[i])/2 
        return ans;	 
    }
    string shortestPalindrome(string s) {
        int leftPartLen = Manacher(s).length;
        string rightStr = s.substr(leftPartLen,s.size()-leftPartLen);
        reverse(rightStr.begin(),rightStr.end());
        return rightStr+s;
    }
};
```
## 题目链接：  
https://leetcode-cn.com/problems/shortest-palindrome/
[一个总结的很好的题解](https://leetcode-cn.com/problems/shortest-palindrome/solution/xiang-xi-tong-su-de-si-lu-fen-xi-duo-jie-fa-by--44/)