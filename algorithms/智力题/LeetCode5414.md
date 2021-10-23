---
title: 收藏清单---LeetCode5414(能线性扫就别搞两重循环了)
date: 2020-05-17 22:06:54
tags: []
---
### 题目描述：  
给你一个数组 favoriteCompanies ，其中 favoriteCompanies[i] 是第 i 名用户收藏的公司清单（下标从 0 开始）。
请找出不是其他任何人收藏的公司清单的子集的收藏清单，并返回该清单下标。下标需要按升序排列。

### 示例：   
```cpp
输入：favoriteCompanies = [["leetcode","google","facebook"],["leetcode","amazon"],["facebook","google"]]
输出：[0,1] 
解释：favoriteCompanies[2]=["facebook","google"] 是 favoriteCompanies[0]=["leetcode","google","facebook"] 的子集，因此，答案为 [0,1] 。
```
<!-- more -->
### 解题思路:  
本次周赛脑子短路+2，明明可以一次线性扫描就完事的，我偏要写成双重循环。这种blog写起来就很尴尬，不知道该加什么tag，但是不写又感觉不舒服。
这道题我的大体思路是对的，就是先对于每一个vector集合排序，这样可以使得判断一个集合是否为另外一个集合的子集时更加容易，直接从左到右遍历就行了。我的问题就是出在从左到右遍历时，我居然对于从哪一个位置开始还写了一层循环(不知道自己在干嘛)，其实完全没必要的。  
这次还踩了一个auto的坑，使用for(auto xxx:xxxx)时，是只读的。如果要对于xxx里的值进行改变(比如排序)，那么应该写为for(auto& xxx:xxxx)。

```cpp
class Solution {
public:
    
    bool BincludeA(vector<string>& a,vector<string>& b)
    {
        int aLen = a.size();
        int bLen = b.size();
        // for(int i=0;i<bLen;i++)
        // {
        //     int aIndex = 0;
        //     for(int j=i;j<bLen;j++)
        //     {
        //         if(b[j] == a[aIndex])
        //         {
        //             aIndex++;
        //             if(aIndex == aLen) return true;
        //         }
        //     }
            
        // }
        //可以直接线性扫的呀。。。。
        int cura=0;
        for(int i=0;i<bLen;i++)
        {
            if(b[i] == a[cura])
            {
                cura++;
                if(cura == aLen) return true;
            }
        }
        return false;
    }

    static bool cmp(string a,string b) {
        return a<b;
    }
    
    vector<int> peopleIndexes(vector<vector<string>>& favoriteCompanies) {
        //暴力，奥里给，干了
        //for(auto xxx:favoriteCompanies) sort(xxx.begin(),xxx.end(),cmp); //用auto要加引用才能改值，这里没加，就相当于只读了，等于没排上。
        int length = favoriteCompanies.size();
        for(int i=0;i<length;i++)
        {
           sort(favoriteCompanies[i].begin(),favoriteCompanies[i].end(),cmp);
        }
        vector<int> ans;
        for(int i=0;i<length;i++)
        {
            int flag=1;
            for(int j=0;j<length;j++)
            {
                if(i==j) continue;
                if(BincludeA(favoriteCompanies[i],favoriteCompanies[j]))
                {
                    flag = 0;
                }
            }
            if(flag)
                ans.push_back(i);
        }  
        return ans;
    }
};
```

### 题目链接：  
https://leetcode-cn.com/problems/people-whose-list-of-favorite-companies-is-not-a-subset-of-another-list/