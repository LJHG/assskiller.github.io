---
title: 重新排列句子中的单词---LeetCode5413(在排序时长度相同的保持相对位置不变)
date: 2020-05-17 21:32:32
tags: [字符串数组]
---
### 题目描述：  
「句子」是一个用空格分隔单词的字符串。给你一个满足下述格式的句子 text :
句子的首字母大写
text 中的每个单词都用单个空格分隔。
请你重新排列 text 中的单词，使所有单词按其长度的升序排列。如果两个单词的长度相同，则保留其在原句子中的相对顺序。
请同样按上述格式返回新的句子。

### 示例：   
```cpp
示例 1：
输入：text = "Leetcode is cool"
输出："Is cool leetcode"
解释：句子中共有 3 个单词，长度为 8 的 "Leetcode" ，长度为 2 的 "is" 以及长度为 4 的 "cool" 。
输出需要按单词的长度升序排列，新句子中的第一个单词首字母需要大写。
```
<!-- more -->

### 解题思路:  
这次周赛就做出第一题，惨不忍睹，这是第二题，非常悲剧的超时了。  
这道题一看都会，不就是根据句子搞一个单词数组，然后排个序不就完了吗。是这样的，但是如果你直接对字符串向量进行排序，那么是不行的，因为它的排序算法会调换你的相对位置，相同长度的单词，可能排序后本来在前面的，就跑到后面去了。所以要自己写CMP，但是如果你直接对单词数组写cmp，例如**cmp(string a,string b)**，你又会发现只有单词信息，没有位置信息啊，所以这样也不行。  
后来我干脆就没排序了，每次从单词数组中找出最短的单词，然后把这个单词去掉。这样确实可行，然后超时了。  
明显这道题O(N²)是不行了，然后我就放弃了。    
下面展示正确解法（看的别人的）：建一个长度vector和一个下标vector，然后对下标vector进行排序，这样的话自己写cmp时，就既有长度信息，又有位置信息了(妙啊)。

```cpp
vector<int> lenv;
vector<int> indexv;
 bool cmp(int a,int b)
    {
        if(lenv[a] == lenv[b])
        {
            return a<b;
        }
        else
            return lenv[a]<lenv[b];
    }
class Solution {
public:

    vector<string> getAllStrings(string text)
    {
        vector<string> ans;
        string temp="";
        int length = text.length();
        for(int i=0;i<length;i++)
        {
            if(text[i]==' ' || i==length-1)
            {
                if(text[i] != ' ') temp+=text[i];
                if(temp[0] <= 90) temp[0]+=32;
                ans.push_back(temp);
                temp = "";
            }
            else
            {
                temp += text[i];
            }
        }
        return ans;
    }


    string arrangeWords(string text) {
        lenv.clear();
        indexv.clear();
        vector<string> strings = getAllStrings(text);
        int length = strings.size();
        for(int i=0;i<length;i++)
        {
            lenv.push_back(strings[i].length());
            indexv.push_back(i);
        }
        sort(indexv.begin(),indexv.end(),cmp);
        string ans = "";
        for(int i=0;i<length;i++)
        {
            ans += strings[indexv[i]];
            if(i != length-1) ans+=" ";
        }

        ans[0] -=32;
        return ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/rearrange-words-in-a-sentence/