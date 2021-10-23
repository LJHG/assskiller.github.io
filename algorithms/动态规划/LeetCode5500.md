---
title: 乘积为正数的最长子数组长度---LeetCode5500
date: 2020-08-30 14:21:15
tags: [前缀和]
---
## 题目描述：  
给你一个整数数组 nums ，请你求出乘积为正数的最长子数组的长度。
一个数组的子数组是由原数组中零个或者更多个连续数字组成的数组。
请你返回乘积为正数的最长子数组长度。


## 示例：   
```cpp
示例  1：
输入：nums = [1,-2,-3,4]
输出：4
解释：数组本身乘积就是正数，值为 24 。

示例 2：
输入：nums = [0,1,-2,-3,-4]
输出：3
解释：最长乘积为正数的子数组为 [1,-2,-3] ，乘积为 6 。
注意，我们不能把 0 也包括到子数组中，因为这样乘积为 0 ，不是正数。

示例 3：
输入：nums = [-1,-2,-3,0,1]
输出：2
解释：乘积为正数的最长子数组是 [-1,-2] 或者 [-2,-3] 。

```
<!-- more -->
## 解题思路:  
第204次周赛翻车现场。  
这次在图书馆抗压做题，一个半小时的的题我妄想在一个小时搞定，最后就A了一题，艹。  
第一题居然就是模拟，还是那种一看不难，一写就烦的题，然后第一题我就写了快半个小时。  

然后现在在写的就是第二题了。  
这道题最开始一看想dp，然后又一看，数据量1e5，开不了二维数组啊，于是就想到了前缀和。  
准确的说应该叫前缀积，因为只需要正负，所以我就把正数负数转为了1和-1，其实这道题也可以用前缀和而不是前缀积来做，只要统计正负数的数量即可。  
这道题有一个需要注意的地方就是0，有0存在后，不管怎么乘都是0，所以为了避开这个问题，我们可以让数组中不含零，方法就是按照0来分段。 
最开始我写的代码如下：
这个方法超时了，因为我在遍历前缀积数组时用了双重循环。
```cpp
class Solution {
public:
    
    int getMaxLenWithOut0(vector<int>& nums){
         int ans = 0;
        int prefix[100010];
        int len = nums.size();
        if(nums[0] > 0) prefix[0] =1;
        else if(nums[0] <0) prefix[0] = -1;
        else prefix[0] = 0;
        
        for(int i=1;i<len;i++){
            int ans = nums[i]*prefix[i-1];
            if(ans >0){
                prefix[i] =1;
            }else if(ans<0) prefix[i] = -1;
            else prefix[i] = 0;
        }
        // for(int i=0;i<len;i++)
        //     cout<<prefix[i]<<" ";
        // cout<<endl;
        
        for(int i=0;i<len;i++){
            if(nums[i] >0) ans = max(ans,1);
            for(int j=i+1;j<len;j++){
                if(prefix[j] == 1){
                    ans = max(ans,j+1);
                    continue;
                } 

                if(prefix[j]==prefix[i]) { //只能是都是-1的情况了
                    ans = max(ans,j-i);
                   // cout<<i<<" "<<j<<endl;
                }
            }
        }
        return ans;
    }
    
    
    int getMaxLen(vector<int>& nums) {
       int len = nums.size();
        vector<int> newNums;
        newNums.clear();
        int ans = 0;
        for(int i=0;i<len;i++){
            if(nums[i] == 0){
                if(newNums.size()>0)
                {
                    ans = max(ans,getMaxLenWithOut0(newNums));
                newNums.clear();
                }
                
            }else
            {
                newNums.push_back(nums[i]);
            }
        }
        //cout<<newNums.size()<<endl;
        if(newNums.size()>0) ans = max(ans,getMaxLenWithOut0(newNums));
        return ans;
        
    }
};
```

双重循环可以，但没必要。  
稍微一想就能想到，要求乘积最大长度，只有两个情况。
1. 最后乘起来为正数，那么直接找到最靠后的前缀积为1的位置即可。
2. 最后乘起来为负数，那么直接找到最右边的前缀积为-1和最前面前缀积为-1的位置即可。 
```cpp
class Solution {
public:
    
    int getMaxLenWithOut0(vector<int>& nums){
         int ans = 0;
        int prefix[100020];
        int len = nums.size();
        if(nums[0] > 0) prefix[0] =1;
        else if(nums[0] <0) prefix[0] = -1;
        else prefix[0] = 0;
        
        for(int i=1;i<len;i++){
            int ans = nums[i]*prefix[i-1];
            if(ans >0){
                prefix[i] =1;
            }else if(ans<0) prefix[i] = -1;
            else prefix[i] = 0;
        }
        // for(int i=0;i<len;i++)
        //     cout<<prefix[i]<<" ";
        // cout<<endl;
        
        //某个数为1的情况
        for(int i=len-1;i>=0;i--)
        {
            if(prefix[i] == 1){
                ans = max(ans,i+1);
            }
        }
        //为-1的情况，取左右两端差的最远的-1
        int left=0;
        int right = 0;
        for(int i=0;i<len;i++){
            if(prefix[i] == -1)
            {
                left =i;
                break;
            }
        }
        for(int i=len-1;i>=0;i--)
        {
            if(prefix[i] == -1)
            {
                right = i;
                break;
            }
        }
        ans = max(right-left,ans);
        //还遍历什么啊，直接找的出来了
        // for(int i=0;i<len;i++){
        //     if(nums[i] >0) ans = max(ans,1);
        //     for(int j=i+1;j<len;j++){
        //         if(prefix[j] == 1){
        //             ans = max(ans,j+1);
        //             continue;
        //         } 

        //         if(prefix[j]==prefix[i]) { //只能是都是-1的情况了
        //             ans = max(ans,j-i);
        //            // cout<<i<<" "<<j<<endl;
        //         }
        //     }
        // }
        return ans;
    }
    
    
    int getMaxLen(vector<int>& nums) {
       int len = nums.size();
        vector<int> newNums;
        newNums.clear();
        int ans = 0;
        for(int i=0;i<len;i++){
            if(nums[i] == 0){
                if(newNums.size()>0)
                {
                    ans = max(ans,getMaxLenWithOut0(newNums));
                newNums.clear();
                }
                
            }else
            {
                newNums.push_back(nums[i]);
            }
        }
        //cout<<newNums.size()<<endl;
        if(newNums.size()>0) ans = max(ans,getMaxLenWithOut0(newNums));
        return ans;
        
    }
};
```

## 题目链接：  
https://leetcode-cn.com/problems/maximum-length-of-subarray-with-positive-product/