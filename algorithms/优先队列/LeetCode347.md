---
title: 前K个高频元素---LeetCode347(优先队列)
date: 2020-09-07 15:04:18
tags: [优先队列,堆]
---
## 题目描述：  
给定一个非空的整数数组，返回其中出现频率前 k 高的元素。

## 示例：   
```cpp
示例 1:
输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]

示例 2:
输入: nums = [1], k = 1
输出: [1]
 
提示：
你可以假设给定的 k 总是合理的，且 1 ≤ k ≤ 数组中不相同的元素的个数。
你的算法的时间复杂度必须优于 O(n log n) , n 是数组的大小。
题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的。
你可以按任意顺序返回答案。
```
<!-- more -->

## 解题思路:  
题目要求的速度是O(nlogn), 先做一遍统计是O(n),全部push来一次堆排序是O(nlogn)，那不正好满足题目要求吗，那直接优先队列没得说。  
### 递减优先队列
因为题目是要求前K大，那么很自然就能想到用递减的优先队列。全部push进去然后取前面k个不久行了。(这是没有灵魂的堆排序，这个和普通排序有啥区别)  
```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        //优先队列？
        unordered_map<int,int> record;
        int len = nums.size();
        for(int i=0;i<len;i++){
            record[nums[i]]++;
        }
        priority_queue< pair<int,int>> q;
        for(auto &x:record){
            q.push(make_pair(x.second,x.first));
        }
        vector<int> ans;
        for(int i=0;i<k;i++){
            ans.push_back(q.top().second);
            q.pop();
        }
        return ans;
    }
};
```

### 递增优先队列
题目要求前k个最大的，那我们其实可以**维护大小为k的最小堆**(堆顶的元素是最小的)，每次要插入时和堆顶元素比，如果比堆顶元素大才插入，不然不插入(这才是堆的正确用法,速度会快很多(在元素很多的情况下))  
这里要说明一下，优先队列是默认的最大堆，所以要改为最小堆，需要把第三个参数改为greater<???>。当然，你也可以直接在元素上取个负数。  
优先队列是按照pair的第一个元素为依据来进行排序的。  
代码如下： 
```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        //优先队列
        unordered_map<int,int> record;
        int len = nums.size();
        for(int i=0;i<len;i++){
            record[nums[i]]++;
        }
        //把递减队列改为递增队列，这样就不用全部push，而是维护一个k大的堆
        priority_queue<pair<int,int>> q;
        int qlen = 0;
        for(auto &x:record){
            if(qlen < k){
                q.push(make_pair(x.second*(-1),x.first));
                qlen++;
            }else{
                if(q.top().first*(-1) < x.second){
                    q.pop();
                    q.push(make_pair(x.second*(-1),x.first));
                }
            }   
        }
        vector<int> ans;
        for(int i=0;i<k;i++){
            ans.push_back(q.top().second);
            q.pop();
        }
        return ans;
    }
};
```


## 题目链接：  
https://leetcode-cn.com/problems/top-k-frequent-elements/