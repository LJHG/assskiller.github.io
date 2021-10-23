---
title: 对角线遍历---内存开到爆怎么办？用vector吧
date: 2020-04-26 14:13:27
tags: [周赛186, 栈溢出, 数组越界]
---
### 题目描述：  
给你一个列表 nums ，里面每一个元素都是一个整数列表。请你依照下面各图的规则，按顺序返回 nums 中对角线上的整数。

### 示例： 
```cpp
输入：nums = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,4,2,7,5,3,8,6,9]
输入：nums = [[1,2,3],[4],[5,6,7],[8],[9,10,11]]
输出：[1,4,2,5,3,8,6,9,7,10,11]
```

### 解题思路:  
思路就是正常遍历，然后把值加入到对应的对角线数组(vector)里面去  
思路对是对了，但是最开始我是直接开的二维数组，然后数据最大是1e5，开二维爆的很彻底，于是稍微缩小一点，结果就越界了，然后就GG了。  
先展示错误示范：  

我这里ans开的二维数组，大小怎么改都改不好。
```cpp
class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& nums) {
        //又是栈溢出，= =我人晕了
        int ans[99999][200]; //ans[i][j]表示 第i层对角线的第n个元素
        int maxIndex[10000]; //表示第i条对角线装的最大元素
        memset(ans,0,sizeof(ans));
        memset(maxIndex,-1,sizeof(maxIndex));
        int endMax =0 ;
        int outerLength = nums.size();
        for(int i=0;i<outerLength;i++)
        {
            int length = nums[i].size();
            
            for(int j=0;j<length;j++)
            {
                maxIndex[i+1+j]++;
                
                ans[i+1+j][maxIndex[i+1+j]] = nums[i][j];
                if(i+1+j > endMax)
                    endMax = i+1+j;
            }
        }
        vector<int> ansV;
        cout<<endMax<<endl;
        for(int i=1;i<=endMax;i++)
        {
            int eeaaa=maxIndex[i];
            for(int j= eeaaa;j>=0;j--)
            {
                ansV.push_back(ans[i][j]);
            }
        }
        return ansV;
    }
};
```

<br/>
<br/>

再来看正确示范:  
既然直接开二维数组会爆，那就开vector数组吧  
可以看到，我只是把ans给改成了vector数组，其它什么都没干，就过了，vector yyds。  
其实这里的maxIndex都可以不要了，因为vector自带长度信息，懒得删了。
```cpp
const int maxN = 1e5 + 50;
class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& nums) {
        vector<int> ans[maxN*2];
        int maxIndex[maxN]; //表示第i条对角线装的最大元素
        for(int i=0;i<maxN*2;i++) ans[i].clear(); 
        memset(maxIndex,-1,sizeof(maxIndex));
        int endMax =0 ;
        int outerLength = nums.size();
        for(int i=0;i<outerLength;i++)
        {
            int length = nums[i].size();
            
            for(int j=0;j<length;j++)
            {
                maxIndex[i+1+j]++;
                
                ans[i+1+j].push_back(nums[i][j]);
                if(i+1+j > endMax)
                    endMax = i+1+j;
            }
        }
        vector<int> ansV;
        for(int i=1;i<=endMax;i++)
        {
            int eeaaa=maxIndex[i];
            for(int j= eeaaa;j>=0;j--)
            {
                ansV.push_back(ans[i][j]);
            }
        }
        return ansV;
    }
};
```


### 题目链接：  
https://leetcode-cn.com/problems/diagonal-traverse-ii/