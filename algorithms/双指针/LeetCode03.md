---
title: 无重复最长子串---LeetCode03
date: 2020-05-02 20:59:01
tags: [滑动窗口, 双指针]
---
### 题目描述：  
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

### 示例：   
```cpp
示例 1:
    输入: "abcabcbb"
    输出: 3 
    解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

示例 2:
    输入: "bbbbb"
    输出: 1
    解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

示例 3:
    输入: "pwwkew"
    输出: 3
    解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
         请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

```

<!--more-->

### 解题思路:  
这道题的解法很多，我在这里总结了四种解法，分别是暴力解法1，暴力解法2，滑动窗口解法，滑动窗口的优化解法  

### 暴力解法1
暴力解法1是我最先想到的解法,方法是从头到尾进行一次遍历，对于每一个字符，往后查找直到有重复字符，使用的方法是用一个数组来记录（用map也行，这道题很多地方都可以用map，不过用数组比较方便，我就都是用的数组）。每次选择一个字符时，都要对数组进行初始化。  
缺点就是每次初始化比较耗时，同时时间复杂度是O(n²)。

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int map[1000];
        int max =0;
        int ans = 0;
        memset(map,0,sizeof(map));
        int length = s.length();
        for(int i=0;i<length;i++)
        {
            max = 0;
            memset(map,0,sizeof(map));
            for(int j=i;j<length;j++)
            {
                if(map[s[j]] >0)
                {
                    break;
                }
                max++;
                map[s[j]]++;
            }
            if(max > ans)
                ans = max ;
        }
        return  ans;   
    }
};
```

<br/>

### 暴力解法2
暴力解法2是对长度进行遍历，相当于是给定一个固定长度的窗口，然后向后移动，不过虽然在改变数组时修改值是只改变了前后两个值，但是再查找是否有重复时还是采用的遍历，感觉比第一个解法还暴力，最后果不其然的超时了，这是虚假的滑动窗口。  
```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int length = s.length();
        int flag[1000];
        int ans = length;
        while(ans > 1)
        {
            memset(flag,0,sizeof(flag));
            int right = 1;
            for(int i=0;i<ans;i++)
            {
                flag[s[i]]++;
                if(flag[s[i]] > 1)
                    right=0;
            }
            if(right == 1)
                return ans;
            for(int i=1;i+ans<=length;i++)
            {
                right = 1;
                flag[s[i-1]]--;
                flag[s[i+ans-1]]++;
                for(int j=i;j<i+ans;j++)
                {
                    if(flag[s[j]] > 1)
                    {
                        right=0;
                        break;
                    }                 
                }
                if(right == 1)
                {
                	return ans;
				}
            }
            ans--;
        }
        return ans;
    }
};
```

<br/>

### 滑动窗口
滑动窗口也可以叫双指针法，大体的思想是：如果当前子串没有重复，那么就把右指针往右移动一个单位；如果当前子串有重复，那么就把左指针往右移动一个单位。这里采用的方法是，每次移动左指针或者右指针后，都遍历判断一下当前是否有重复。实际上也是虚假的滑动窗口。  
```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int left =0;
        int right = 0;
        int length = s.length();
        bool isLongest = 1;
        int max = 1;
        int flag[200];
        if(length == 0)
            return 0;
        while( !( (right == (length-1))  && isLongest))
        {
            if(isLongest)
            {
                if(right-left+1 > max)
                    max = right-left+1;
                right = (right+1 == length)?right:right+1;
            }
            else
            {
                left++;
            }
            memset(flag,0,sizeof(flag));
            isLongest = 1;
            for(int i=left;i<=right;i++)
            {
                flag[s[i]]++;
                if(flag[s[i]] > 1)
                {
                    isLongest = 0;
                    break;
                }
            }
        }
        return (right-left+1)>max?(right-left+1):max;
    }
};
```


<br/>

### 滑动窗口的优化
既然使用了滑动窗口，那么实际上每次的遍历找是否重复是没有必要的，因为如果有重复，那么必然来自于最近一次右边的移动，而且肯定只会重复一次。根据这一特性，可以把重复的字符给保存下来，如果左边往右移动时将这一个字符给去掉了，那么当前就又是一个无重复子串。  
```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        //初始化
        int left =0;
        int right = 0;
        int length = s.length();
        bool isLongest = 1;
        int max = 1;
        int flag[200];
        memset(flag,0,sizeof(flag));
        flag[s[0]]++;
        int curDoubleLetter=-1;
        if(length == 0)
            return 0;
        while( !( (right == (length-1))  && isLongest))
        {
            if(isLongest)
            {
                if(right-left+1 > max)
                    max = right-left+1;
                if(right +1 == length)
                {
                    //nothing
                }
                else
                {
                    right = right +1;
                    flag[s[right]]++;
                    if(flag[s[right]] >1)
                    {
                        isLongest = 0;
                        curDoubleLetter = s[right];
                    }
                }

            }
            else
            {
                left++;
                //cout<<left-1<<endl;
                flag[s[left-1]]--;
                if(curDoubleLetter!=-1 && flag[curDoubleLetter] == 1)
                {
                    isLongest = 1;
                }
                else
                {
                    isLongest = 0;
                }
            }
           
        }
        return (right-left+1)>max?(right-left+1):max;
    }
};
```


### 题目链接：  
https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/